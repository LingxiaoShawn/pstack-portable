import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


installer = module("installer", "scripts/install_codex.py")
config = module("config", "shared/config.py")
renderer = module("renderer", "overrides/skills/brief/scripts/render.py")


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = ROOT / "plugins/pstack/skills"
        self.target = self.root / "project/.agents/skills"

    def test_install_update_and_uninstall_preserve_unrelated_skill(self):
        unrelated = self.target / "my-skill"
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("personal content")
        installer.install(self.target, self.source)
        self.assertEqual(len(list(self.target.glob("pstack*/SKILL.md"))), 51)
        shared = self.target / "pstack-runtime"
        mapping = json.loads((shared / "skill-map.json").read_text())
        for entry in mapping.values():
            self.assertTrue((shared / entry["path"]).is_file())
        script = self.target / "pstack-brief/scripts/render.py"
        output = self.root / "brief.html"
        subprocess.run([sys.executable, str(script), "--input", str(script.parents[1] / "assets/example.json"), "--output", str(output)], check=True, capture_output=True)
        self.assertIn("一次清楚的代码交接", output.read_text())
        installer.install(self.target, self.source)
        installer.install(self.target, self.source, uninstall=True)
        self.assertEqual((unrelated / "SKILL.md").read_text(), "personal content")
        self.assertFalse((self.target / installer.STATE).exists())

    def test_dry_run_has_no_filesystem_effect(self):
        actions = installer.install(self.target, self.source, dry_run=True)
        self.assertEqual(len(actions), 51)
        self.assertFalse(self.target.exists())

    def test_existing_unmanaged_collision_is_not_overwritten(self):
        collision = self.target / "pstack"
        collision.mkdir(parents=True)
        (collision / "SKILL.md").write_text("user version")
        with self.assertRaises(ValueError):
            installer.install(self.target, self.source)
        self.assertEqual((collision / "SKILL.md").read_text(), "user version")
        self.assertFalse((self.target / "pstack-how").exists())

    def test_modified_install_is_preserved_on_update_and_uninstall(self):
        installer.install(self.target, self.source)
        skill = self.target / "pstack/SKILL.md"
        skill.write_text("my local edits")
        for uninstall in [False, True]:
            with self.assertRaises(ValueError):
                installer.install(self.target, self.source, uninstall=uninstall)
        self.assertEqual(skill.read_text(), "my local edits")

    def test_install_rolls_back_if_a_late_move_fails(self):
        installer.install(self.target, self.source)
        before = installer.digest(self.target)
        real_replace = os.replace

        def fail_one_move(src, dst):
            if Path(src).parent.name == "new" and Path(src).name == "pstack-how":
                raise OSError("simulated disk failure")
            return real_replace(src, dst)

        with patch.object(installer.os, "replace", side_effect=fail_one_move):
            with self.assertRaises(OSError):
                installer.install(self.target, self.source)
        self.assertEqual(installer.digest(self.target), before)

    def test_tampered_state_cannot_escape_install_directory(self):
        self.target.mkdir(parents=True)
        (self.target / installer.STATE).write_text(json.dumps({"owner": installer.OWNER, "entries": {"../important": {}}}))
        with self.assertRaises(ValueError):
            installer.install(self.target, self.source, uninstall=True)

    def test_incomplete_update_cannot_remove_installed_skills(self):
        installer.install(self.target, self.source)
        before = installer.digest(self.target)
        empty = self.root / "broken-source"
        empty.mkdir()
        with self.assertRaises(ValueError):
            installer.install(self.target, empty)
        self.assertEqual(installer.digest(self.target), before)


class ConfigTests(unittest.TestCase):
    def test_defaults_and_project_precedence(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "home"
            project = Path(temp) / "project"
            self.assertEqual(config.resolve(project, home)[0]["roles"], {})
            global_config = home / ".config/pstack/config.json"
            global_config.parent.mkdir(parents=True)
            global_config.write_text(json.dumps({"language": "zh", "max_workers": 3}))
            self.assertEqual(config.resolve(project, home)[0]["language"], "zh")
            local = project / ".pstack/config.json"
            local.parent.mkdir(parents=True)
            local.write_text(json.dumps({"max_workers": 1}))
            self.assertEqual(config.resolve(project, home)[0]["max_workers"], 1)

    def test_invalid_config_fails_instead_of_silently_ignoring(self):
        for data in [{"max_workers": True}, {"max_workers": 0}, {"version": 2}, {"roles": {"review": []}}, {"roles": {"review": ["a", "b", "c"]}}, {"unexpected": 3}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                config.validate(data)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class BriefTests(unittest.TestCase):
    def example(self):
        return json.loads((ROOT / "overrides/skills/brief/assets/example.json").read_text())

    def test_untrusted_content_cannot_create_html_or_active_links(self):
        data = self.example()
        data["title"] = '<img src=x onerror="alert(1)">'
        data["summary"] = '</script><script>alert(2)</script>'
        data["sources"] = [{"label": "bad URL", "location": "javascript:alert(3)"}]
        parser = Parser()
        parser.feed(renderer.render(data))
        self.assertFalse(any(tag == "img" for tag, attrs in parser.tags))
        self.assertEqual(sum(tag == "script" for tag, attrs in parser.tags), 1)
        self.assertFalse(any(attrs.get("href", "").startswith("javascript:") for tag, attrs in parser.tags))

    def test_long_content_is_preserved(self):
        data = self.example()
        data["after"] = [f"Verified claim {i}" for i in range(50)]
        parser = Parser()
        parser.feed(renderer.render(data))
        content = " ".join(parser.text)
        for claim in data["after"]:
            self.assertIn(claim, content)
        self.assertEqual(sum(tag == "section" for tag, attrs in parser.tags), 5)

    def test_missing_evidence_is_rejected(self):
        data = self.example()
        data["sources"] = []
        with self.assertRaises(ValueError):
            renderer.render(data)


if __name__ == "__main__":
    unittest.main()

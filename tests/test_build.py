import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="pstack-build-test-")
        self.addCleanup(temp.cleanup)
        self.checkout = Path(temp.name)
        for name in ["scripts", "overrides", "shared", "upstream"]:
            shutil.copytree(ROOT / name, self.checkout / name,
                            ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
        for name in ["LICENSE", "upstream.lock.json"]:
            shutil.copy2(ROOT / name, self.checkout / name)
        self.command = [sys.executable, "-B", str(self.checkout / "scripts/build.py")]

    def test_build_generates_marketplaces_and_check_detects_missing_or_stale_files(self):
        checkout, command = self.checkout, self.command
        subprocess.run(command, check=True, capture_output=True)
        subprocess.run(command + ["--check"], check=True, capture_output=True)
        for relative, meta_dir in [
            (".agents/plugins/marketplace.json", ".codex-plugin"),
            (".claude-plugin/marketplace.json", ".claude-plugin"),
        ]:
            path = checkout / relative
            original = path.read_bytes()
            data = json.loads(original)
            self.assertEqual(data["name"], "pstack-portable")
            plugin, = data["plugins"]
            source = plugin["source"]
            source = source["path"] if isinstance(source, dict) else source
            manifest = json.loads((checkout / source / meta_dir / "plugin.json").read_text())
            self.assertEqual(plugin["name"], manifest["name"])

            for damage in ["missing", "stale"]:
                with self.subTest(path=relative, damage=damage):
                    if damage == "missing":
                        path.unlink()
                    else:
                        path.write_text('{}\n')
                    result = subprocess.run(command + ["--check"], text=True, capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(relative, result.stderr)
                    if damage == "missing":
                        self.assertFalse(path.exists())
                    else:
                        self.assertEqual(path.read_text(), '{}\n')
                    path.write_bytes(original)

    def test_release_version_changes_both_packages_and_invalidates_check(self):
        version = self.checkout / "overrides/version.txt"
        version.write_text("2.3.4\n")
        subprocess.run(self.command, check=True, capture_output=True)
        manifests = [self.checkout / "plugins/pstack/.codex-plugin/plugin.json",
                     self.checkout / "claude/plugins/pstack/.claude-plugin/plugin.json"]
        self.assertEqual([json.loads(p.read_text())["version"] for p in manifests],
                         ["2.3.4", "2.3.4"])
        version.write_text("2.3.5\n")
        result = subprocess.run(self.command + ["--check"], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Stale generated packages", result.stderr)
        self.assertEqual([json.loads(p.read_text())["version"] for p in manifests],
                         ["2.3.4", "2.3.4"])
        subprocess.run(self.command, check=True, capture_output=True)
        self.assertEqual([json.loads(p.read_text())["version"] for p in manifests],
                         ["2.3.5", "2.3.5"])
        subprocess.run(self.command + ["--check"], check=True, capture_output=True)

    def test_invalid_release_version_preserves_existing_packages(self):
        subprocess.run(self.command, check=True, capture_output=True)
        roots = [self.checkout / "plugins", self.checkout / "claude"]
        before = {p: p.read_bytes() for root in roots for p in root.rglob("*") if p.is_file()}
        (self.checkout / "overrides/version.txt").write_text("not-a-version\n")
        result = subprocess.run(self.command, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overrides/version.txt", result.stderr)
        self.assertEqual(before, {p: p.read_bytes() for root in roots
                                  for p in root.rglob("*") if p.is_file()})

    def test_validation_rejects_standalone_name_in_plugin_invocation(self):
        subprocess.run(self.command, check=True, capture_output=True)
        validate = [sys.executable, "-B", str(self.checkout / "scripts/validate.py")]
        subprocess.run(validate, check=True, capture_output=True)
        path = self.checkout / "plugins/pstack/skills/pstack-runtime/skill-map.json"
        mapping = json.loads(path.read_text())
        mapping["poteto-mode"]["invoke"] = "$pstack"
        path.write_text(json.dumps(mapping))
        result = subprocess.run(validate, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("poteto-mode", result.stderr)


if __name__ == "__main__":
    unittest.main()

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_build_generates_marketplaces_and_check_detects_missing_or_stale_files(self):
        with tempfile.TemporaryDirectory(prefix="pstack-build-test-") as temp:
            checkout = Path(temp)
            for name in ["scripts", "overrides", "shared", "upstream"]:
                shutil.copytree(ROOT / name, checkout / name,
                                ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
            for name in ["LICENSE", "upstream.lock.json"]:
                shutil.copy2(ROOT / name, checkout / name)

            command = [sys.executable, "-B", str(checkout / "scripts/build.py")]
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


if __name__ == "__main__":
    unittest.main()

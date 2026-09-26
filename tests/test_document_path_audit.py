from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "document_path_audit.py"
SPEC = importlib.util.spec_from_file_location("document_path_audit", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ApplySafeRewritesTests(unittest.TestCase):
    def test_canonical_paths_are_idempotent(self) -> None:
        canonical = (
            "documents/documentation/0-index.md\n"
            "../documents/documentation/application/auth.md\n"
            "documents/tasks/checklist/task.md\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "README.md"
            sample.write_text(canonical, encoding="utf-8")

            first = MODULE.apply_safe_rewrites(root)
            second = MODULE.apply_safe_rewrites(root)

            self.assertEqual(first, [])
            self.assertEqual(second, [])
            self.assertEqual(sample.read_text(encoding="utf-8"), canonical)

    def test_legacy_paths_rewrite_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "README.md"
            sample.write_text(
                "documentation/0-index.md\n"
                "docs/documentation/application/auth.md\n"
                "docs/tasks/checklist/task.md\n",
                encoding="utf-8",
            )

            first = MODULE.apply_safe_rewrites(root)
            second = MODULE.apply_safe_rewrites(root)

            self.assertEqual(first, [{"file": "README.md", "replacements": 3}])
            self.assertEqual(second, [])
            self.assertEqual(
                sample.read_text(encoding="utf-8"),
                "documents/documentation/0-index.md\n"
                "documents/documentation/application/auth.md\n"
                "documents/tasks/checklist/task.md\n",
            )

    def test_regex_literals_are_not_made_unparsable(self) -> None:
        source = r"assert.match(text, /documentation\/0-index\.md/);" + "\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "check.mjs"
            sample.write_text(source, encoding="utf-8")

            changes = MODULE.apply_safe_rewrites(root)

            self.assertEqual(changes, [])
            self.assertEqual(sample.read_text(encoding="utf-8"), source)

    def test_relative_paths_are_left_for_context_aware_repair(self) -> None:
        source = "../documentation/0-index.md\n./docs/tasks/checklist.md\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = root / "README.md"
            sample.write_text(source, encoding="utf-8")

            changes = MODULE.apply_safe_rewrites(root)

            self.assertEqual(changes, [])
            self.assertEqual(sample.read_text(encoding="utf-8"), source)


if __name__ == "__main__":
    unittest.main()

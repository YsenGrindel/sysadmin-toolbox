"""Unit tests for Config Drift Lite engine: no GUI or network."""
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ConfigDriftLite"))
from engine import compare, html_report


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.before = Path(self.tmp.name) / "before"
        self.after = Path(self.tmp.name) / "after"
        self.before.mkdir()
        self.after.mkdir()

    def write(self, base, name, value):
        target = base / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")

    def test_modified_added_removed_unchanged(self):
        self.write(self.before, "network.cfg", "route A\n")
        self.write(self.after, "network.cfg", "route B\n")
        self.write(self.before, "deleted.txt", "old\n")
        self.write(self.after, "added.txt", "new\n")
        self.write(self.before, "same.txt", "ok\n")
        self.write(self.after, "same.txt", "ok\n")
        result = compare(self.before, self.after)
        self.assertEqual(result.counts(), {
            "modified": 1, "added": 1, "removed": 1, "unchanged": 1,
        })
        changed = next(c for c in result.changes if c.path == "network.cfg")
        self.assertIn("-route A", changed.diff())
        self.assertIn("+route B", changed.diff())

    def test_secret_like_files_and_binaries_excluded(self):
        self.write(self.before, ".env", "TOKEN=should-not-appear")
        self.write(self.after, ".env", "TOKEN=different")
        (self.before / "binary.bin").write_bytes(b"\x00\x01\x02")
        (self.after / "binary.bin").write_bytes(b"\x00\x01\x02")
        result = compare(self.before, self.after)
        self.assertEqual(result.changes, [])
        self.assertEqual(len(result.skipped), 4)

    def test_html_escapes_untrusted_content(self):
        self.write(self.before, "a.txt", "safe\n")
        self.write(self.after, "a.txt", "<script>alert('x')</script>\n")
        rendered = html_report(compare(self.before, self.after))
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)

    def test_same_folder_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.before, self.before)

    def test_large_file_excluded(self):
        (self.before / "huge.txt").write_bytes(b"a" * 1000001)
        result = compare(self.before, self.after)
        self.assertEqual(result.changes, [])
        self.assertTrue(any("too large" in s for s in result.skipped))


if __name__ == "__main__":
    unittest.main()

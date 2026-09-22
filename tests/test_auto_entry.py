import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from auto_entry import write_auto_entry


class AutomaticEntryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.moment = datetime(2026, 9, 22, 17, 0, tzinfo=timezone.utc)
        self.run_url = "https://github.com/example/log/actions/runs/123"

    def test_local_day_and_disclosure(self):
        path, changed = write_auto_entry(self.root, self.moment, self.run_url)
        self.assertTrue(changed)
        self.assertEqual(path.relative_to(self.root).as_posix(), "entries/2026/09/2026-09-23.md")
        content = path.read_text(encoding="utf-8")
        self.assertIn("不代表仓库所有者当天完成了学习或研究", content)
        self.assertIn("2026-09-23 01:00:00 +0800", content)
        self.assertIn(self.run_url, content)

    def test_rerun_preserves_record(self):
        path, _ = write_auto_entry(self.root, self.moment, self.run_url)
        original = path.read_bytes()
        _, changed = write_auto_entry(self.root, self.moment.replace(hour=18), self.run_url + "4")
        self.assertFalse(changed)
        self.assertEqual(path.read_bytes(), original)

    def test_preserves_manual_entry(self):
        path = self.root / "entries/2026/09/2026-09-23.md"
        path.parent.mkdir(parents=True)
        path.write_text("My actual learning note", encoding="utf-8")
        _, changed = write_auto_entry(self.root, self.moment, self.run_url)
        self.assertFalse(changed)
        self.assertEqual(path.read_text(encoding="utf-8"), "My actual learning note")

    def test_next_local_day_creates_another_file(self):
        first, _ = write_auto_entry(self.root, self.moment, self.run_url)
        second, changed = write_auto_entry(self.root, self.moment.replace(day=23), self.run_url)
        self.assertTrue(changed)
        self.assertNotEqual(first, second)

    def test_rejects_ambiguous_time(self):
        with self.assertRaises(ValueError):
            write_auto_entry(self.root, self.moment.replace(tzinfo=None), self.run_url)


if __name__ == "__main__":
    unittest.main()

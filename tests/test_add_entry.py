import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from add_entry import entry_path, parse_comment, write_entry  # noqa: E402


SHANGHAI = timezone(timedelta(hours=8), name="Asia/Shanghai")


class ParseCommentTests(unittest.TestCase):
    def test_parses_category_and_multiline_text(self) -> None:
        category, text = parse_comment("/log [Python] 第一行\n第二行")

        self.assertEqual(category, "Python")
        self.assertEqual(text, "第一行\n第二行")

    def test_uses_default_category(self) -> None:
        category, text = parse_comment("/log 复习矩阵乘法")

        self.assertEqual(category, "随手记")
        self.assertEqual(text, "复习矩阵乘法")

    def test_rejects_an_empty_entry(self) -> None:
        with self.assertRaises(ValueError):
            parse_comment("/log   ")


class WriteEntryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.moment = datetime(2026, 7, 21, 20, 5, tzinfo=SHANGHAI)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_uses_year_and_month_directories(self) -> None:
        path = entry_path(self.root, self.moment)

        self.assertEqual(
            path.relative_to(self.root).as_posix(),
            "entries/2026/07/2026-07-21.md",
        )

    def test_creates_then_appends_to_the_daily_file(self) -> None:
        path, first_changed = write_entry(
            self.root,
            self.moment,
            "Python",
            "学会了列表推导式。",
            "https://github.com/example/repo/issues/1#issuecomment-10",
        )
        _, second_changed = write_entry(
            self.root,
            self.moment.replace(hour=21),
            "Statistics",
            "复习了标准差。",
            "https://github.com/example/repo/issues/1#issuecomment-11",
        )

        content = path.read_text(encoding="utf-8")
        self.assertTrue(first_changed)
        self.assertTrue(second_changed)
        self.assertEqual(content.count("# 2026-07-21"), 1)
        self.assertIn("## 20:05 · Python", content)
        self.assertIn("## 21:05 · Statistics", content)

    def test_source_url_makes_a_rerun_idempotent(self) -> None:
        source_url = "https://github.com/example/repo/issues/1#issuecomment-10"
        path, _ = write_entry(
            self.root,
            self.moment,
            "Python",
            "学会了列表推导式。",
            source_url,
        )
        before = path.read_text(encoding="utf-8")

        _, changed = write_entry(
            self.root,
            self.moment,
            "Python",
            "学会了列表推导式。",
            source_url,
        )

        self.assertFalse(changed)
        self.assertEqual(path.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()

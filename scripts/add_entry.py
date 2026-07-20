"""Create or append one daily learning-log entry."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


TIME_ZONE = timezone(timedelta(hours=8), name="Asia/Shanghai")
DEFAULT_CATEGORY = "随手记"
COMMENT_PATTERN = re.compile(
    r"\A/log(?:\s+\[([^\]\r\n]{1,40})\])?\s+(.+?)\s*\Z",
    re.DOTALL,
)


def parse_comment(comment: str) -> tuple[str, str]:
    """Parse `/log [optional category] text` into category and text."""

    match = COMMENT_PATTERN.fullmatch(comment.strip())
    if match is None:
        raise ValueError("评论格式应为 /log [分类] 学习内容，分类可以省略")

    category = (match.group(1) or DEFAULT_CATEGORY).strip()
    text = normalize_text(match.group(2))
    return category, text


def normalize_text(text: str) -> str:
    """Normalize line endings and reject empty or unreasonably large entries."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise ValueError("学习内容不能为空")
    if len(normalized) > 4_000:
        raise ValueError("单条学习记录不能超过 4000 个字符")
    return normalized


def normalize_category(category: str) -> str:
    """Validate the short category displayed in a section heading."""

    normalized = category.strip()
    if not normalized:
        return DEFAULT_CATEGORY
    if "\n" in normalized or "\r" in normalized or len(normalized) > 40:
        raise ValueError("分类必须是 1 到 40 个字符的单行文本")
    return normalized


def entry_path(root: Path, moment: datetime) -> Path:
    """Return entries/YYYY/MM/YYYY-MM-DD.md for the supplied moment."""

    return root / "entries" / moment.strftime("%Y") / moment.strftime("%m") / (
        moment.strftime("%Y-%m-%d") + ".md"
    )


def write_entry(
    root: Path,
    moment: datetime,
    category: str,
    text: str,
    source_url: str | None = None,
) -> tuple[Path, bool]:
    """Write an entry and return its path plus whether the file changed."""

    path = entry_path(root, moment)
    category = normalize_category(category)
    text = normalize_text(text)

    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if source_url and source_url in existing:
        return path, False

    path.parent.mkdir(parents=True, exist_ok=True)
    parts: list[str] = []
    if not existing:
        parts.append(f"# {moment:%Y-%m-%d}\n")

    parts.append(f"\n## {moment:%H:%M} · {category}\n\n{text}\n")
    if source_url:
        parts.append(f"\n[原始记录]({source_url})\n")

    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(parts))

    return path, True


def parse_moment(date_text: str | None, time_text: str | None) -> datetime:
    """Build a timezone-aware moment, defaulting to current Shanghai time."""

    now = datetime.now(TIME_ZONE)
    date_part = date_text or now.strftime("%Y-%m-%d")
    time_part = time_text or now.strftime("%H:%M")
    try:
        return datetime.strptime(
            f"{date_part} {time_part}", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=TIME_ZONE)
    except ValueError as exc:
        raise ValueError("日期或时间格式无效，应为 YYYY-MM-DD 和 HH:MM") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--comment", help="完整的 /log Issue 评论")
    source.add_argument("--text", help="不含 /log 前缀的学习内容")
    parser.add_argument("--category", default=DEFAULT_CATEGORY, help="本地记录分类")
    parser.add_argument("--date", help="记录日期，格式 YYYY-MM-DD")
    parser.add_argument("--time", help="记录时间，格式 HH:MM")
    parser.add_argument("--source-url", help="用于防止重复写入的原始评论链接")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="仓库根目录，默认由脚本位置推导",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.comment is not None:
            category, text = parse_comment(args.comment)
        else:
            category, text = args.category, normalize_text(args.text)

        moment = parse_moment(args.date, args.time)
        path, _changed = write_entry(
            root=args.root.resolve(),
            moment=moment,
            category=category,
            text=text,
            source_url=args.source_url,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(path.relative_to(args.root.resolve()).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Write an honest automatic run record, at most once per UTC+8 day."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from add_entry import TIME_ZONE, entry_path


def write_auto_entry(root: Path, moment: datetime, run_url: str) -> tuple[Path, bool]:
    """Preserve any existing daily file, including manually written entries."""
    if moment.tzinfo is None:
        raise ValueError("moment must include a time zone")
    moment = moment.astimezone(TIME_ZONE)
    path = entry_path(root, moment)
    if path.exists():
        return path, False

    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"# {moment:%Y-%m-%d}\n\n"
        "## 自动运行记录\n\n"
        "> 此记录由 GitHub Actions 自动生成，不代表仓库所有者当天完成了学习或研究。\n\n"
        f"- 运行时间：{moment:%Y-%m-%d %H:%M:%S %z}（新加坡 / 中国时间）。\n"
        "- 工作流已完成日志工具的单元测试和 Python 编译检查。\n"
        f"- 运行来源：[GitHub Actions]({run_url})。\n"
        "- 当日人工学习内容：未由此自动化填写。\n"
    )
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError:
        return path, False
    return path, True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    path, _ = write_auto_entry(root, datetime.now(TIME_ZONE), args.run_url)
    print(path.relative_to(root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

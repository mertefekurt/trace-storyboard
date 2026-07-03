from __future__ import annotations

import argparse
from pathlib import Path

from trace_storyboard.core import load_events, render_markdown, render_svg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render agent trace JSONL as Markdown or SVG.")
    parser.add_argument("trace", type=Path)
    parser.add_argument("--format", choices=("markdown", "svg"), default="markdown")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    events = load_events(args.trace)
    rendered = render_svg(events) if args.format == "svg" else render_markdown(events)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0

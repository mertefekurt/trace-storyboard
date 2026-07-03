from __future__ import annotations

from trace_storyboard.cli import main
from trace_storyboard.core import load_events, render_markdown, render_svg, summarize


def sample(tmp_path):
    path = tmp_path / "trace.jsonl"
    path.write_text('{"actor":"a","action":"x","message":"one","latency_ms":10}\n', encoding="utf-8")
    return path


def test_load_events(tmp_path) -> None:
    assert load_events(sample(tmp_path))[0].actor == "a"


def test_summary_by_actor(tmp_path) -> None:
    assert summarize(load_events(sample(tmp_path))) == {"a": 10}


def test_markdown_table(tmp_path) -> None:
    assert "| step |" in render_markdown(load_events(sample(tmp_path)))


def test_svg_has_trace_text(tmp_path) -> None:
    svg = render_svg(load_events(sample(tmp_path)))
    assert "<svg" in svg and "one" in svg


def test_cli_writes_output(tmp_path) -> None:
    out = tmp_path / "trace.svg"
    assert main([str(sample(tmp_path)), "--format", "svg", "--output", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("<svg")


def test_cli_help(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    assert "trace" in capsys.readouterr().out

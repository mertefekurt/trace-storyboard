from __future__ import annotations

import html
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Event:
    index: int
    actor: str
    action: str
    message: str
    latency_ms: int
    time: str


def load_events(path: Path) -> list[Event]:
    events: list[Event] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        raw = json.loads(line)
        events.append(
            Event(
                index=index,
                actor=str(raw.get("actor", "agent")),
                action=str(raw.get("action", "event")),
                message=str(raw.get("message", "")),
                latency_ms=int(raw.get("latency_ms", 0) or 0),
                time=str(raw.get("time", index)),
            )
        )
    return events


def summarize(events: list[Event]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for event in events:
        totals[event.actor] = totals.get(event.actor, 0) + event.latency_ms
    return totals


def render_markdown(events: list[Event]) -> str:
    lines = [
        "# Trace Storyboard",
        "",
        "| step | actor | action | latency | message |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for event in events:
        lines.append(
            f"| {event.index} | {event.actor} | {event.action} | {event.latency_ms}ms | {event.message} |"
        )
    lines.extend(["", "## Latency by actor"])
    for actor, latency in sorted(summarize(events).items()):
        lines.append(f"- `{actor}`: {latency}ms")
    return "\n".join(lines) + "\n"


def render_svg(events: list[Event]) -> str:
    height = 120 + 74 * max(len(events), 1)
    rows = []
    for offset, event in enumerate(events):
        y = 86 + offset * 74
        color = "#38bdf8" if offset % 2 == 0 else "#f97316"
        rows.append(
            f'<circle cx="86" cy="{y}" r="15" fill="{color}"/>'
            f'<text x="122" y="{y - 8}" fill="#f8fafc" font-size="22" font-weight="700">'
            f"{html.escape(event.actor)} / {html.escape(event.action)}</text>"
            f'<text x="122" y="{y + 22}" fill="#cbd5e1" font-size="18">'
            f"{html.escape(event.message)} · {event.latency_ms}ms</text>"
        )
    return (
        f'<svg width="980" height="{height}" viewBox="0 0 980 {height}" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<rect width="980" height="100%" rx="24" fill="#0f172a"/>'
        '<text x="56" y="48" fill="#f8fafc" font-size="30" font-weight="800">Trace Storyboard</text>'
        f"{''.join(rows)}</svg>"
    )

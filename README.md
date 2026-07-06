# Trace Storyboard

Turn agent trace JSONL into a readable timeline or an SVG storyboard.

![Trace Storyboard cover](assets/readme-cover.svg)

## Two outputs

Markdown is best for pull requests and incident notes. SVG is best when the trace needs to become a quick visual artifact.

```bash
git clone https://github.com/mertefekurt/trace-storyboard.git
cd trace-storyboard
python -m pip install -e ".[dev]"
trace-storyboard examples/agent-trace.jsonl
trace-storyboard examples/agent-trace.jsonl --format svg --output trace.svg
```

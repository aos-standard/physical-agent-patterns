import datetime
import os
import pathlib
import sys

import anthropic

OUTPUT_DIR = pathlib.Path(__file__).parent / "output"
DEFAULT_MODEL = "claude-haiku-4-5"


def run(prompt: str = "List 3 practical trends in AI agents this week.") -> pathlib.Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    output_path = OUTPUT_DIR / f"agent_run_{today}.md"

    if output_path.exists():
        print(f"[skip] Output already exists for {today}: {output_path}")
        return output_path

    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text
    output_path.write_text(f"# Agent Run: {today}\n\n{content}\n", encoding="utf-8")

    # Physical evidence is now on disk — only then declare completion
    print(f"[done] Output written: {output_path}")
    return output_path


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    run(prompt) if prompt else run()

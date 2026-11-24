import os
from pathlib import Path

LINE = "I asked for a raise and HR threw me a pizza party instead. I now earn 0.4 slices an hour — before tax."


def main() -> None:
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "entry.txt").write_text(LINE + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

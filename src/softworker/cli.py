import json
from typing import Optional
from pathlib import Path
from typer import Typer, Argument, Option
from softworker import render_pdf_from_dict
from softworker.enums import ResumeLanguage
from softworker.settings import settings

app: Typer = Typer(no_args_is_help=True)

@app.command()
def render(
    input_path: Path,
    output_path: Optional[Path] = Argument(None),
    resume_language: ResumeLanguage = Option(settings.DEFAULT_LANGUAGE, "--resume-language", "--language", "-l")
) -> None:
    pdf: bytes = render_pdf_from_dict(resume_dict=json.loads(input_path.read_text(encoding="utf-8")), resume_language=resume_language)
    output_path = output_path or Path.cwd() / f"{input_path.stem}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf)
    print(output_path)

if __name__ == "__main__":
    app()

from typing import Optional
from pathlib import Path
from typer import Typer, Argument
from antimeta_resume import render_pdf_from_json

app: Typer = Typer(no_args_is_help=True)

@app.command()
def render(input_path: Path, output_path: Optional[Path] = Argument(None)) -> None:
    pdf: bytes = render_pdf_from_json(input_path)
    output_path = output_path or Path.cwd() / f"{input_path.stem}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf)
    print(output_path)

if __name__ == "__main__":
    app()

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Any
from resume_pycli import html as resume_html
from weasyprint import HTML, CSS
from softworker.enums import ResumeLanguage
from softworker.i18n import get_theme_i18n
from softworker.render_utils import format_date, format_url, format_mail
from softworker.schemas import ResumeSchema
from softworker.settings import settings

def render_pdf(resume: ResumeSchema, resume_language: ResumeLanguage = settings.DEFAULT_LANGUAGE) -> bytes:
    i18n: Dict[str, Any] = get_theme_i18n(settings.THEME_PATH, resume_language)
    context: Dict[str, Any] = {
        "resume": resume.model_dump(mode="python", by_alias=True),
        "format_date": lambda date: format_date(date, locale=str(i18n["babel_locale"]), current_label=str(i18n["present"])),
        "format_url": format_url,
        "format_mail": format_mail,
        "i18n": i18n
    }

    with TemporaryDirectory() as tmpdir:
        output_directory: Path = Path(tmpdir)
        resume_html.export(
            resume=context,
            theme=settings.THEME_PATH,
            output=output_directory
        )

        html_path, pdf_path = output_directory / "index.html", output_directory / "index.pdf"
        html: HTML = HTML(filename=str(html_path), base_url=str(output_directory))
        html.write_pdf(
            target=str(pdf_path),
            stylesheets=[CSS(string="@page { size: A4 }")],
            pdf_variant="pdf/ua-1",
            pdf_tags=True,
            custom_metadata=True
        )

        return pdf_path.read_bytes()

def render_pdf_from_dict(resume_dict: Dict[str, Any], resume_language: ResumeLanguage = settings.DEFAULT_LANGUAGE) -> bytes:
    resume: ResumeSchema = ResumeSchema.model_validate(resume_dict)
    return render_pdf(resume, resume_language=resume_language)

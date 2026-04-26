from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
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

    theme_env: Environment = Environment(loader=FileSystemLoader(settings.THEME_PATH), autoescape=select_autoescape(["html", "xml"]))
    html_content: str = theme_env.get_template("index.html").render(**context)
    return HTML(string=html_content, base_url=str(settings.THEME_PATH)).write_pdf(
        stylesheets=[CSS(string="@page { size: A4 }")],
        pdf_variant="pdf/ua-1",
        pdf_tags=True,
        custom_metadata=True
    )

def render_pdf_from_dict(resume_dict: Dict[str, Any], resume_language: ResumeLanguage = settings.DEFAULT_LANGUAGE) -> bytes:
    resume: ResumeSchema = ResumeSchema.model_validate(resume_dict)
    return render_pdf(resume, resume_language=resume_language)

# CV PDF generation using WeasyPrint - Danish CV compliant, A4, 2-page max
from __future__ import annotations

from typing import Any

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


# CSS as a module-level constant to avoid f-string brace conflicts
CV_CSS = r"""
        @page {
            size: A4;
            margin: 2.5cm 2cm;
        }

        @font-face {
            font-family: 'Collapse';
            src: url('file:///opt/career-ops-dashboard/frontend/public/fonts/Collapse-Bold.woff2') format('woff2');
            font-weight: 700;
        }
        @font-face {
            font-family: 'JetBrains Mono';
            src: url('file:///opt/career-ops-dashboard/frontend/public/fonts/JetBrainsMono-Regular.woff2') format('woff2');
        }
        @font-face {
            font-family: 'JetBrains Mono';
            src: url('file:///opt/career-ops-dashboard/frontend/public/fonts/JetBrainsMono-Bold.woff2') format('woff2');
            font-weight: 700;
        }
        @font-face {
            font-family: 'Segoe UI';
            src: local('Segoe UI'), local('system-ui');
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 10pt;
            line-height: 1.45;
            color: #1e293b;
            margin: 0;
        }

        .hermes-mono {
            font-family: 'JetBrains Mono', monospace;
            font-variant-numeric: tabular-nums;
        }

        h1, h2, h3 {
            font-family: 'Collapse', 'JetBrains Mono', monospace;
            font-weight: 700;
            color: #0f172a;
            margin: 0 0 0.5em 0;
            page-break-after: avoid;
        }

        h1 { font-size: 1.8em; }
        h2 { font-size: 1.25em; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.25em; margin-top: 1.5em; }
        h3 { font-size: 1.1em; color: #334155; }

        a { color: #0053fd; text-decoration: none; }
        a:hover { text-decoration: underline; }

        .cv-name { margin-bottom: 0.25em; }
        .cv-contact { color: #475569; margin: 0.25em 0; font-size: 0.95em; }
        .cv-target { color: #0053fd; font-style: italic; margin: 0.25em 0; }
        .cv-target .hermes-mono { font-size: 0.95em; }

        .cv-section { margin-bottom: 1.25em; }

        .cv-entry { margin-bottom: 1em; page-break-inside: avoid; }
        .cv-entry-header { display: flex; flex-wrap: wrap; gap: 1em; align-items: baseline; margin-bottom: 0.35em; }
        .cv-company { color: #0f172a; font-weight: 600; }
        .cv-role { color: #334155; font-weight: 500; }
        .cv-period { color: #64748b; font-size: 0.9em; white-space: nowrap; }

        .cv-entry ul { margin: 0.5em 0 0 1.25em; padding: 0; }
        .cv-entry li { margin: 0.2em 0; line-height: 1.5; }

        .cv-skills { list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 2em; }
        .cv-skills li { margin: 0.25em 0; break-inside: avoid; }
        .cv-skills strong { color: #0f172a; }

        .cv-education { list-style: none; padding: 0; margin: 0; }
        .cv-edu-entry { margin: 0.5em 0; }
        .cv-edu-entry strong { color: #0f172a; }
        .cv-edu-entry time { color: #64748b; font-size: 0.9em; margin-left: 1em; }

        /* Photo placeholder */
        .cv-header {
            display: grid;
            grid-template-columns: 3.5cm 1fr;
            gap: 1.5em;
            margin-bottom: 1.5em;
        }
        .cv-photo {
            width: 100%;
            aspect-ratio: 4/5;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Two-column layout for main content */
        .cv-main { display: contents; }

        @media print {
            .cv-photo { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        }
"""


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return (
        text.replace("&", "&")
        .replace("<", "<")
        .replace(">", ">")
        .replace('"', '"')
        .replace("'", "'")
    )


def cv_to_html(cv: dict[str, Any], role_target: str = "") -> str:
    """Convert CV JSON to HTML matching Hermes design system."""
    p = cv.get("profile", {})
    exp = cv.get("experience", [])
    skills = cv.get("skills", [])
    edu = cv.get("education", [])

    # Personal section
    personal_lines = []
    if p.get("name"):
        personal_lines.append(f'<h1 class="cv-name">{escape_html(p["name"])}</h1>')
    contact_parts = []
    if p.get("email"):
        contact_parts.append(f'<a href="mailto:{escape_html(p["email"])}">{escape_html(p["email"])}</a>')
    if p.get("phone"):
        contact_parts.append(escape_html(p["phone"]))
    if p.get("linkedin"):
        url = p["linkedin"]
        display = escape_html(url.replace("https://", "").replace("http://", ""))
        contact_parts.append(f'<a href="{escape_html(url)}">{display}</a>')
    if p.get("github"):
        url = p["github"]
        display = escape_html(url.replace("https://", "").replace("http://", ""))
        contact_parts.append(f'<a href="{escape_html(url)}">{display}</a>')
    if contact_parts:
        personal_lines.append(f'<p class="cv-contact">{"  .  ".join(contact_parts)}</p>')
    if p.get("roleTarget"):
        personal_lines.append(f'<p class="cv-target">Target: {escape_html(p["roleTarget"])}</p>')

    personal_html = "\n".join(personal_lines)

    # Summary
    summary_html = ""
    if p.get("summary"):
        summary_html = f"""
        <section class="cv-section">
            <h2>Profile</h2>
            <p>{escape_html(p["summary"])}</p>
        </section>
        """

    # Experience
    exp_html = ""
    if exp:
        exp_items = []
        for e in exp:
            company = escape_html(e.get("company", ""))
            role = escape_html(e.get("role", ""))
            start = e.get("start", "")
            end = e.get("end", "Present")
            loc = escape_html(e.get("location", ""))
            bullets = e.get("bullets", "").replace("\n", "\n").strip()

            period = f"{start} - {end}" if start else end
            meta_parts = [period]
            if loc:
                meta_parts.append(loc)
            meta = "  .  ".join(meta_parts)

            bullet_html = ""
            if bullets:
                bullet_lines = [f"<li>{escape_html(b.strip())}</li>" for b in bullets.split("\n") if b.strip()]
                bullet_html = f"<ul>{''.join(bullet_lines)}</ul>"

            exp_items.append(f"""
            <article class="cv-entry">
                <header class="cv-entry-header">
                    <h3 class="cv-company">{company}</h3>
                    <h3 class="cv-role">{role}</h3>
                    <time class="cv-period hermes-mono" datetime="{start}">{meta}</time>
                </header>
                {bullet_html}
            </article>
            """)

        exp_html = f"""
        <section class="cv-section">
            <h2>Experience</h2>
            {''.join(exp_items)}
        </section>
        """

    # Skills
    skills_html = ""
    if skills:
        by_cat: dict[str, list[str]] = {}
        for s in skills:
            cat = s.get("category", "Other")
            by_cat.setdefault(cat, []).append(s.get("name", ""))

        cat_lines = []
        for cat, names in by_cat.items():
            escaped = [escape_html(n) for n in names]
            cat_lines.append(f'<li><strong>{escape_html(cat)}:</strong> {", ".join(escaped)}</li>')

        skills_html = f"""
        <section class="cv-section">
            <h2>Skills</h2>
            <ul class="cv-skills">
                {''.join(cat_lines)}
            </ul>
        </section>
        """

    # Education
    edu_html = ""
    if edu:
        edu_items = []
        for e in edu:
            inst = escape_html(e.get("institution", ""))
            deg = escape_html(e.get("degree", ""))
            start = e.get("start", "")
            end = e.get("end", "")
            period = f"{start} - {end}" if start else end
            edu_items.append(f"""
            <li class="cv-edu-entry">
                <strong>{deg}</strong> - {inst}
                <time class="hermes-mono" datetime="{start}">({period})</time>
            </li>
            """)

        edu_html = f"""
        <section class="cv-section">
            <h2>Education</h2>
            <ul class="cv-education">
                {''.join(edu_items)}
            </ul>
        </section>
        """

    # Danish CV additions
    interests_html = ""
    if p.get("interests"):
        interests_html = f"""
        <section class="cv-section">
            <h2>Interests</h2>
            <p>{escape_html(p["interests"])}</p>
        </section>
        """

    languages_html = ""
    if p.get("languages"):
        languages_html = f"""
        <section class="cv-section">
            <h2>Languages</h2>
            <p>{escape_html(p["languages"])}</p>
        </section>
        """

    # Full HTML document
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CV - {escape_html(p.get('name', 'Candidate'))}</title>
    <style>
{CV_CSS}
    </style>
</head>
<body>
    <div class="cv-header">
        <div class="cv-photo">PHOTO</div>
        <div class="cv-main">
            {personal_html}
            {summary_html}
            {exp_html}
            {skills_html}
            {edu_html}
            {interests_html}
            {languages_html}
        </div>
    </div>
</body>
</html>
"""


def generate_pdf(cv: dict[str, Any], role_target: str = "") -> bytes:
    """Generate PDF from CV dict using WeasyPrint."""
    html_content = cv_to_html(cv, role_target)
    font_config = FontConfiguration()
    html = HTML(string=html_content)
    css = CSS(string="", font_config=font_config)
    return html.write_pdf(stylesheets=[css], font_config=font_config)


def generate_cv_pdf(
    profile: dict,
    experience: list[dict],
    skills: list[dict],
    education: list[dict],
    role_target: str = "AI Engineer",
) -> bytes:
    """Main entry point - matches router signature."""
    cv = {
        "profile": profile,
        "experience": experience,
        "skills": skills,
        "education": education,
    }
    return generate_pdf(cv, role_target)

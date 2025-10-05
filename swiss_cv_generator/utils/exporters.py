"""
Export-Utilities für verschiedene Ausgabeformate
"""

import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from ..data_models import CV


class BatchGenerator:
    """Batch-Generierung und Export von CVs"""

    def __init__(self, cv_generator):
        self.cv_generator = cv_generator

    def generate_batch(self, count: int) -> List[CV]:
        """Generiert eine Batch von CVs"""
        return self.cv_generator.generate_batch(count)

    def export_csv(self, cvs: List[CV], filename: str) -> str:
        """Exportiert CVs als CSV"""
        if not cvs:
            raise ValueError("Keine CVs zum Exportieren")

        # Konvertiere zu flacher Datenstruktur
        data = []
        for cv in cvs:
            row = cv.to_dict()

            # Zusätzliche berechnete Felder
            row.update({
                "education_count": len(cv.education),
                "career_positions": len(cv.career),
                "language_count": len(cv.skills.languages),
                "professional_skills_count": len(cv.skills.professional_skills),
                "languages_list": "; ".join(cv.skills.languages.keys()),
                "professional_skills_list": "; ".join(cv.skills.professional_skills),
                "it_skills_list": "; ".join(cv.skills.it_skills),
                "hobbies_list": "; ".join(cv.hobbies)
            })

            data.append(row)

        # Zu Pandas DataFrame und CSV exportieren
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')

        return f"Erfolgreich {len(cvs)} CVs nach {filename} exportiert"

    def export_json(self, cvs: List[CV], filename: str, pretty: bool = True) -> str:
        """Exportiert CVs als JSON"""
        if not cvs:
            raise ValueError("Keine CVs zum Exportieren")

        # Konvertiere zu serialisierbarer Struktur
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_cvs": len(cvs),
                "generator_version": "1.0.0"
            },
            "cvs": [cv.dict() for cv in cvs]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            else:
                json.dump(data, f, ensure_ascii=False, default=str)

        return f"Erfolgreich {len(cvs)} CVs nach {filename} exportiert"

    def export_excel(self, cvs: List[CV], filename: str) -> str:
        """Exportiert CVs als Excel mit mehreren Sheets"""
        if not cvs:
            raise ValueError("Keine CVs zum Exportieren")

        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Haupt-CV-Daten
            main_data = [cv.to_dict() for cv in cvs]
            df_main = pd.DataFrame(main_data)
            df_main.to_excel(writer, sheet_name='CVs_Übersicht', index=False)

            # Bildungsdaten
            education_data = []
            for cv in cvs:
                for edu in cv.education:
                    education_data.append({
                        'cv_id': cv.cv_id,
                        'person': f"{cv.persona.personal.first_name} {cv.persona.personal.last_name}",
                        'level': edu.level.value,
                        'institution': edu.institution,
                        'start_year': edu.start_year,
                        'end_year': edu.end_year,
                        'qualification': edu.qualification
                    })

            if education_data:
                df_edu = pd.DataFrame(education_data)
                df_edu.to_excel(writer, sheet_name='Bildungswege', index=False)

            # Karrieredaten
            career_data = []
            for cv in cvs:
                for career in cv.career:
                    career_data.append({
                        'cv_id': cv.cv_id,
                        'person': f"{cv.persona.personal.first_name} {cv.persona.personal.last_name}",
                        'position': career.position,
                        'company': career.company,
                        'start_year': career.start_year,
                        'end_year': career.end_year,
                        'duration_years': career.duration_years,
                        'workload': career.workload
                    })

            if career_data:
                df_career = pd.DataFrame(career_data)
                df_career.to_excel(writer, sheet_name='Karriereverläufe', index=False)

        return f"Erfolgreich {len(cvs)} CVs nach {filename} exportiert"


class CVFormatter:
    """Formatierung von CVs für verschiedene Ausgaben"""

    @staticmethod
    def to_formatted_text(cv: CV) -> str:
        """Formatiert CV als lesbaren Text"""
        return cv.to_formatted_text()

    @staticmethod
    def to_html(cv: CV) -> str:
        """Formatiert CV als HTML"""
        persona = cv.persona.personal

        html = f"""
        <div class="cv">
            <div class="header">
                <h1>{persona.first_name} {persona.last_name}</h1>
                <p>Alter: {persona.age} | {persona.city}, {persona.canton}</p>
                <p>Sprachregion: {persona.language_region.value}</p>
            </div>

            <div class="section">
                <h2>Ausbildung</h2>
                <ul>
        """

        for edu in cv.education:
            html += f"""
                    <li>
                        <strong>{edu.start_year}-{edu.end_year}:</strong> {edu.level.value}<br>
                        {edu.institution}<br>
                        <em>{edu.qualification}</em>
                    </li>
            """

        html += """
                </ul>
            </div>

            <div class="section">
                <h2>Beruflicher Werdegang</h2>
                <ul>
        """

        for career in cv.career:
            end_year = career.end_year if career.end_year else "heute"
            html += f"""
                    <li>
                        <strong>{career.start_year}-{end_year}:</strong> {career.position}<br>
                        {career.company}, {career.location}<br>
                        <em>{career.employment_type}, {career.workload}</em>
                    </li>
            """

        html += f"""
                </ul>
            </div>

            <div class="section">
                <h2>Sprachkenntnisse</h2>
                <ul>
        """

        for lang, level in cv.skills.languages.items():
            html += f"<li>{lang.capitalize()}: {level}</li>"

        html += f"""
                </ul>
            </div>

            <div class="section">
                <h2>Hobbies</h2>
                <p>{', '.join(cv.hobbies)}</p>
            </div>
        </div>
        """

        return html

    @staticmethod
    def to_markdown(cv: CV) -> str:
        """Formatiert CV als Markdown"""
        persona = cv.persona.personal

        md = (
            f"# {persona.first_name} {persona.last_name}\n\n"
            f"**Alter:** {persona.age} Jahre  \n"
            f"**Wohnort:** {persona.city}, {persona.canton}  \n"
            f"**Sprachregion:** {persona.language_region.value}  \n"
            f"**Sektor:** {cv.persona.sector}\n\n"
            "## Ausbildung\n\n"
        )

        for edu in cv.education:
            md += f"- **{edu.start_year}-{edu.end_year}:** {edu.level.value}  \n"
            md += f"  *{edu.institution}*  \n"
            md += f"  {edu.qualification}\n\n"

        md += "## Beruflicher Werdegang\n\n"

        for career in cv.career:
            end_year = career.end_year if career.end_year else "heute"
            md += f"- **{career.start_year}-{end_year}:** {career.position}  \n"
            md += f"  *{career.company}, {career.location}*  \n"
            md += f"  {career.employment_type}, {career.workload}\n\n"

        md += "## Sprachkenntnisse\n\n"

        for lang, level in cv.skills.languages.items():
            md += f"- **{lang.capitalize()}:** {level}\n"

        md += f"\n## Hobbies\n\n{', '.join(cv.hobbies)}"

        return md

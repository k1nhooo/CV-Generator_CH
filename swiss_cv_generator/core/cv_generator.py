"""
Swiss CV Generator - Generiert vollständige Lebensläufe basierend auf Personas
"""

import random
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from ..data.education import EDUCATION_INSTITUTIONS, QUALIFICATIONS
from ..data.companies import SWISS_COMPANIES, SECTOR_COMPANIES
from ..data_models import (
    CV, Education, Career, Skills, EducationLevel, 
    Persona, LanguageRegion
)
from .persona_generator import SwissPersonaGenerator


class SwissCVGenerator:
    """Generiert vollständige synthetische Lebensläufe für den Schweizer Arbeitsmarkt"""

    def __init__(self, random_seed: Optional[int] = None):
        if random_seed:
            random.seed(random_seed)
        self.persona_generator = SwissPersonaGenerator(random_seed)
        self.current_year = datetime.now().year

    def generate_cv(self, persona: Optional[Persona] = None) -> CV:
        """Generiert einen vollständigen Lebenslauf"""
        if persona is None:
            persona = self.persona_generator.generate_persona()

        education = self._generate_education_path(persona)
        career = self._generate_career_path(persona, education)
        skills = self._generate_skills_and_languages(persona)
        hobbies = self._generate_hobbies()

        return CV(
            cv_id=f"CH-CV-{random.randint(100000, 999999)}",
            persona=persona,
            education=education,
            career=career,
            skills=skills,
            hobbies=hobbies,
            generated_date=datetime.now()
        )

    def _generate_education_path(self, persona: Persona) -> List[Education]:
        """Generiert realistischen Bildungsweg basierend auf regionalen Präferenzen"""
        education_path = []
        region = persona.personal.language_region
        birth_year = persona.personal.birth_year

        # Obligatorische Schulzeit (6-15 Jahre)
        primary_school = Education(
            level=EducationLevel.OBLIGATORISCH,
            institution=f"Primarschule und Sekundarschule {persona.personal.city}",
            start_year=birth_year + 6,
            end_year=birth_year + 15,
            qualification=random.choice(QUALIFICATIONS["obligatorisch"])
        )
        education_path.append(primary_school)

        # Bildungsweg bestimmen (regional unterschiedlich)
        preferences = self.persona_generator.get_regional_education_preferences(region)
        education_route = random.choices(
            ["vocational", "academic"],
            weights=[preferences["vocational"], preferences["academic"]],
            k=1
        )[0]

        if education_route == "vocational":
            # Berufslehre (16-19 Jahre)
            institution = random.choice(EDUCATION_INSTITUTIONS["vocational"][region.value])
            qualification = random.choice(QUALIFICATIONS["berufslehre"])

            vocational_education = Education(
                level=EducationLevel.BERUFSLEHRE,
                institution=institution,
                start_year=birth_year + 16,
                end_year=birth_year + 19,
                qualification=qualification,
                field_of_study=random.choice(persona.sector_data["roles"])
            )
            education_path.append(vocational_education)

            # Höhere Berufsbildung (optional, 30% Chance bei Alter > 25)
            if random.random() < 0.3 and persona.personal.age > 25:
                higher_education = Education(
                    level=EducationLevel.HOEHERE_BERUFSBILDUNG,
                    institution=f"Höhere Fachschule {persona.personal.canton}",
                    start_year=birth_year + 22,
                    end_year=birth_year + 24,
                    qualification=random.choice(QUALIFICATIONS["weiterbildung"])
                )
                education_path.append(higher_education)

        else:
            # Akademischer Weg
            # Gymnasium (16-19 Jahre)
            gymnasium = random.choice(EDUCATION_INSTITUTIONS["gymnasium"][region.value])
            gym_education = Education(
                level=EducationLevel.GYMNASIUM,
                institution=gymnasium,
                start_year=birth_year + 16,
                end_year=birth_year + 19,
                qualification=random.choice(QUALIFICATIONS["gymnasium"])
            )
            education_path.append(gym_education)

            # Hochschulstudium (80% Chance)
            if random.random() < 0.8:
                university = random.choice(EDUCATION_INSTITUTIONS["universities"][region.value])

                # Bachelor (20-23 Jahre)
                bachelor = Education(
                    level=EducationLevel.UNIVERSITAET,
                    institution=university,
                    start_year=birth_year + 20,
                    end_year=birth_year + 23,
                    qualification=random.choice([q for q in QUALIFICATIONS["universitaet"] if "Bachelor" in q])
                )
                education_path.append(bachelor)

                # Master (70% Chance)
                if random.random() < 0.7:
                    master = Education(
                        level=EducationLevel.UNIVERSITAET,
                        institution=university,
                        start_year=birth_year + 23,
                        end_year=birth_year + 25,
                        qualification=random.choice([q for q in QUALIFICATIONS["universitaet"] if "Master" in q])
                    )
                    education_path.append(master)

        return education_path

    def _generate_career_path(self, persona: Persona, education: List[Education]) -> List[Career]:
        """Generiert realistische Berufslaufbahn"""
        if not education:
            return []

        sector_data = persona.sector_data
        progression = sector_data["career_progression"]

        # Berufseinstieg nach letztem Bildungsabschluss
        career_start_year = max(edu.end_year for edu in education) + 1
        working_years = max(0, self.current_year - career_start_year)

        if working_years <= 0:
            return []

        career_positions = []
        current_year = career_start_year
        position_index = 0

        while current_year < self.current_year and position_index < len(progression):
            # Dauer pro Position variiert
            if position_index == 0:  # Einstiegslevel
                duration = random.randint(2, 4)
            elif position_index == 1:  # Zweite Stufe
                duration = random.randint(3, 5)
            else:  # Führungspositionen
                duration = random.randint(4, 8)

            end_year = min(current_year + duration, self.current_year)

            # Unternehmensgröße basierend auf Karrierelevel
            if position_index <= 1:
                company_weights = [50, 30, 20]  # Klein, Mittel, Groß
            else:
                company_weights = [20, 40, 40]  # Mehr große Unternehmen für Senior-Positionen

            company_size = random.choices(
                ["small", "medium", "large"],
                weights=company_weights,
                k=1
            )[0]

            # Wähle Unternehmen (sektor-spezifisch wenn verfügbar)
            if persona.sector in SECTOR_COMPANIES and company_size in SECTOR_COMPANIES[persona.sector]:
                companies = SECTOR_COMPANIES[persona.sector][company_size]
            else:
                companies = SWISS_COMPANIES[company_size]

            company = random.choice(companies)

            # Arbeitspensum (Frauen arbeiten häufiger Teilzeit)
            if persona.personal.gender.value == "female" and random.random() < 0.3:
                workload = random.choice(["80%", "90%"])
            else:
                workload = "100%"

            position = Career(
                position=progression[position_index],
                company=company,
                location=persona.personal.city,
                start_year=current_year,
                end_year=end_year if end_year < self.current_year else None,
                duration_years=end_year - current_year,
                employment_type="Festanstellung",
                workload=workload
            )

            career_positions.append(position)

            current_year = end_year
            position_index += 1

            if current_year >= self.current_year:
                break

        return career_positions

    def _generate_skills_and_languages(self, persona: Persona) -> Skills:
        """Generiert Sprach- und Fachkompetenzen"""
        region = persona.personal.language_region
        primary_lang = persona.personal.primary_language

        # Sprachkenntnisse
        languages = {primary_lang: "Muttersprache"}

        # Andere Schweizer Landessprachen
        other_swiss_langs = [lang for lang in ["deutsch", "français", "italiano"] if lang != primary_lang]

        for lang in other_swiss_langs[:2]:  # 1-2 andere Schweizer Sprachen
            level = random.choices(
                ["Grundkenntnisse", "Gute Kenntnisse", "Sehr gute Kenntnisse", "Verhandlungssicher"],
                weights=[20, 35, 30, 15],
                k=1
            )[0]
            languages[lang] = level

        # Englisch (sehr verbreitet in der Schweiz)
        english_level = random.choices(
            ["Grundkenntnisse", "Gute Kenntnisse", "Sehr gute Kenntnisse", "Verhandlungssicher"],
            weights=[15, 35, 35, 15],
            k=1
        )[0]
        languages["english"] = english_level

        # Berufsspezifische Fähigkeiten
        sector_skills_map = {
            "commercial_administrative": [
                "MS Office", "SAP", "Projektmanagement", "Buchhaltung", 
                "Personalwesen", "Marketing", "Kundenbetreuung"
            ],
            "healthcare_social": [
                "Patientenbetreuung", "Medizinische Dokumentation", 
                "Qualitätsmanagement", "Erste Hilfe", "Pflegeplanung"
            ],
            "technical_engineering": [
                "CAD", "Projektmanagement", "Qualitätssicherung", 
                "Programmierung", "Technische Dokumentation"
            ],
            "finance_banking": [
                "Financial Analysis", "Risk Management", "Compliance", 
                "Bloomberg Terminal", "Kundenberatung"
            ],
            "construction": [
                "Bauleitung", "Arbeitssicherheit", "Kostenkalkulation", 
                "Baurecht", "Projektmanagement"
            ],
            "hospitality_tourism": [
                "Kundenservice", "Eventorganisation", "Fremdsprachen", 
                "Reservationssysteme", "Gastronomie"
            ],
            "education": [
                "Didaktik", "Curriculum Development", "Klassenführung", 
                "Pädagogische Diagnostik", "E-Learning"
            ],
            "retail_sales": [
                "Verkaufstechniken", "Warenwirtschaft", "Visual Merchandising", 
                "Kundenberatung", "Kassensysteme"
            ]
        }

        sector_skills = sector_skills_map.get(persona.sector, ["Teamwork", "Kommunikation"])
        professional_skills = random.sample(
            sector_skills,
            k=min(4, len(sector_skills))
        )

        # IT-Kenntnisse
        it_skills = random.sample([
            "MS Office", "E-Mail", "Internet", "Datenbanken", 
            "Social Media", "ERP-Systeme", "CRM-Systeme"
        ], k=random.randint(2, 4))

        return Skills(
            languages=languages,
            professional_skills=professional_skills,
            it_skills=it_skills
        )

    def _generate_hobbies(self) -> List[str]:
        """Generiert typische Schweizer Hobbies"""
        swiss_hobbies = [
            "Wandern", "Skifahren", "Snowboarden", "Lesen", "Reisen", 
            "Kochen", "Sport", "Musik", "Fotografie", "Gärtnern", 
            "Radfahren", "Schwimmen", "Vereinstätigkeit", "Tennis", 
            "Joggen", "Kultur", "Theater", "Kino", "Bergsport"
        ]

        return random.sample(swiss_hobbies, k=random.randint(2, 4))

    def generate_batch(self, count: int) -> List[CV]:
        """Generiert mehrere CVs auf einmal"""
        return [self.generate_cv() for _ in range(count)]

"""
Datenmodelle für den Swiss CV Generator
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class LanguageRegion(str, Enum):
    DEUTSCHSCHWEIZ = "deutschschweiz"
    ROMANDIE = "romandie"
    TICINO = "ticino"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class EducationLevel(str, Enum):
    OBLIGATORISCH = "Obligatorische Schulzeit"
    BERUFSLEHRE = "Berufliche Grundbildung"
    GYMNASIUM = "Gymnasium"
    FACHHOCHSCHULE = "Fachhochschule"
    UNIVERSITAET = "Universitätsstudium"
    HOEHERE_BERUFSBILDUNG = "Höhere Berufsbildung"


class PersonalInfo(BaseModel):
    """Persönliche Informationen einer Person"""
    first_name: str
    last_name: str
    age: int = Field(..., ge=16, le=70)
    birth_year: int
    gender: Gender
    language_region: LanguageRegion
    primary_language: str
    canton: str
    city: str

    @validator('birth_year')
    def validate_birth_year(cls, v, values):
        current_year = datetime.now().year
        expected_birth_year = current_year - values.get('age', 0)
        if abs(v - expected_birth_year) > 1:
            raise ValueError('Birth year must match age')
        return v


class Education(BaseModel):
    """Bildungseintrag"""
    level: EducationLevel
    institution: str
    start_year: int
    end_year: int
    qualification: str
    field_of_study: Optional[str] = None

    @validator('end_year')
    def validate_end_year(cls, v, values):
        start_year = values.get('start_year')
        if start_year and v <= start_year:
            raise ValueError('End year must be after start year')
        return v

    @property
    def duration_years(self) -> int:
        return self.end_year - self.start_year


class Career(BaseModel):
    """Berufseintrag"""
    position: str
    company: str
    location: str
    start_year: int
    end_year: Optional[int] = None
    duration_years: int
    employment_type: str = "Festanstellung"
    workload: str = "100%"
    responsibilities: Optional[List[str]] = None

    @property
    def is_current(self) -> bool:
        return self.end_year is None

    @validator('duration_years')
    def validate_duration(cls, v, values):
        start_year = values.get('start_year')
        end_year = values.get('end_year')
        if end_year and start_year:
            expected_duration = end_year - start_year
            if abs(v - expected_duration) > 1:
                raise ValueError('Duration must match start/end years')
        return v


class Skills(BaseModel):
    """Fähigkeiten und Kompetenzen"""
    languages: Dict[str, str] = Field(default_factory=dict)
    professional_skills: List[str] = Field(default_factory=list)
    it_skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


class Persona(BaseModel):
    """Persona mit allen Grunddaten"""
    personal: PersonalInfo
    sector: str
    sector_data: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


class CV(BaseModel):
    """Vollständiger Lebenslauf"""
    cv_id: str
    persona: Persona
    education: List[Education]
    career: List[Career]
    skills: Skills
    hobbies: List[str] = Field(default_factory=list)
    generated_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

    @property
    def total_experience_years(self) -> int:
        """Gesamte Berufserfahrung in Jahren"""
        return sum(pos.duration_years for pos in self.career)

    @property
    def current_position(self) -> Optional[str]:
        """Aktuelle Position"""
        current_jobs = [pos for pos in self.career if pos.is_current]
        return current_jobs[0].position if current_jobs else None

    @property
    def education_level(self) -> str:
        """Höchster Bildungsabschluss"""
        if not self.education:
            return "Keine Angabe"

        # Sortiere nach Bildungslevel-Priorität
        level_priority = {
            EducationLevel.UNIVERSITAET: 6,
            EducationLevel.FACHHOCHSCHULE: 5,
            EducationLevel.HOEHERE_BERUFSBILDUNG: 4,
            EducationLevel.GYMNASIUM: 3,
            EducationLevel.BERUFSLEHRE: 2,
            EducationLevel.OBLIGATORISCH: 1
        }

        highest = max(self.education, key=lambda x: level_priority.get(x.level, 0))
        return highest.level.value

    def to_dict(self) -> Dict[str, Any]:
        """Konvertiere zu Dictionary für Export"""
        return {
            "cv_id": self.cv_id,
            "first_name": self.persona.personal.first_name,
            "last_name": self.persona.personal.last_name,
            "age": self.persona.personal.age,
            "gender": self.persona.personal.gender.value,
            "canton": self.persona.personal.canton,
            "city": self.persona.personal.city,
            "language_region": self.persona.personal.language_region.value,
            "sector": self.persona.sector,
            "education_level": self.education_level,
            "total_experience": self.total_experience_years,
            "current_position": self.current_position,
            "languages": list(self.skills.languages.keys()),
            "generated_date": self.generated_date.isoformat()
        }

    def to_formatted_text(self) -> str:
        """Formatiere als lesbaren Text"""
        lines = []
        lines.append("=" * 60)
        lines.append("SYNTHETISCHER LEBENSLAUF")
        lines.append("=" * 60)
        lines.append("")

        # Persönliche Daten
        p = self.persona.personal
        lines.append("PERSÖNLICHE ANGABEN")
        lines.append("-" * 20)
        lines.append(f"Name: {p.first_name} {p.last_name}")
        lines.append(f"Alter: {p.age} Jahre ({p.birth_year})")
        lines.append(f"Wohnort: {p.city}, {p.canton}")
        lines.append(f"Sprachregion: {p.language_region.value}")
        lines.append("")

        # Bildung
        lines.append("AUSBILDUNG")
        lines.append("-" * 10)
        for edu in self.education:
            lines.append(f"{edu.start_year}-{edu.end_year}: {edu.level.value}")
            lines.append(f"  {edu.institution}")
            lines.append(f"  {edu.qualification}")
            lines.append("")

        # Beruflicher Werdegang
        lines.append("BERUFLICHER WERDEGANG")
        lines.append("-" * 22)
        for career in self.career:
            end_year = career.end_year if career.end_year else "heute"
            lines.append(f"{career.start_year}-{end_year}: {career.position}")
            lines.append(f"  {career.company}, {career.location}")
            lines.append(f"  {career.employment_type}, {career.workload}")
            lines.append("")

        # Sprachen
        lines.append("SPRACHKENNTNISSE")
        lines.append("-" * 16)
        for lang, level in self.skills.languages.items():
            lines.append(f"  {lang.capitalize()}: {level}")
        lines.append("")

        return "\n".join(lines)

"""
Unit Tests für den Swiss CV Generator
"""

import pytest
import random
from datetime import datetime

from swiss_cv_generator.core.persona_generator import SwissPersonaGenerator
from swiss_cv_generator.core.cv_generator import SwissCVGenerator
from swiss_cv_generator.utils.validators import StatisticsValidator
from swiss_cv_generator.utils.exporters import BatchGenerator
from swiss_cv_generator.data_models import Gender, LanguageRegion


class TestSwissPersonaGenerator:
    """Tests für die Persona-Generierung"""

    def setup_method(self):
        """Setup für jeden Test"""
        self.generator = SwissPersonaGenerator(random_seed=42)

    def test_generate_persona(self):
        """Test basic persona generation"""
        persona = self.generator.generate_persona()

        assert persona.personal.first_name
        assert persona.personal.last_name
        assert 22 <= persona.personal.age <= 65
        assert persona.personal.birth_year > 1950
        assert persona.personal.gender in [Gender.MALE, Gender.FEMALE]
        assert persona.personal.language_region in [
            LanguageRegion.DEUTSCHSCHWEIZ, 
            LanguageRegion.ROMANDIE, 
            LanguageRegion.TICINO
        ]
        assert persona.sector
        assert persona.sector_data

    def test_age_distribution(self):
        """Test dass Altersverteilung realistisch ist"""
        personas = [self.generator.generate_persona() for _ in range(100)]
        ages = [p.personal.age for p in personas]

        assert min(ages) >= 22
        assert max(ages) <= 65
        assert 35 <= sum(ages) / len(ages) <= 55  # Durchschnittsalter im realistischen Bereich

    def test_regional_distribution(self):
        """Test Sprachregionen-Verteilung"""
        personas = [self.generator.generate_persona() for _ in range(1000)]

        deutsch_count = sum(1 for p in personas if p.personal.language_region == LanguageRegion.DEUTSCHSCHWEIZ)
        romandie_count = sum(1 for p in personas if p.personal.language_region == LanguageRegion.ROMANDIE)
        ticino_count = sum(1 for p in personas if p.personal.language_region == LanguageRegion.TICINO)

        # Sollte grob den Schweizer Verteilungen entsprechen
        assert deutsch_count > romandie_count > ticino_count
        assert deutsch_count / len(personas) > 0.5  # Deutschschweiz ist Mehrheit

    def test_gender_distribution(self):
        """Test Geschlechterverteilung"""
        personas = [self.generator.generate_persona() for _ in range(1000)]

        male_count = sum(1 for p in personas if p.personal.gender == Gender.MALE)
        female_count = len(personas) - male_count

        # Sollte relativ ausgeglichen sein
        assert 0.4 <= male_count / len(personas) <= 0.6
        assert 0.4 <= female_count / len(personas) <= 0.6


class TestSwissCVGenerator:
    """Tests für die CV-Generierung"""

    def setup_method(self):
        """Setup für jeden Test"""
        self.generator = SwissCVGenerator(random_seed=42)

    def test_generate_cv(self):
        """Test basic CV generation"""
        cv = self.generator.generate_cv()

        assert cv.cv_id
        assert cv.persona
        assert cv.education
        assert cv.skills
        assert cv.generated_date

        # Mindestens obligatorische Schulzeit
        assert len(cv.education) >= 1

        # Sprachen sollten immer vorhanden sein
        assert len(cv.skills.languages) >= 1

    def test_education_coherence(self):
        """Test dass Bildungsweg zeitlich kohärent ist"""
        cv = self.generator.generate_cv()

        # Bildungseinträge sollten chronologisch sein
        for i in range(len(cv.education) - 1):
            current = cv.education[i]
            next_edu = cv.education[i + 1]

            assert current.end_year <= next_edu.start_year
            assert current.start_year < current.end_year

    def test_career_coherence(self):
        """Test dass Karriere zeitlich kohärent ist"""
        cv = self.generator.generate_cv()

        if len(cv.career) > 1:
            # Karriereeinträge sollten chronologisch sein
            for i in range(len(cv.career) - 1):
                current = cv.career[i]
                next_career = cv.career[i + 1]

                if current.end_year and next_career.start_year:
                    assert current.end_year <= next_career.start_year

    def test_age_experience_correlation(self):
        """Test dass Alter und Berufserfahrung korrelieren"""
        cvs = [self.generator.generate_cv() for _ in range(50)]

        for cv in cvs:
            age = cv.persona.personal.age
            experience = cv.total_experience_years

            # Berufserfahrung sollte nicht länger als Alter minus ~18 Jahre sein
            max_possible_experience = age - 18
            assert experience <= max_possible_experience + 2  # +2 für Toleranz

    def test_language_skills(self):
        """Test Sprachkenntnisse basierend auf Region"""
        cv = self.generator.generate_cv()
        languages = cv.skills.languages

        region = cv.persona.personal.language_region
        primary_lang = cv.persona.personal.primary_language

        # Primärsprache sollte als Muttersprache vorhanden sein
        assert primary_lang in languages
        assert languages[primary_lang] == "Muttersprache"

        # Englisch sollte fast immer vorhanden sein
        assert "english" in languages


class TestStatisticsValidator:
    """Tests für die Statistik-Validierung"""

    def setup_method(self):
        """Setup für jeden Test"""
        self.generator = SwissCVGenerator(random_seed=42)

    def test_validate_empty_list(self):
        """Test Validierung mit leerer Liste"""
        result = StatisticsValidator.validate_cvs([])
        assert "error" in result

    def test_validate_small_batch(self):
        """Test Validierung mit kleiner Batch"""
        cvs = [self.generator.generate_cv() for _ in range(10)]
        result = StatisticsValidator.validate_cvs(cvs)

        assert result["total_cvs"] == 10
        assert "validations" in result
        assert "summary" in result
        assert result["summary"]["total_validations"] > 0

    def test_validation_structure(self):
        """Test Struktur des Validierungsberichts"""
        cvs = [self.generator.generate_cv() for _ in range(50)]
        result = StatisticsValidator.validate_cvs(cvs)

        # Prüfe erwartete Validierungen
        expected_validations = ["gender", "regions", "education", "sectors", "age"]
        for validation in expected_validations:
            assert validation in result["validations"]
            assert "status" in result["validations"][validation]

    def test_generate_report(self):
        """Test Generierung des formatierten Berichts"""
        cvs = [self.generator.generate_cv() for _ in range(20)]
        report = StatisticsValidator.generate_validation_report(cvs)

        assert isinstance(report, str)
        assert "VALIDIERUNGSBERICHT" in report
        assert "ZUSAMMENFASSUNG" in report


class TestBatchGenerator:
    """Tests für Batch-Generierung und Export"""

    def setup_method(self):
        """Setup für jeden Test"""
        self.cv_generator = SwissCVGenerator(random_seed=42)
        self.batch_generator = BatchGenerator(self.cv_generator)

    def test_generate_batch(self):
        """Test Batch-Generierung"""
        batch_size = 25
        cvs = self.batch_generator.generate_batch(batch_size)

        assert len(cvs) == batch_size
        assert all(cv.cv_id for cv in cvs)

        # Alle CV-IDs sollten einzigartig sein
        cv_ids = [cv.cv_id for cv in cvs]
        assert len(set(cv_ids)) == len(cv_ids)

    def test_export_csv(self):
        """Test CSV-Export"""
        cvs = self.batch_generator.generate_batch(5)

        # Temporäre Datei für Test
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name

        try:
            result = self.batch_generator.export_csv(cvs, temp_filename)
            assert "Erfolgreich" in result
            assert os.path.exists(temp_filename)

            # Prüfe CSV-Inhalt
            import pandas as pd
            df = pd.read_csv(temp_filename)
            assert len(df) == 5
            assert "cv_id" in df.columns
            assert "first_name" in df.columns

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


# Integration Test
def test_full_workflow():
    """Integration Test für kompletten Workflow"""
    # Generator initialisieren
    generator = SwissCVGenerator(random_seed=123)
    batch_generator = BatchGenerator(generator)

    # Batch generieren
    cvs = batch_generator.generate_batch(100)
    assert len(cvs) == 100

    # Validieren
    validation = StatisticsValidator.validate_cvs(cvs)
    assert validation["total_cvs"] == 100
    assert validation["summary"]["total_validations"] > 0

    # Report generieren
    report = StatisticsValidator.generate_validation_report(cvs)
    assert len(report) > 100  # Report sollte substantiell sein

    print("✅ Integration Test erfolgreich!")


if __name__ == "__main__":
    # Führe Integration Test aus wenn direkt gestartet
    test_full_workflow()

"""
Validatoren für Schweizer Arbeitsmarktstatistiken
"""

from typing import List, Dict, Any
import pandas as pd
from ..data_models import CV, Persona
from ..data.statistics import SWISS_LABOR_STATISTICS, OCCUPATIONAL_SECTORS


class StatisticsValidator:
    """Validiert generierte Daten gegen Schweizer Arbeitsmarktstatistiken"""

    @staticmethod
    def validate_cvs(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert eine Liste von CVs gegen bekannte Statistiken"""
        if not cvs:
            return {"error": "Keine CVs zum Validieren"}

        total = len(cvs)
        validation_report = {
            "total_cvs": total,
            "validations": {},
            "summary": {}
        }

        # Geschlechterverteilung validieren
        gender_validation = StatisticsValidator._validate_gender_distribution(cvs)
        validation_report["validations"]["gender"] = gender_validation

        # Sprachregionen validieren
        region_validation = StatisticsValidator._validate_language_regions(cvs)
        validation_report["validations"]["regions"] = region_validation

        # Bildungswege validieren
        education_validation = StatisticsValidator._validate_education_paths(cvs)
        validation_report["validations"]["education"] = education_validation

        # Berufssektoren validieren
        sector_validation = StatisticsValidator._validate_sectors(cvs)
        validation_report["validations"]["sectors"] = sector_validation

        # Altersverteilung validieren
        age_validation = StatisticsValidator._validate_age_distribution(cvs)
        validation_report["validations"]["age"] = age_validation

        # Gesamtbewertung
        validation_report["summary"] = StatisticsValidator._generate_summary(validation_report)

        return validation_report

    @staticmethod
    def _validate_gender_distribution(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert Geschlechterverteilung"""
        total = len(cvs)
        male_count = sum(1 for cv in cvs if cv.persona.personal.gender.value == "male")
        female_count = total - male_count

        actual_male_pct = (male_count / total) * 100
        actual_female_pct = (female_count / total) * 100

        # Schweizer Zielwerte (ca. 52% Männer, 48% Frauen in Erwerbsbevölkerung)
        target_male_pct = 52.0
        target_female_pct = 48.0

        return {
            "metric": "Geschlechterverteilung",
            "actual": {
                "male": {"count": male_count, "percentage": actual_male_pct},
                "female": {"count": female_count, "percentage": actual_female_pct}
            },
            "target": {
                "male": target_male_pct,
                "female": target_female_pct
            },
            "deviation": {
                "male": abs(actual_male_pct - target_male_pct),
                "female": abs(actual_female_pct - target_female_pct)
            },
            "status": "PASS" if abs(actual_male_pct - target_male_pct) < 5.0 else "FAIL"
        }

    @staticmethod
    def _validate_language_regions(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert Sprachregionen-Verteilung"""
        total = len(cvs)
        region_counts = {}

        for region in ["deutschschweiz", "romandie", "ticino"]:
            count = sum(1 for cv in cvs if cv.persona.personal.language_region.value == region)
            region_counts[region] = {
                "count": count,
                "percentage": (count / total) * 100
            }

        # Schweizer Zielwerte
        targets = {
            "deutschschweiz": SWISS_LABOR_STATISTICS["language_regions"]["german_speaking"],
            "romandie": SWISS_LABOR_STATISTICS["language_regions"]["french_speaking"],
            "ticino": SWISS_LABOR_STATISTICS["language_regions"]["italian_speaking"]
        }

        deviations = {}
        max_deviation = 0
        for region in region_counts:
            deviation = abs(region_counts[region]["percentage"] - targets[region])
            deviations[region] = deviation
            max_deviation = max(max_deviation, deviation)

        return {
            "metric": "Sprachregionen",
            "actual": region_counts,
            "target": targets,
            "deviation": deviations,
            "max_deviation": max_deviation,
            "status": "PASS" if max_deviation < 8.0 else "FAIL"
        }

    @staticmethod
    def _validate_education_paths(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert Bildungswege"""
        total = len(cvs)
        education_counts = {
            "Berufslehre": 0,
            "Höhere Berufsbildung": 0,
            "Universitätsabschluss": 0,
            "Obligatorische Schulzeit": 0
        }

        for cv in cvs:
            education_level = cv.education_level
            if "Berufliche Grundbildung" in education_level or "Berufslehre" in education_level:
                education_counts["Berufslehre"] += 1
            elif "Höhere Berufsbildung" in education_level:
                education_counts["Höhere Berufsbildung"] += 1
            elif "Universitätsstudium" in education_level or "Universitätsabschluss" in education_level:
                education_counts["Universitätsabschluss"] += 1
            else:
                education_counts["Obligatorische Schulzeit"] += 1

        # Zu Prozenten konvertieren
        education_percentages = {
            key: (count / total) * 100 
            for key, count in education_counts.items()
        }

        # Schweizer Zielwerte (ca. 64% Berufslehre)
        vocational_pct = education_percentages["Berufslehre"] + education_percentages["Höhere Berufsbildung"]
        target_vocational = 64.0

        return {
            "metric": "Bildungswege",
            "actual": education_percentages,
            "vocational_total": vocational_pct,
            "target_vocational": target_vocational,
            "deviation": abs(vocational_pct - target_vocational),
            "status": "PASS" if abs(vocational_pct - target_vocational) < 10.0 else "FAIL"
        }

    @staticmethod
    def _validate_sectors(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert Berufssektoren"""
        total = len(cvs)
        sector_counts = {}

        for sector in OCCUPATIONAL_SECTORS.keys():
            count = sum(1 for cv in cvs if cv.persona.sector == sector)
            sector_counts[sector] = {
                "count": count,
                "percentage": (count / total) * 100
            }

        # Vergleiche mit Zielwerten
        targets = {sector: data["percentage"] for sector, data in OCCUPATIONAL_SECTORS.items()}

        deviations = {}
        total_coverage = 0
        for sector in sector_counts:
            deviation = abs(sector_counts[sector]["percentage"] - targets[sector])
            deviations[sector] = deviation
            total_coverage += sector_counts[sector]["percentage"]

        return {
            "metric": "Berufssektoren",
            "actual": sector_counts,
            "target": targets,
            "deviation": deviations,
            "total_coverage": total_coverage,
            "status": "PASS" if total_coverage > 70.0 else "FAIL"
        }

    @staticmethod
    def _validate_age_distribution(cvs: List[CV]) -> Dict[str, Any]:
        """Validiert Altersverteilung"""
        ages = [cv.persona.personal.age for cv in cvs]

        if not ages:
            return {"error": "Keine Altersangaben gefunden"}

        mean_age = sum(ages) / len(ages)
        median_age = sorted(ages)[len(ages) // 2]
        min_age = min(ages)
        max_age = max(ages)

        # Schweizer Erwerbsbevölkerung: typischerweise 25-64 Jahre, Durchschnitt ~44
        target_mean = 44.0
        target_min = 22
        target_max = 65

        return {
            "metric": "Altersverteilung",
            "actual": {
                "mean": mean_age,
                "median": median_age,
                "min": min_age,
                "max": max_age,
                "range": max_age - min_age
            },
            "target": {
                "mean": target_mean,
                "min": target_min,
                "max": target_max
            },
            "deviation": abs(mean_age - target_mean),
            "status": "PASS" if (target_min <= min_age <= target_min + 5 and 
                              target_max - 5 <= max_age <= target_max and
                              abs(mean_age - target_mean) < 5.0) else "FAIL"
        }

    @staticmethod
    def _generate_summary(validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert Zusammenfassung der Validierung"""
        validations = validation_report["validations"]

        passed = sum(1 for v in validations.values() if v.get("status") == "PASS")
        total_validations = len(validations)

        return {
            "total_validations": total_validations,
            "passed": passed,
            "failed": total_validations - passed,
            "pass_rate": (passed / total_validations) * 100 if total_validations > 0 else 0,
            "overall_status": "PASS" if passed >= total_validations * 0.8 else "FAIL"
        }

    @staticmethod
    def generate_validation_report(cvs: List[CV]) -> str:
        """Generiert einen formatierten Validierungsbericht"""
        validation = StatisticsValidator.validate_cvs(cvs)

        lines = []
        lines.append("VALIDIERUNGSBERICHT - SYNTHETISCHE LEBENSLÄUFE")
        lines.append("=" * 60)
        lines.append(f"Anzahl CVs: {validation['total_cvs']}")
        lines.append("")

        for metric, data in validation["validations"].items():
            lines.append(f"{data['metric'].upper()}")
            lines.append("-" * len(data['metric']))

            if metric == "gender":
                lines.append(f"Männer: {data['actual']['male']['percentage']:.1f}% (Ziel: {data['target']['male']:.1f}%)")
                lines.append(f"Frauen: {data['actual']['female']['percentage']:.1f}% (Ziel: {data['target']['female']:.1f}%)")
                lines.append(f"Status: {data['status']}")

            elif metric == "age":
                lines.append(f"Durchschnittsalter: {data['actual']['mean']:.1f} Jahre")
                lines.append(f"Altersbereich: {data['actual']['min']}-{data['actual']['max']} Jahre")
                lines.append(f"Status: {data['status']}")

            lines.append("")

        # Gesamtfazit
        summary = validation["summary"]
        lines.append("ZUSAMMENFASSUNG")
        lines.append("-" * 14)
        lines.append(f"Validierungen bestanden: {summary['passed']}/{summary['total_validations']}")
        lines.append(f"Erfolgsquote: {summary['pass_rate']:.1f}%")
        lines.append(f"Gesamtstatus: {summary['overall_status']}")

        return "\n".join(lines)

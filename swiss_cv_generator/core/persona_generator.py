"""
Swiss Persona Generator - Generiert demografische Profile basierend auf Schweizer Statistiken
"""

import random
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..data.statistics import SWISS_LABOR_STATISTICS, OCCUPATIONAL_SECTORS, SWISS_CANTONS
from ..data.names import SWISS_NAMES
from ..data_models import PersonalInfo, Persona, Gender, LanguageRegion


class SwissPersonaGenerator:
    """Generiert realistische demografische Profile für Schweizer Arbeitnehmer"""

    def __init__(self, random_seed: Optional[int] = None):
        if random_seed:
            random.seed(random_seed)
        self.current_year = datetime.now().year

    def generate_persona(self) -> Persona:
        """Generiert eine vollständige Persona basierend auf Schweizer Statistiken"""

        # Sprachregion bestimmen (beeinflusst alle anderen Eigenschaften)
        region_weights = [
            SWISS_LABOR_STATISTICS["language_regions"]["german_speaking"],
            SWISS_LABOR_STATISTICS["language_regions"]["french_speaking"], 
            SWISS_LABOR_STATISTICS["language_regions"]["italian_speaking"]
        ]

        region = random.choices(
            [LanguageRegion.DEUTSCHSCHWEIZ, LanguageRegion.ROMANDIE, LanguageRegion.TICINO],
            weights=region_weights,
            k=1
        )[0]

        # Kanton und Stadt aus der gewählten Region
        region_data = SWISS_CANTONS[region.value]
        canton = random.choice(region_data["cantons"])
        city = random.choice(region_data["major_cities"])
        language = region_data["language"]

        # Geschlecht (leicht mehr Männer in der Erwerbsbevölkerung)
        gender = random.choices(
            [Gender.MALE, Gender.FEMALE], 
            weights=[52, 48], 
            k=1
        )[0]

        # Alter basierend auf Erwerbsbevölkerung (22-65 Jahre)
        age = self._generate_realistic_age()
        birth_year = self.current_year - age

        # Namen generieren
        name_data = SWISS_NAMES[language]
        first_name = random.choice(name_data[gender.value])
        last_name = random.choice(name_data["surnames"])

        # Berufssektor bestimmen
        sector_weights = [sector_data["percentage"] for sector_data in OCCUPATIONAL_SECTORS.values()]
        sector = random.choices(
            list(OCCUPATIONAL_SECTORS.keys()),
            weights=sector_weights,
            k=1
        )[0]

        personal_info = PersonalInfo(
            first_name=first_name,
            last_name=last_name,
            age=age,
            birth_year=birth_year,
            gender=gender,
            language_region=region,
            primary_language=language,
            canton=canton,
            city=city
        )

        return Persona(
            personal=personal_info,
            sector=sector,
            sector_data=OCCUPATIONAL_SECTORS[sector]
        )

    def _generate_realistic_age(self) -> int:
        """Generiert ein realistisches Alter basierend auf Schweizer Erwerbsstatistiken"""
        # Gewichtung basierend auf Erwerbsquoten nach Altersgruppen
        age_ranges = [
            (22, 30, 0.8),   # Junge Erwerbstätige
            (31, 45, 1.5),   # Kern-Erwerbsjahre
            (46, 55, 1.3),   # Erfahrene Arbeitskräfte  
            (56, 65, 0.7)    # Ältere Erwerbstätige
        ]

        # Wähle Altersbereich
        ranges, weights = zip(*[(r, w) for r, _, w in age_ranges])
        chosen_range = random.choices(age_ranges, weights=weights, k=1)[0]

        # Wähle spezifisches Alter im Bereich
        return random.randint(chosen_range[0], chosen_range[1])

    def get_regional_education_preferences(self, region: LanguageRegion) -> Dict[str, float]:
        """Gibt regionale Bildungspräferenzen zurück"""
        if region == LanguageRegion.DEUTSCHSCHWEIZ:
            return {
                "vocational": 0.70,     # Höhere Lehrlingsquote
                "academic": 0.30
            }
        else:  # Romandie & Ticino
            return {
                "vocational": 0.55,     # Niedrigere Lehrlingsquote
                "academic": 0.45        # Höhere Gymnasialquote
            }

    def generate_batch(self, count: int) -> List[Persona]:
        """Generiert mehrere Personas auf einmal"""
        return [self.generate_persona() for _ in range(count)]

    def get_statistics_summary(self, personas: List[Persona]) -> Dict[str, Any]:
        """Erstellt Statistik-Zusammenfassung für Validierung"""
        if not personas:
            return {}

        total = len(personas)

        # Geschlechterverteilung
        gender_dist = {}
        for gender in Gender:
            count = sum(1 for p in personas if p.personal.gender == gender)
            gender_dist[gender.value] = {"count": count, "percentage": count/total*100}

        # Sprachregionen
        region_dist = {}
        for region in LanguageRegion:
            count = sum(1 for p in personas if p.personal.language_region == region)
            region_dist[region.value] = {"count": count, "percentage": count/total*100}

        # Altersverteilung
        ages = [p.personal.age for p in personas]
        age_stats = {
            "mean": sum(ages) / len(ages),
            "median": sorted(ages)[len(ages)//2],
            "min": min(ages),
            "max": max(ages)
        }

        # Sektoren
        sector_dist = {}
        for sector in OCCUPATIONAL_SECTORS.keys():
            count = sum(1 for p in personas if p.sector == sector)
            sector_dist[sector] = {"count": count, "percentage": count/total*100}

        return {
            "total_personas": total,
            "gender_distribution": gender_dist,
            "region_distribution": region_dist,
            "age_statistics": age_stats,
            "sector_distribution": sector_dist
        }

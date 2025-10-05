"""
Schweizer Arbeitsmarkt-Statistiken basierend auf BFS-Daten
"""

from typing import Dict, List, Any

# Aktuelle Schweizer Arbeitsmarktstatistiken (Stand 2024)
SWISS_LABOR_STATISTICS = {
    "total_employed": 5361000,  # Q2 2024
    "employment_rate": 80.7,  # 2023
    "sectors": {
        "tertiary_services": 77.8,  # 2024
        "secondary_industry": 20.2,
        "primary_agriculture": 2.0
    },
    "education_pathways": {
        "vocational_training": 64,  # ~64% wählen Berufslehre
        "academic_gymnasium": 25,  # ~25% wählen Gymnasialweg
        "specialized_schools": 4,
        "interim_solutions": 7
    },
    "language_regions": {
        "german_speaking": 62.0,  # Deutschschweiz
        "french_speaking": 22.8,  # Romandie
        "italian_speaking": 8.4,  # Tessin
        "romansh": 0.5,
        "others": 6.3
    },
    "gender_distribution": {
        "male_employment": 84.4,
        "female_employment": 76.8
    },
    "age_groups": {
        "15_24": 61.5,
        "25_54": 87.2,
        "55_64": 73.8
    }
}

# Berufssektoren mit statistischen Gewichtungen
OCCUPATIONAL_SECTORS = {
    "commercial_administrative": {
        "percentage": 13.0,
        "roles": [
            "Kaufmann/-frau", "Sachbearbeiter/in", "Teamleiter/in", 
            "Projektleiter/in", "Buchhalter/in", "HR-Spezialist/in", 
            "Marketingfachperson", "Verkaufsleiter/in"
        ],
        "career_progression": [
            "Sachbearbeiter", "Senior Sachbearbeiter", "Teamleiter", 
            "Abteilungsleiter", "Geschäftsführer"
        ],
        "typical_salaries": {
            "entry": 55000, "mid": 75000, "senior": 95000, "executive": 130000
        }
    },
    "healthcare_social": {
        "percentage": 11.5,
        "roles": [
            "Pflegefachperson", "Arzt/Ärztin", "Physiotherapeut/in", 
            "Sozialarbeiter/in", "Medizinische Praxisassistenz", "Therapeut/in"
        ],
        "career_progression": [
            "Pflegeassistent", "Pflegefachperson", "Stationsleitung", 
            "Pflegedienstleitung"
        ],
        "typical_salaries": {
            "entry": 58000, "mid": 78000, "senior": 98000, "executive": 120000
        }
    },
    "technical_engineering": {
        "percentage": 10.8,
        "roles": [
            "Ingenieur/in", "Techniker/in", "Informatiker/in", 
            "Elektroinstallateur/in", "Maschinenbauingenieur/in", "Bauingenieur/in"
        ],
        "career_progression": [
            "Techniker", "Projektingenieur", "Senior Ingenieur", "Technischer Leiter"
        ],
        "typical_salaries": {
            "entry": 62000, "mid": 85000, "senior": 110000, "executive": 140000
        }
    },
    "hospitality_tourism": {
        "percentage": 8.2,
        "roles": [
            "Hotelfachperson", "Koch/Köchin", "Restaurantfachperson", 
            "Reiseleiter/in", "Eventmanager/in"
        ],
        "career_progression": [
            "Serviceangestellter", "Teamleiter Service", "Restaurantleiter", 
            "Hoteldirektor"
        ],
        "typical_salaries": {
            "entry": 45000, "mid": 58000, "senior": 72000, "executive": 95000
        }
    },
    "construction": {
        "percentage": 7.5,
        "roles": [
            "Maurer/in", "Zimmermann/-frau", "Bauführer/in", 
            "Architekt/in", "Polier/in"
        ],
        "career_progression": [
            "Bauarbeiter", "Vorarbeiter", "Polier", "Bauführer", "Bauleiter"
        ],
        "typical_salaries": {
            "entry": 50000, "mid": 68000, "senior": 85000, "executive": 110000
        }
    },
    "finance_banking": {
        "percentage": 6.8,
        "roles": [
            "Bankkaufmann/-frau", "Finanzanalyst/in", "Kundenberater/in", 
            "Portfolio Manager/in"
        ],
        "career_progression": [
            "Bankberater", "Senior Berater", "Team Manager", "Bereichsleiter"
        ],
        "typical_salaries": {
            "entry": 65000, "mid": 88000, "senior": 120000, "executive": 180000
        }
    },
    "education": {
        "percentage": 6.2,
        "roles": [
            "Primarlehrer/in", "Sekundarlehrer/in", "Dozent/in", "Ausbilder/in"
        ],
        "career_progression": [
            "Klassenlehrer", "Fachlehrer", "Schulleiter", "Bildungsexperte"
        ],
        "typical_salaries": {
            "entry": 72000, "mid": 88000, "senior": 105000, "executive": 125000
        }
    },
    "retail_sales": {
        "percentage": 8.9,
        "roles": [
            "Verkäufer/in", "Filialleiter/in", "Einkäufer/in", 
            "Visual Merchandiser/in"
        ],
        "career_progression": [
            "Verkäufer", "Teamleiter", "Filialleiter", "Regionalleiter"
        ],
        "typical_salaries": {
            "entry": 48000, "mid": 62000, "senior": 78000, "executive": 100000
        }
    }
}

# Kantonale Daten
SWISS_CANTONS = {
    "deutschschweiz": {
        "cantons": [
            "Zürich", "Bern", "Luzern", "St. Gallen", "Aargau", 
            "Basel-Stadt", "Basel-Landschaft", "Thurgau", "Solothurn"
        ],
        "major_cities": [
            "Zürich", "Basel", "Bern", "Luzern", "St. Gallen", "Winterthur"
        ],
        "employment_rate": 68.8,
        "language": "deutsch",
        "apprenticeship_rate": 31.9
    },
    "romandie": {
        "cantons": [
            "Genève", "Vaud", "Neuchâtel", "Jura", "Fribourg", "Valais"
        ],
        "major_cities": [
            "Genève", "Lausanne", "Neuchâtel", "Fribourg", "Sion"
        ],
        "employment_rate": 59.8,
        "language": "français",
        "apprenticeship_rate": 26.3
    },
    "ticino": {
        "cantons": ["Ticino"],
        "major_cities": ["Lugano", "Bellinzona", "Locarno"],
        "employment_rate": 65.2,
        "language": "italiano",
        "apprenticeship_rate": 28.5
    }
}

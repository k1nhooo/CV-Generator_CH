"""
Schweizer Unternehmen nach Größenkategorien
"""

from typing import Dict, List

SWISS_COMPANIES: Dict[str, List[str]] = {
    "large": [
        # Großunternehmen (>250 Mitarbeiter)
        "UBS", "Credit Suisse", "Nestlé", "Novartis", "Roche", 
        "ABB", "Zurich Insurance", "Swiss Re", "Swisscom", 
        "Migros", "Coop", "SBB CFF FFS", "PostFinance",
        "Raiffeisen", "Julius Bär", "Swiss Life", "Baloise",
        "LafargeHolcim", "Adecco", "Kuehne + Nagel",
        "Clariant", "Syngenta", "Barry Callebaut",
        "Implenia", "Flughafen Zürich", "RUAG",
        "Swissport", "Dufry", "Galenica", "Emmi"
    ],
    "medium": [
        # Mittlere Unternehmen (50-250 Mitarbeiter)
        "Sika", "Geberit", "Sonova", "Logitech", "Givaudan",
        "Straumann", "Schindler", "Kardex", "Sulzer",
        "Von Roll", "Rieter", "Burckhardt Compression",
        "Inficon", "Tecan", "u-blox", "Molecular Partners",
        "Bachem", "VAT Group", "SFS Group", "Belimo",
        "Feintool", "Komax", "Mikron", "LEM", "Ypsomed",
        "Zur Rose", "Lonza", "Medartis", "ALSO",
        "Ascom", "Bossard", "Dätwyler", "EMS-Chemie"
    ],
    "small": [
        # Kleinunternehmen (<50 Mitarbeiter)
        "Alpine Solutions AG", "Swiss Consulting GmbH",
        "Alpen Tech Solutions", "Helvetica Services SA",
        "Mountain View Consulting", "Lake Geneva Partners",
        "Rhein Valley Systems", "Jura Innovations AG",
        "Ticino Technologies", "Basel Biotech GmbH",
        "Zürich Analytics SA", "Bern Software Solutions",
        "Luzern Logistics AG", "St. Gallen Services",
        "Swiss Quality Control", "Precision Engineering AG",
        "Mountain Peak Consulting", "Lake Solutions GmbH",
        "Valley Innovations SA", "Summit Technologies",
        "Alpine Consulting Group", "Swiss Excellence AG",
        "Helvetic Solutions GmbH", "Central Swiss Services",
        "Eastern Swiss Technology", "Western Swiss Consulting"
    ]
}

# Sektor-spezifische Unternehmen
SECTOR_COMPANIES: Dict[str, Dict[str, List[str]]] = {
    "finance_banking": {
        "large": ["UBS", "Credit Suisse", "Raiffeisen", "PostFinance", "Julius Bär"],
        "medium": ["Bank Cler", "Hypothekarbank Lenzburg", "Vontobel", "EFG International"],
        "small": ["Alpine Private Banking", "Swiss Wealth Management", "Helvetic Finance"]
    },
    "healthcare_social": {
        "large": ["Novartis", "Roche", "Universitätsspital Zürich", "Inselspital Bern"],
        "medium": ["Hirslanden", "Swiss Medical Network", "Galenica"],
        "small": ["Alpine Medical Center", "Swiss Care Solutions", "Health Plus AG"]
    },
    "technical_engineering": {
        "large": ["ABB", "Sulzer", "Schindler", "Implenia"],
        "medium": ["Sika", "Geberit", "Burckhardt Compression"],
        "small": ["Swiss Engineering Solutions", "Tech Innovation AG", "Precision Systems"]
    },
    "retail_sales": {
        "large": ["Migros", "Coop", "Manor", "Denner"],
        "medium": ["Volg", "Spar", "Landi"],
        "small": ["Local Market AG", "Swiss Retail Solutions", "Village Store GmbH"]
    }
}

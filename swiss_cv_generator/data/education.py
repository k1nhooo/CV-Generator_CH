"""
Schweizer Bildungsinstitutionen nach Sprachregionen und Bildungstypen
"""

from typing import Dict, List

EDUCATION_INSTITUTIONS: Dict[str, Dict[str, List[str]]] = {
    "vocational": {
        "deutschschweiz": [
            "Berufsbildungszentrum Zürich BBZ",
            "Gewerblich-industrielle Berufsfachschule Bern gibb",
            "Berufsfachschule Basel BFS",
            "BWZ Rapperswil",
            "Berufsbildungszentrum Luzern BBZ",
            "Gewerbeschule St. Gallen",
            "Berufsfachschule Aarau",
            "Berufsfachschule Baden",
            "Berufsbildungszentrum Olten",
            "Gewerbeschule Thun",
            "Berufsfachschule Winterthur"
        ],
        "romandie": [
            "Centre de formation professionnelle technique Genève CFPT",
            "École professionnelle commerciale Lausanne EPCL",
            "Centre de formation du Littoral neuchâtelois CFLN",
            "École technique - École des métiers Fribourg EMF",
            "Centre professionnel du Nord vaudois CPNV",
            "École professionnelle artisanale et service Vevey EPAS",
            "Centre de formation professionnelle Berne francophone",
            "École des Arts et Métiers Vevey"
        ],
        "ticino": [
            "Centro professionale trevano CPT",
            "Scuola professionale artigianale e industriale SPAI Lugano",
            "Centro scolastico per le industrie artistiche CSIA",
            "Scuola cantonale di commercio Bellinzona",
            "Centro professionale commerciale Chiasso"
        ]
    },
    "universities": {
        "deutschschweiz": [
            "ETH Zürich",
            "Universität Zürich UZH",
            "Universität Basel",
            "Universität Bern",
            "Universität St. Gallen HSG",
            "Fachhochschule Nordwestschweiz FHNW",
            "Zürcher Hochschule für Angewandte Wissenschaften ZHAW",
            "Berner Fachhochschule BFH",
            "Hochschule Luzern HSLU",
            "OST - Ostschweizer Fachhochschule",
            "Kalaidos Fachhochschule"
        ],
        "romandie": [
            "École polytechnique fédérale de Lausanne EPFL",
            "Université de Genève UNIGE",
            "Université de Lausanne UNIL",
            "HES-SO Haute école spécialisée de Suisse occidentale",
            "Université de Neuchâtel UNINE",
            "Université de Fribourg UNIFR",
            "Haute école de gestion Genève HEG-GE",
            "Haute école d'ingénierie et de gestion Vaud HEIG-VD"
        ],
        "ticino": [
            "Università della Svizzera italiana USI",
            "Scuola universitaria professionale della Svizzera italiana SUPSI",
            "Accademia di architettura Mendrisio",
            "Franklin University Switzerland"
        ]
    },
    "gymnasium": {
        "deutschschweiz": [
            "Kantonsschule Zürich Nord",
            "Gymnasium Neufeld Bern",
            "Gymnasium Liestal",
            "Kantonsschule am Burggraben St. Gallen",
            "Alte Kantonsschule Aarau",
            "Gymnasium Bäumlihof Basel",
            "Kantonsschule Luzern",
            "Gymnasium Thun",
            "Kantonsschule Wil",
            "Gymnasium Leonhard Basel"
        ],
        "romandie": [
            "Collège de Genève",
            "Gymnase de Chamblandes Pully",
            "Lycée cantonal de Porrentruy",
            "Collège Sainte-Croix Fribourg",
            "Gymnase de Burier",
            "Collège de l'Abbaye de Saint-Maurice",
            "Lycée Denis-de-Rougemont Neuchâtel",
            "Gymnase intercantonal de la Broye"
        ],
        "ticino": [
            "Liceo cantonale Lugano",
            "Liceo cantonale Bellinzona",
            "Liceo cantonale Locarno",
            "Liceo cantonale Mendrisio"
        ]
    }
}

# Bildungsabschlüsse nach Niveau
QUALIFICATIONS: Dict[str, List[str]] = {
    "obligatorisch": [
        "Abschluss Sekundarstufe I",
        "Realschulabschluss",
        "Sekundarschulabschluss"
    ],
    "berufslehre": [
        "Eidgenössisches Fähigkeitszeugnis EFZ",
        "Eidgenössisches Berufsattest EBA",
        "Berufsmaturität"
    ],
    "gymnasium": [
        "Maturitätszeugnis",
        "Gymnasiale Maturität",
        "Berufsmaturität"
    ],
    "fachhochschule": [
        "Bachelor of Science FH",
        "Bachelor of Arts FH",
        "Bachelor of Engineering FH",
        "Master of Science FH",
        "Master of Arts FH"
    ],
    "universitaet": [
        "Bachelor of Arts",
        "Bachelor of Science",
        "Master of Arts",
        "Master of Science",
        "Lizentiat",
        "Doktorat PhD"
    ],
    "weiterbildung": [
        "Diplom Höhere Fachschule HF",
        "Eidgenössisches Diplom",
        "CAS Certificate of Advanced Studies",
        "DAS Diploma of Advanced Studies",
        "MAS Master of Advanced Studies",
        "EMBA Executive Master of Business Administration"
    ]
}

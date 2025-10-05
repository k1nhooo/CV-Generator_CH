# Swiss CV Generator

Ein spezialisiertes Python-Paket zur Generierung synthetischer Lebensläufe basierend auf Schweizer Arbeitsmarktstatistiken.

## 🎯 Überblick

Dieses System erstellt realitätsnahe, statistisch plausible Lebensläufe ohne Verwendung realer personenbezogener Daten. Es basiert auf aktuellen Daten des Bundesamts für Statistik (BFS) und berücksichtigt die Komplexität des Schweizer Arbeitsmarkts.

## ✨ Features

- **Statistisch repräsentativ:** Basiert auf BFS-Daten 2024
- **Regional differenziert:** Deutschschweiz, Romandie, Tessin
- **Realistische Karriereverläufe:** Altersgerechte Progression
- **Mehrsprachig:** DE/FR/IT mit realistischen Sprachkenntnissen
- **DSGVO-konform:** Vollständig synthetische Daten
- **Skalierbar:** 1.000-10.000+ CVs in Minuten
- **Multiple Formate:** CSV, JSON, Excel, HTML, Markdown

## 🚀 Installation

```bash
# Aus PyPI (wenn publiziert)
pip install swiss-cv-generator

# Oder Development-Installation
git clone <repository>
cd swiss-cv-generator
pip install -e .[dev]
```

## 📋 Abhängigkeiten

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.20.0
- pydantic >= 1.10.0
- click >= 8.0.0

## 🏃‍♂️ Schnellstart

### Python API

```python
from swiss_cv_generator import SwissCVGenerator, BatchGenerator

# Einzelnen CV generieren
generator = SwissCVGenerator()
cv = generator.generate_cv()

print(f"CV für {cv.persona.personal.first_name} {cv.persona.personal.last_name}")
print(f"Alter: {cv.persona.personal.age}, Sektor: {cv.persona.sector}")
print(f"Berufserfahrung: {cv.total_experience_years} Jahre")

# Batch generieren
batch = BatchGenerator(generator)
cvs = batch.generate_batch(1000)
batch.export_csv(cvs, "swiss_cvs.csv")
```

### Command Line Interface

```bash
# Einzelnen CV generieren
swiss-cv-gen single --output cv.json --format json

# Batch generieren
swiss-cv-gen batch --count 1000 --format csv --output batch_cvs

# Daten validieren
swiss-cv-gen validate existing_data.csv

# Informationen anzeigen
swiss-cv-gen info
```

## 📊 Datenqualität

Das System generiert Daten, die folgenden Schweizer Statistiken entsprechen:

- **Geschlechterverteilung:** ~52% männlich, ~48% weiblich
- **Sprachregionen:** 62% Deutschschweiz, 23% Romandie, 8% Tessin
- **Bildungswege:** ~64% Berufslehre, ~25% Gymnasium
- **Berufssektoren:** Basiert auf BFS-Sektorverteilung
- **Altersstruktur:** Realistische Erwerbsbevölkerung 22-65 Jahre

## 🏗️ Projektstruktur

```
swiss_cv_generator/
├── core/                   # Kern-Generatoren
│   ├── persona_generator.py
│   └── cv_generator.py
├── data/                   # Statistische Daten
│   ├── statistics.py
│   ├── names.py
│   ├── companies.py
│   └── education.py
├── utils/                  # Utilities
│   ├── validators.py
│   ├── exporters.py
│   └── formatters.py
├── config/                 # Konfiguration
│   └── settings.py
└── data_models.py          # Pydantic Models

examples/                   # Beispiele
├── generate_sample_cvs.py
├── batch_generation.py
└── statistical_analysis.py

tests/                      # Unit Tests
└── test_*.py
```

## 🧪 Testing

```bash
# Tests ausführen
pytest

# Mit Coverage
pytest --cov=swiss_cv_generator

# Spezifische Tests
pytest tests/test_persona_generator.py
```

## 📈 Verwendungsmöglichkeiten

### HR & Recruiting
- Testing von Bewerbermanagementsystemen
- Schulung von HR-Personal
- A/B-Testing von Recruitingprozessen

### KI & Machine Learning
- Training von CV-Parsing-Algorithmen
- Bias-Reduktion in AI-Recruiting
- Entwicklung von Matching-Systemen

### Forschung & Analyse
- Demografische Studien
- Arbeitsmarktanalysen
- Bildungsstatistiken

## ⚖️ Datenschutz & Compliance

- **Vollständig synthetisch:** Keine realen Personendaten
- **DSGVO-konform:** Kein Personenbezug möglich
- **Reproduzierbar:** Seeds für konsistente Ergebnisse
- **Transparent:** Open Source Algorithmus

## 🔧 Erweiterte Konfiguration

```python
from swiss_cv_generator import SwissCVGenerator

# Mit benutzerdefinierten Parametern
generator = SwissCVGenerator(
    random_seed=42,          # Für reproduzierbare Ergebnisse
    # Weitere Konfigurationen möglich
)

# Regionale Präferenzen anpassen
persona = generator.persona_generator.generate_persona()
education_prefs = generator.persona_generator.get_regional_education_preferences(
    persona.personal.language_region
)
```

## 📝 Beispiele

Siehe `examples/` Verzeichnis für detaillierte Beispiele:

- `generate_sample_cvs.py`: Einfache CV-Generierung
- `batch_generation.py`: Große Batches mit Performance-Monitoring
- `statistical_analysis.py`: Datenvalidierung und Analyse

## 🤝 Contributing

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Committe deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagung

- Bundesamt für Statistik (BFS) für öffentliche Arbeitsmarktdaten
- Schweizer Bildungssystem für strukturierte Bildungswege
- Open Source Community für verwendete Libraries

## 📞 Support

- **Issues:** GitHub Issues für Bugs und Feature Requests
- **Dokumentation:** Siehe `docs/` Verzeichnis
- **Beispiele:** `examples/` Verzeichnis

---

**Swiss CV Generator v1.0.0** - Synthetische Lebensläufe für den Schweizer Arbeitsmarkt

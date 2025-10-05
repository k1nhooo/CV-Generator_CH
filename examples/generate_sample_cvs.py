#!/usr/bin/env python3
"""
Einfaches Beispiel für die Generierung von synthetischen Schweizer CVs
"""

from swiss_cv_generator import SwissCVGenerator, BatchGenerator
from swiss_cv_generator.utils.validators import StatisticsValidator
from swiss_cv_generator.utils.exporters import CVFormatter


def main():
    print("Swiss CV Generator - Einfaches Beispiel")
    print("=" * 50)

    # Generator initialisieren
    generator = SwissCVGenerator(random_seed=42)  # Seed für reproduzierbare Ergebnisse

    # Einzelnen CV generieren
    print("\n1. Einzelnen CV generieren...")
    cv = generator.generate_cv()

    print(f"✓ CV generiert für: {cv.persona.personal.first_name} {cv.persona.personal.last_name}")
    print(f"  Alter: {cv.persona.personal.age}, Sektor: {cv.persona.sector}")
    print(f"  Berufserfahrung: {cv.total_experience_years} Jahre")
    print(f"  Aktuelle Position: {cv.current_position}")

    # CV formatiert ausgeben
    print("\n2. Formatierter CV:")
    print("-" * 30)
    formatted_cv = CVFormatter.to_formatted_text(cv)
    print(formatted_cv[:500] + "..." if len(formatted_cv) > 500 else formatted_cv)

    # Batch generieren
    print("\n3. Batch von 50 CVs generieren...")
    batch_generator = BatchGenerator(generator)
    cvs = batch_generator.generate_batch(50)

    print(f"✓ {len(cvs)} CVs generiert")

    # Statistiken validieren
    print("\n4. Statistiken validieren...")
    validation_report = StatisticsValidator.generate_validation_report(cvs)
    print(validation_report)

    # Als CSV exportieren
    print("\n5. Export als CSV...")
    try:
        export_result = batch_generator.export_csv(cvs, "beispiel_cvs.csv")
        print(f"✓ {export_result}")
    except Exception as e:
        print(f"❌ Export-Fehler: {e}")

    print("\n" + "=" * 50)
    print("Beispiel abgeschlossen!")


if __name__ == "__main__":
    main()

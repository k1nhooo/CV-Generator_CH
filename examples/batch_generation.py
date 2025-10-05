#!/usr/bin/env python3
"""
Erweiterte Batch-Generierung mit verschiedenen Export-Formaten
"""

import argparse
from datetime import datetime
from swiss_cv_generator import SwissCVGenerator
from swiss_cv_generator.utils.exporters import BatchGenerator
from swiss_cv_generator.utils.validators import StatisticsValidator


def generate_large_batch(count: int, output_prefix: str = "swiss_cvs"):
    """Generiert große Batch von CVs mit verschiedenen Export-Formaten"""

    print(f"Swiss CV Generator - Batch-Generierung ({count} CVs)")
    print("=" * 60)

    # Generator mit Zeitstempel als Seed für Einzigartigkeit
    seed = int(datetime.now().timestamp())
    generator = SwissCVGenerator(random_seed=seed)
    batch_generator = BatchGenerator(generator)

    print(f"\n🎲 Random Seed: {seed}")
    print(f"📊 Ziel-Anzahl CVs: {count}")

    # Batch generieren
    print("\n1. CVs generieren...")
    start_time = datetime.now()

    # Für sehr große Batches: in Chunks generieren
    chunk_size = min(1000, count)
    all_cvs = []

    for i in range(0, count, chunk_size):
        chunk_count = min(chunk_size, count - i)
        print(f"   Chunk {i//chunk_size + 1}: {chunk_count} CVs...")

        chunk_cvs = batch_generator.generate_batch(chunk_count)
        all_cvs.extend(chunk_cvs)

    generation_time = datetime.now() - start_time
    print(f"✓ {len(all_cvs)} CVs generiert in {generation_time.total_seconds():.1f} Sekunden")
    print(f"  ({len(all_cvs)/generation_time.total_seconds():.1f} CVs/Sekunde)")

    # Statistiken validieren
    print("\n2. Datenqualität validieren...")
    validation = StatisticsValidator.validate_cvs(all_cvs)

    passed_validations = validation["summary"]["passed"]
    total_validations = validation["summary"]["total_validations"]
    pass_rate = validation["summary"]["pass_rate"]

    print(f"✓ Validierungen: {passed_validations}/{total_validations} bestanden ({pass_rate:.1f}%)")
    print(f"  Status: {validation['summary']['overall_status']}")

    # Detaillierte Statistiken
    print("\n3. Datenverteilung:")
    print("   Geschlecht:")
    gender_data = validation["validations"]["gender"]["actual"]
    print(f"     Männlich: {gender_data['male']['count']} ({gender_data['male']['percentage']:.1f}%)")
    print(f"     Weiblich: {gender_data['female']['count']} ({gender_data['female']['percentage']:.1f}%)")

    print("   Sprachregionen:")
    region_data = validation["validations"]["regions"]["actual"]
    for region, data in region_data.items():
        print(f"     {region.capitalize()}: {data['count']} ({data['percentage']:.1f}%)")

    # Export in verschiedene Formate
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n4. Export...")
    try:
        # CSV Export
        csv_filename = f"{output_prefix}_{timestamp}.csv"
        batch_generator.export_csv(all_cvs, csv_filename)
        print(f"✓ CSV: {csv_filename}")

        # JSON Export
        json_filename = f"{output_prefix}_{timestamp}.json"
        batch_generator.export_json(all_cvs, json_filename)
        print(f"✓ JSON: {json_filename}")

        # Excel Export (nur für kleinere Batches wegen Performance)
        if count <= 5000:
            excel_filename = f"{output_prefix}_{timestamp}.xlsx"
            batch_generator.export_excel(all_cvs, excel_filename)
            print(f"✓ Excel: {excel_filename}")

        # Validierungsbericht speichern
        report_filename = f"validation_report_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(StatisticsValidator.generate_validation_report(all_cvs))
        print(f"✓ Validierungsbericht: {report_filename}")

    except Exception as e:
        print(f"❌ Export-Fehler: {e}")

    total_time = datetime.now() - start_time
    print(f"\n🏁 Gesamt-Laufzeit: {total_time.total_seconds():.1f} Sekunden")
    print("   Erfolgreich abgeschlossen!")

    return all_cvs


def main():
    parser = argparse.ArgumentParser(description="Swiss CV Generator - Batch-Generierung")
    parser.add_argument("--count", type=int, default=1000, 
                       help="Anzahl CVs zu generieren (Standard: 1000)")
    parser.add_argument("--output", type=str, default="swiss_cvs",
                       help="Output-Datei Präfix (Standard: swiss_cvs)")

    args = parser.parse_args()

    if args.count <= 0:
        print("❌ Fehler: Anzahl muss größer als 0 sein")
        return

    if args.count > 50000:
        response = input(f"⚠️  Warnung: {args.count} CVs können lange dauern. Fortfahren? (j/N): ")
        if response.lower() not in ['j', 'ja', 'yes', 'y']:
            print("Abgebrochen.")
            return

    generate_large_batch(args.count, args.output)


if __name__ == "__main__":
    main()

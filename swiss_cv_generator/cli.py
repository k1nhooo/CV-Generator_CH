#!/usr/bin/env python3
"""
Command Line Interface für den Swiss CV Generator
"""

import click
import json
from datetime import datetime
from pathlib import Path

from swiss_cv_generator import SwissCVGenerator
from swiss_cv_generator.utils.exporters import BatchGenerator, CVFormatter
from swiss_cv_generator.utils.validators import StatisticsValidator


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Swiss CV Generator - Synthetische Lebensläufe für den Schweizer Arbeitsmarkt"""
    pass


@cli.command()
@click.option("--output", "-o", default="cv.json", help="Output-Datei")
@click.option("--format", "-f", type=click.Choice(["json", "text", "html", "markdown"]), 
              default="json", help="Output-Format")
@click.option("--seed", type=int, help="Random Seed für reproduzierbare Ergebnisse")
def single(output, format, seed):
    """Generiert einen einzelnen synthetischen CV"""

    click.echo("🇨🇭 Swiss CV Generator - Einzelner CV")
    click.echo("=" * 40)

    generator = SwissCVGenerator(random_seed=seed)
    cv = generator.generate_cv()

    persona = cv.persona.personal
    click.echo(f"✓ CV generiert für: {persona.first_name} {persona.last_name}")
    click.echo(f"  Alter: {persona.age}, Region: {persona.language_region.value}")
    click.echo(f"  Sektor: {cv.persona.sector}")
    click.echo(f"  Berufserfahrung: {cv.total_experience_years} Jahre")

    # Output in gewähltem Format
    if format == "json":
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(cv.dict(), f, indent=2, ensure_ascii=False, default=str)
    elif format == "text":
        with open(output, 'w', encoding='utf-8') as f:
            f.write(CVFormatter.to_formatted_text(cv))
    elif format == "html":
        with open(output, 'w', encoding='utf-8') as f:
            f.write(CVFormatter.to_html(cv))
    elif format == "markdown":
        with open(output, 'w', encoding='utf-8') as f:
            f.write(CVFormatter.to_markdown(cv))

    click.echo(f"📄 CV gespeichert als: {output}")


@cli.command()
@click.option("--count", "-c", default=100, help="Anzahl CVs zu generieren")
@click.option("--output", "-o", default="batch_cvs", help="Output-Datei Präfix")
@click.option("--format", "-f", type=click.Choice(["csv", "json", "excel"]), 
              default="csv", help="Output-Format")
@click.option("--seed", type=int, help="Random Seed")
@click.option("--validate/--no-validate", default=True, help="Statistiken validieren")
def batch(count, output, format, seed, validate):
    """Generiert eine Batch von synthetischen CVs"""

    click.echo(f"🇨🇭 Swiss CV Generator - Batch ({count} CVs)")
    click.echo("=" * 50)

    if count > 10000:
        if not click.confirm(f"⚠️  {count} CVs können lange dauern. Fortfahren?"):
            return

    # Generierung
    with click.progressbar(length=count, label="CVs generieren") as bar:
        generator = SwissCVGenerator(random_seed=seed)
        batch_generator = BatchGenerator(generator)

        # In Chunks für Progress-Anzeige
        chunk_size = max(1, count // 20)  # 20 Updates
        all_cvs = []

        for i in range(0, count, chunk_size):
            chunk_count = min(chunk_size, count - i)
            chunk_cvs = batch_generator.generate_batch(chunk_count)
            all_cvs.extend(chunk_cvs)
            bar.update(len(chunk_cvs))

    click.echo(f"✓ {len(all_cvs)} CVs generiert")

    # Validierung
    if validate:
        click.echo("\n📊 Validiere Statistiken...")
        validation = StatisticsValidator.validate_cvs(all_cvs)

        summary = validation["summary"]
        click.echo(f"   Validierungen: {summary['passed']}/{summary['total_validations']} bestanden")
        click.echo(f"   Status: {summary['overall_status']}")

        if summary["overall_status"] == "FAIL":
            click.echo("⚠️  Warnung: Einige Validierungen fehlgeschlagen")

    # Export
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        if format == "csv":
            filename = f"{output}_{timestamp}.csv"
            batch_generator.export_csv(all_cvs, filename)
        elif format == "json":
            filename = f"{output}_{timestamp}.json"
            batch_generator.export_json(all_cvs, filename)
        elif format == "excel":
            filename = f"{output}_{timestamp}.xlsx"
            batch_generator.export_excel(all_cvs, filename)

        click.echo(f"💾 Exportiert nach: {filename}")

    except Exception as e:
        click.echo(f"❌ Export-Fehler: {e}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
def validate(input_file):
    """Validiert eine bestehende CV-Datei gegen Schweizer Statistiken"""

    click.echo("📊 Validiere CV-Daten...")

    try:
        # Lade CVs (unterstützt JSON und CSV)
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Hier müsste eine Konvertierung zurück zu CV-Objekten stattfinden
                # Vereinfacht für dieses Beispiel
                click.echo("JSON-Validierung noch nicht implementiert")
                return

        elif input_file.endswith('.csv'):
            import pandas as pd
            df = pd.read_csv(input_file)

            # Einfache Statistiken
            total = len(df)
            click.echo(f"📈 Analysiere {total} CVs...")

            if 'gender' in df.columns:
                gender_counts = df['gender'].value_counts()
                click.echo("\n👥 Geschlechterverteilung:")
                for gender, count in gender_counts.items():
                    percentage = (count / total) * 100
                    click.echo(f"   {gender}: {count} ({percentage:.1f}%)")

            if 'language_region' in df.columns:
                region_counts = df['language_region'].value_counts()
                click.echo("\n🗺️  Sprachregionen:")
                for region, count in region_counts.items():
                    percentage = (count / total) * 100
                    click.echo(f"   {region}: {count} ({percentage:.1f}%)")

            if 'age' in df.columns:
                click.echo(f"\n📅 Altersstatistik:")
                click.echo(f"   Durchschnitt: {df['age'].mean():.1f} Jahre")
                click.echo(f"   Bereich: {df['age'].min()}-{df['age'].max()} Jahre")

        else:
            click.echo("❌ Unterstützte Formate: .json, .csv")

    except Exception as e:
        click.echo(f"❌ Validierungs-Fehler: {e}")


@cli.command()
def info():
    """Zeigt Informationen über den Generator"""

    click.echo("🇨🇭 Swiss CV Generator v1.0.0")
    click.echo("=" * 40)
    click.echo("Synthetische Lebenslauf-Generierung für den Schweizer Arbeitsmarkt")
    click.echo("")
    click.echo("📊 Basiert auf:")
    click.echo("   • BFS Arbeitsmarktstatistiken 2024")
    click.echo("   • Schweizer Bildungswege")
    click.echo("   • Regionale Unterschiede")
    click.echo("   • DSGVO-konforme synthetische Daten")
    click.echo("")
    click.echo("🎯 Anwendungen:")
    click.echo("   • HR-System Testing")
    click.echo("   • KI-Training")
    click.echo("   • Marktforschung")
    click.echo("   • Bias-Reduktion")


def main():
    """Entry point für console_scripts"""
    cli()


if __name__ == "__main__":
    main()

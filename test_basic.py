#!/usr/bin/env python3
"""
Schneller Test des Swiss CV Generators
"""

try:
    from swiss_cv_generator import SwissCVGenerator
    
    print("🇨🇭 Swiss CV Generator - Test")
    print("=" * 40)
    
    # Generator erstellen
    generator = SwissCVGenerator()
    
    # CV generieren
    cv = generator.generate_cv()
    
    # Ausgabe
    persona = cv.persona.personal
    print(f"✅ CV erfolgreich generiert!")
    print(f"Name: {persona.first_name} {persona.last_name}")
    print(f"Alter: {persona.age} Jahre")
    print(f"Region: {persona.language_region.value}")
    print(f"Sektor: {cv.persona.sector}")
    print(f"Berufserfahrung: {cv.total_experience_years} Jahre")
    print(f"Bildungsabschlüsse: {len(cv.education)}")
    
    print("\n🎉 Setup erfolgreich!")

except ImportError as e:
    print(f"❌ Import Fehler: {e}")
    print("Bitte sicherstellen, dass alle Dependencies installiert sind:")
    print("pip install -r requirements.txt")
    print("pip install -e .")

except Exception as e:
    print(f"❌ Fehler: {e}")

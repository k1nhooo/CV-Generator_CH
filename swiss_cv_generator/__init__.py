"""
Swiss CV Generator - Synthetische Lebenslauf-Generierung für den Schweizer Arbeitsmarkt
"""

from .core.cv_generator import SwissCVGenerator
from .core.persona_generator import SwissPersonaGenerator
from .utils.exporters import BatchGenerator
from .data_models import CV, Persona, Education, Career

__version__ = "1.0.0"
__all__ = [
    "SwissCVGenerator",
    "SwissPersonaGenerator",
    "BatchGenerator",
    "CV",
    "Persona",
    "Education",
    "Career",
]

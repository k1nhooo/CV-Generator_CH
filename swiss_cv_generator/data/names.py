"""
Schweizer Namen nach Sprachregionen
Basiert auf den häufigsten Namen in den jeweiligen Sprachregionen
"""

from typing import Dict, List

SWISS_NAMES: Dict[str, Dict[str, List[str]]] = {
    "deutsch": {
        "male": [
            "Hans", "Peter", "Thomas", "Andreas", "Daniel", "Martin", 
            "Michael", "Stefan", "Christian", "Markus", "David", "Patrick", 
            "Simon", "Marco", "Lukas", "Beat", "Reto", "Urs", "René", 
            "Philipp", "Roger", "Pascal", "Adrian", "Matthias", "Dominik",
            "Samuel", "Benjamin", "Tobias", "Jan", "Kevin", "Fabian",
            "Florian", "Raphael", "Joel", "Nils", "Tim", "Luca", "Noah"
        ],
        "female": [
            "Maria", "Anna", "Sandra", "Nicole", "Petra", "Andrea", 
            "Claudia", "Susanne", "Monika", "Christine", "Barbara", 
            "Kathrin", "Sabine", "Daniela", "Carmen", "Brigitte", 
            "Ursula", "Ruth", "Heidi", "Iris", "Simone", "Nadja",
            "Miriam", "Corina", "Jasmin", "Melanie", "Karin", "Doris",
            "Sarah", "Laura", "Michelle", "Stephanie", "Vanessa", 
            "Jessica", "Jennifer", "Chantal", "Manuela", "Anja"
        ],
        "surnames": [
            "Müller", "Meier", "Schmid", "Keller", "Weber", "Huber", 
            "Schneider", "Meyer", "Steiner", "Fischer", "Gerber", 
            "Brunner", "Baumann", "Frei", "Zimmermann", "Kaufmann",
            "Widmer", "Moser", "Wyss", "Roth", "Lehmann", "Zürcher",
            "Marti", "König", "Käser", "Flückiger", "Moor", "Graf",
            "Wegmann", "Hofer", "Stalder", "Sommer", "Bauer", "Hauser"
        ]
    },
    "français": {
        "male": [
            "Pierre", "Jean", "Michel", "Philippe", "Alain", "André", 
            "Claude", "Daniel", "François", "Laurent", "Nicolas", 
            "Olivier", "Pascal", "Stéphane", "Thierry", "Christophe",
            "Frédéric", "Didier", "Patrice", "Serge", "Bernard",
            "Marc", "Patrick", "Yves", "Christian", "Gérard",
            "Jacques", "Vincent", "Fabrice", "Sébastien", "Julien",
            "Antoine", "Maxime", "Alexandre", "Romain", "Thomas"
        ],
        "female": [
            "Marie", "Françoise", "Catherine", "Monique", "Sylvie", 
            "Isabelle", "Patricia", "Christine", "Véronique", 
            "Martine", "Nicole", "Brigitte", "Anne", "Chantal",
            "Dominique", "Nathalie", "Corinne", "Sandrine", 
            "Valérie", "Céline", "Stéphanie", "Karine", "Laure",
            "Sophie", "Delphine", "Audrey", "Emilie", "Julie",
            "Camille", "Charlotte", "Marion", "Sarah", "Laura"
        ],
        "surnames": [
            "Martin", "Bernard", "Dubois", "Thomas", "Robert", 
            "Richard", "Petit", "Durand", "Leroy", "Moreau", 
            "Simon", "Laurent", "Lefebvre", "Michel", "Garcia",
            "Roux", "David", "Bertrand", "Morel", "Fournier",
            "Girard", "Bonnet", "Dupont", "Lambert", "Fontaine",
            "Rousseau", "Vincent", "Muller", "Lefevre", "Faure",
            "Andre", "Mercier", "Blanc", "Guerin", "Boyer"
        ]
    },
    "italiano": {
        "male": [
            "Giuseppe", "Antonio", "Francesco", "Mario", "Luigi", 
            "Giovanni", "Salvatore", "Roberto", "Vincenzo", "Angelo", 
            "Marco", "Alessandro", "Stefano", "Pietro", "Domenico",
            "Paolo", "Andrea", "Carlo", "Nicola", "Bruno", "Claudio",
            "Michele", "Sergio", "Massimo", "Daniele", "Giorgio",
            "Luciano", "Maurizio", "Fabio", "Giancarlo", "Enzo",
            "Franco", "Renato", "Matteo", "Simone", "Federico"
        ],
        "female": [
            "Maria", "Anna", "Giuseppina", "Rosa", "Angela", 
            "Giovanna", "Teresa", "Lucia", "Carmela", "Caterina", 
            "Antonia", "Francesca", "Elena", "Rita", "Paola",
            "Laura", "Carla", "Giulia", "Patrizia", "Daniela",
            "Roberta", "Silvia", "Elisabetta", "Monica", "Barbara",
            "Antonella", "Cristina", "Federica", "Alessandra", 
            "Chiara", "Stefania", "Valentina", "Simona", "Claudia"
        ],
        "surnames": [
            "Rossi", "Ferrari", "Russo", "Bianchi", "Romano", 
            "Gallo", "Conti", "De Luca", "Mancini", "Ricci", 
            "Santoro", "Barbieri", "Fontana", "Mariani", "Rinaldi",
            "Colombo", "Benedetti", "Palumbo", "Pellegrini", "Galli",
            "Moretti", "Lombardi", "Gentile", "Martinelli", "Greco",
            "Fiore", "Testa", "Ferraro", "Barone", "De Angelis",
            "Cattaneo", "Vitale", "Villa", "Pagano", "Rizzo"
        ]
    }
}

"""Module d'analyse phonématique"""

class PhonemeAnalyzer:
    def __init__(self):
        self.paires_minimales = [
            {"mot1": "fil", "mot2": "fille", "description": "/il/ vs /ij/ - absence vs présence de [j]"},
            {"mot1": "con", "mot2": "ton", "description": "/kɔ̃/ vs /tɔ̃/ - [k] vs [t]"},
            {"mot1": "rein", "mot2": "train", "description": "/ʁɛ̃/ vs /tʁɛ̃/ - absence vs présence de [t]"},
            {"mot1": "frein", "mot2": "train", "description": "/fʁɛ̃/ vs /tʁɛ̃/ - [f] vs [t]"},
            {"mot1": "rein", "mot2": "frein", "description": "/ʁɛ̃/ vs /fʁɛ̃/ - absence vs [f]"},
            {"mot1": "bille", "mot2": "quille", "description": "/bil/ vs /kil/ - [b] vs [k]"},
            {"mot1": "fil", "mot2": "fils", "description": "/fil/ vs /fis/ - [l] vs [s]"},
            {"mot1": "con", "mot2": "pont", "description": "/kɔ̃/ vs /pɔ̃/ - [k] vs [p]"},
        ]
    
    def get_paires_minimales(self):
        """Retourner les paires minimales"""
        return self.paires_minimales
    
    def analyze_phonemes(self, audio_data):
        """Analyser les phonèmes d'un enregistrement"""
        # Analyse simplifiée des phonèmes
        return {"phonemes": [], "confidence": []}

"""Module d'analyse prosodique"""

class ProsodyAnalyzer:
    def __init__(self):
        self.characteristics = {
            "déclarative": {
                "F0": "Descend progressivement, intonation plate puis descendante en fin",
                "Amplitude": "Modérée et relativement stable",
                "Durée": "Normale, pas d'allongement final",
                "Exemple": "Tu fermes la grande porte."
            },
            "interrogative": {
                "F0": "Monte significativement en fin, montée générale",
                "Amplitude": "Peut augmenter légèrement",
                "Durée": "Légère augmentation, surtout en fin",
                "Exemple": "Tu fermes la grande porte?"
            },
            "exclamative": {
                "F0": "Très variable, montées et descentes marquées",
                "Amplitude": "Forte et variable",
                "Durée": "Variable avec des pauses expressives",
                "Exemple": "Tu fermes la grande porte!"
            },
            "impérative": {
                "F0": "Descendante ou stable, ordre direct",
                "Amplitude": "Plus forte que la déclarative",
                "Durée": "Normale à rapide",
                "Exemple": "Ferme la grande porte!"
            }
        }
    
    def get_characteristics(self, mode):
        """Récupérer les caractéristiques d'une modalité"""
        return self.characteristics.get(mode, {})
    
    def analyze_prosody(self, audio_data, sr):
        """Analyser les paramètres prosodiques"""
        import librosa
        import numpy as np
        
        # Extraction de F0
        f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, f_min=80, f_max=400, sr=sr)
        
        # Durée
        duration = len(audio_data) / sr
        
        # RMS
        rms = np.sqrt(np.mean(audio_data**2))
        
        return {
            "f0_mean": np.nanmean(f0[f0 > 0]),
            "f0_min": np.nanmin(f0[f0 > 0]),
            "f0_max": np.nanmax(f0[f0 > 0]),
            "duration": duration,
            "rms": rms
        }

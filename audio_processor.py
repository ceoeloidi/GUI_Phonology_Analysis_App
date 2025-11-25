"""Module de traitement audio"""

import numpy as np
from scipy import signal
import librosa

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 44100
    
    def extract_f0(self, audio_data, sr):
        """Extraire la fréquence fondamentale"""
        f0, voiced_flag, voiced_probs = librosa.pyin(audio_data, f_min=80, f_max=400, sr=sr)
        return f0, voiced_flag
    
    def extract_amplitude(self, audio_data):
        """Extraire l'enveloppe d'amplitude"""
        amplitude = np.abs(signal.hilbert(audio_data))
        return amplitude
    
    def extract_mfcc(self, audio_data, sr):
        """Extraire les coefficients MFCC"""
        mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        return mfcc
    
    def normalize_audio(self, audio_data):
        """Normaliser l'audio"""
        return audio_data / np.max(np.abs(audio_data))
    
    def apply_preemphasis(self, audio_data, coef=0.97):
        """Appliquer un filtre de préaccentuation"""
        return np.append(audio_data[0], audio_data[1:] - coef * audio_data[:-1])

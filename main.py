"""
Application d'Analyse de Phonologie en Français
GUI desktop pour l'analyse phonématique et prosodique
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy import signal
import librosa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from datetime import datetime

from modules.phoneme_analyzer import PhonemeAnalyzer
from modules.prosody_analyzer import ProsodyAnalyzer
from modules.audio_processor import AudioProcessor

class PhonologyAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application d'Analyse de Phonologie")
        self.root.geometry("1400x900")
        
        # Configuration du style
        self.setup_style()
        
        # Initialisation des analyseurs
        self.phoneme_analyzer = PhonemeAnalyzer()
        self.prosody_analyzer = ProsodyAnalyzer()
        self.audio_processor = AudioProcessor()
        
        # Stockage des enregistrements
        self.recordings = {}
        self.current_audio = None
        self.sample_rate = 44100
        
        # Dossier des enregistrements
        os.makedirs("enregistrements", exist_ok=True)
        
        # Création de l'interface
        self.create_ui()
    
    def setup_style(self):
        """Configuration du thème de l'application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs du thème (inspiré de la design inspiration)
        bg_color = "#0a0e27"
        fg_color = "#e0e0e0"
        accent_color = "#00d4ff"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", background="#1a1f3a", foreground=fg_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", background="#1a1f3a", foreground=fg_color)
        
        self.root.configure(bg=bg_color)
    
    def create_ui(self):
        """Création de l'interface utilisateur"""
        # Barre supérieure avec titre
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=20, pady=15)
        
        title_label = ttk.Label(header, text="Analyse de Phonologie Française", 
                               font=("Segoe UI", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglets
        self.create_phoneme_tab()
        self.create_prosody_tab()
        self.create_recorder_tab()
        self.create_comparison_tab()
    
    def create_phoneme_tab(self):
        """Onglet Phonématique - Paires Minimales"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Phonématique")
        
        # Titre
        title = ttk.Label(frame, text="Paires Minimales en Français", font=("Segoe UI", 14, "bold"))
        title.pack(padx=20, pady=15)
        
        # Données des paires minimales
        paires = self.phoneme_analyzer.get_paires_minimales()
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(frame, bg="#0a0e27", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar for y-scrolling
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold content
        # This frame will be the actual scrollable content
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Add some content to the scrollable frame
        for i in range(50):
            ttk.Label(scrollable_frame, text=f"This is line {i}").pack(pady=2)

        # Update the scrollregion of the canvas whenever the scrollable_frame's size changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.root.mainloop()
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Affichage des paires
        for i, paire in enumerate(paires, 1):
            paire_frame = ttk.Frame(scrollable_frame)
            paire_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Numéro et paire
            paire_text = f"{i}. {paire['mot1']} / {paire['mot2']}"
            label = ttk.Label(paire_frame, text=paire_text, font=("Courier New", 11, "bold"))
            label.pack(side=tk.LEFT, padx=10)
            
            # Description
            desc = ttk.Label(paire_frame, text=paire['description'], 
                           font=("Segoe UI", 9), foreground="#00d4ff")
            desc.pack(side=tk.LEFT, padx=10)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_prosody_tab(self):
        """Onglet Prosodie"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Prosodie")
        
        # Titre
        title = ttk.Label(frame, text="Analyse Prosodique: 'Tu fermes la grande porte'", 
                         font=("Segoe UI", 14, "bold"))
        title.pack(padx=20, pady=15)
        
        # Sous-onglets pour les modalités
        prosody_notebook = ttk.Notebook(frame)
        prosody_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.prosody_modes = ["déclarative", "interrogative", "exclamative", "impérative"]
        self.prosody_frames = {}
        
        for mode in self.prosody_modes:
            mode_frame = ttk.Frame(prosody_notebook)
            prosody_notebook.add(mode_frame, text=mode.capitalize())
            self.prosody_frames[mode] = mode_frame
            
            # Contenu pour chaque modalité
            self.create_prosody_mode_content(mode_frame, mode)
    
    def create_prosody_mode_content(self, frame, mode):
        """Contenu pour chaque modalité prosodique"""
        # Boutons d'enregistrement
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        record_btn = ttk.Button(button_frame, text=f"🎙️ Enregistrer ({mode})",
                               command=lambda m=mode: self.start_recording(m))
        record_btn.pack(side=tk.LEFT, padx=5)
        
        play_btn = ttk.Button(button_frame, text=f"▶️ Écouter",
                             command=lambda m=mode: self.play_recording(m))
        play_btn.pack(side=tk.LEFT, padx=5)
        
        # Caractéristiques attendues
        char_frame = ttk.LabelFrame(frame, text="Caractéristiques attendues", padding=15)
        char_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        characteristics = self.prosody_analyzer.get_characteristics(mode)
        
        for key, value in characteristics.items():
            text = f"{key}: {value}"
            label = ttk.Label(char_frame, text=text, font=("Segoe UI", 10), 
                            wraplength=400, justify=tk.LEFT)
            label.pack(anchor=tk.W, pady=5)
    
    def create_recorder_tab(self):
        """Onglet Enregistrement"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Enregistrement")
        
        # Titre
        title = ttk.Label(frame, text="Enregistrer et Analyser", font=("Segoe UI", 14, "bold"))
        title.pack(padx=20, pady=15)
        
        # Contrôles d'enregistrement
        control_frame = ttk.LabelFrame(frame, text="Contrôles", padding=15)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Saisie du nom de l'enregistrement
        name_frame = ttk.Frame(control_frame)
        name_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(name_frame, text="Nom de l'enregistrement:").pack(side=tk.LEFT, padx=5)
        self.record_name_var = tk.StringVar(value="Enregistrement 1")
        self.record_name_entry = ttk.Entry(name_frame, textvariable=self.record_name_var, width=30)
        self.record_name_entry.pack(side=tk.LEFT, padx=5)
        
        # Boutons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.record_button = ttk.Button(button_frame, text="🎙️ Démarrer",
                                       command=self.start_custom_recording)
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Arrêter",
                                     command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="▶️ Écouter", 
                  command=self.play_custom_recording).pack(side=tk.LEFT, padx=5)
        
        # Zone d'affichage des enregistrements
        list_frame = ttk.LabelFrame(frame, text="Enregistrements", padding=15)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox des enregistrements
        self.recordings_listbox = tk.Listbox(list_frame, bg="#1a1f3a", fg="#e0e0e0",
                                           selectmode=tk.SINGLE, height=10)
        self.recordings_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                command=self.recordings_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recordings_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.recording_is_active = False
        self.current_recording_stream = None
        self.current_recording_frames = []
    
    def create_comparison_tab(self):
        """Onglet Comparaison"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Comparaison")
        
        title = ttk.Label(frame, text="Comparaison des Paramètres Acoustiques", 
                         font=("Segoe UI", 14, "bold"))
        title.pack(padx=20, pady=15)
        
        # Sélection des enregistrements
        select_frame = ttk.LabelFrame(frame, text="Sélectionner les enregistrements", padding=15)
        select_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Enregistrement 1
        ttk.Label(select_frame, text="Enregistrement 1:").pack(side=tk.LEFT, padx=10)
        self.comparison_var1 = tk.StringVar()
        combo1 = ttk.Combobox(select_frame, textvariable=self.comparison_var1, state="readonly", width=25)
        combo1.pack(side=tk.LEFT, padx=5)
        
        # Enregistrement 2
        ttk.Label(select_frame, text="Enregistrement 2:").pack(side=tk.LEFT, padx=10)
        self.comparison_var2 = tk.StringVar()
        combo2 = ttk.Combobox(select_frame, textvariable=self.comparison_var2, state="readonly", width=25)
        combo2.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(select_frame, text="Comparer",
                  command=self.perform_comparison).pack(side=tk.LEFT, padx=10)
        
        # Zone de résultats
        self.comparison_canvas_frame = ttk.Frame(frame)
        self.comparison_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def start_recording(self, mode):
        """Démarrer un enregistrement prosodique"""
        messagebox.showinfo("Enregistrement", 
                          f"Enregistrez la phrase en modalité {mode}:\n\n'Tu fermes la grande porte'")
        self.start_custom_recording(mode)
    
    def start_custom_recording(self, mode=None):
        """Démarrer un enregistrement personnalisé"""
        if self.recording_is_active:
            messagebox.showwarning("Enregistrement", "Un enregistrement est déjà en cours")
            return
        
        self.recording_is_active = True
        self.current_recording_frames = []
        self.current_recording_mode = mode
        
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        messagebox.showinfo("Enregistrement", "Enregistrement en cours...\nParlez clairement")
        
        # Enregistrement audio
        self.current_recording_stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            callback=self.audio_callback,
            blocksize=1024
        )
        self.current_recording_stream.start()
    
    def audio_callback(self, indata, frames, time, status):
        """Callback pour l'enregistrement audio"""
        if status:
            print(f"Erreur d'enregistrement: {status}")
        self.current_recording_frames.append(indata.copy())
    
    def stop_recording(self):
        """Arrêter l'enregistrement"""
        if not self.recording_is_active:
            return
        
        self.current_recording_stream.stop()
        self.current_recording_stream.close()
        self.recording_is_active = False
        
        # Combiner les frames
        audio_data = np.concatenate(self.current_recording_frames, axis=0)
        self.current_audio = audio_data.flatten()
        
        # Sauvegarder
        filename = self.record_name_var.get() or f"Recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if self.current_recording_mode:
            filename = f"{self.current_recording_mode}_{filename}"
        
        filepath = f"enregistrements/{filename}.wav"
        sf.write(filepath, self.current_audio, self.sample_rate)
        
        self.recordings[filename] = filepath
        self.update_recordings_list()
        
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        messagebox.showinfo("Succès", f"Enregistrement sauvegardé: {filename}")
    
    def play_recording(self, mode):
        """Écouter un enregistrement prosodique"""
        if mode not in self.recordings:
            messagebox.showwarning("Erreur", f"Pas d'enregistrement pour la modalité {mode}")
            return
        
        audio_data, sr = librosa.load(self.recordings[mode], sr=self.sample_rate)
        sd.play(audio_data, sr)
    
    def play_custom_recording(self):
        """Écouter l'enregistrement actuel"""
        if self.current_audio is None:
            messagebox.showwarning("Erreur", "Aucun enregistrement à écouter")
            return
        
        sd.play(self.current_audio, self.sample_rate)
    
    def update_recordings_list(self):
        """Mettre à jour la liste des enregistrements"""
        self.recordings_listbox.delete(0, tk.END)
        for name in self.recordings.keys():
            self.recordings_listbox.insert(tk.END, name)
    
    def perform_comparison(self):
        """Comparer deux enregistrements"""
        rec1 = self.comparison_var1.get()
        rec2 = self.comparison_var2.get()
        
        if not rec1 or not rec2:
            messagebox.showwarning("Erreur", "Sélectionnez deux enregistrements")
            return
        
        # Charger les fichiers
        audio1, sr1 = librosa.load(self.recordings[rec1], sr=self.sample_rate)
        audio2, sr2 = librosa.load(self.recordings[rec2], sr=self.sample_rate)
        
        # Créer la figure de comparaison
        fig = Figure(figsize=(12, 8), dpi=100, facecolor="#0a0e27")
        
        # Formes d'onde
        ax1 = fig.add_subplot(3, 2, 1)
        ax1.plot(audio1, color="#00d4ff", linewidth=0.5)
        ax1.set_title(f"Forme d'onde - {rec1}", color="#e0e0e0")
        ax1.set_facecolor("#1a1f3a")
        ax1.tick_params(colors="#e0e0e0")
        
        ax2 = fig.add_subplot(3, 2, 2)
        ax2.plot(audio2, color="#00ff88", linewidth=0.5)
        ax2.set_title(f"Forme d'onde - {rec2}", color="#e0e0e0")
        ax2.set_facecolor("#1a1f3a")
        ax2.tick_params(colors="#e0e0e0")
        
        # Spectrogramme
        ax3 = fig.add_subplot(3, 2, 3)
        D1 = librosa.stft(audio1)
        S1 = librosa.power_to_db(np.abs(D1)**2, ref=np.max)
        im1 = ax3.imshow(S1, aspect='auto', origin='lower', cmap='Blues')
        ax3.set_title(f"Spectrogramme - {rec1}", color="#e0e0e0")
        ax3.set_facecolor("#1a1f3a")
        fig.colorbar(im1, ax=ax3)
        
        ax4 = fig.add_subplot(3, 2, 4)
        D2 = librosa.stft(audio2)
        S2 = librosa.power_to_db(np.abs(D2)**2, ref=np.max)
        im2 = ax4.imshow(S2, aspect='auto', origin='lower', cmap='Greens')
        ax4.set_title(f"Spectrogramme - {rec2}", color="#e0e0e0")
        ax4.set_facecolor("#1a1f3a")
        fig.colorbar(im2, ax=ax4)
        
        # Analyse F0 (fréquence fondamentale)
        ax5 = fig.add_subplot(3, 2, 5)
        f0_1, voiced_flag1, voiced_probs1 = librosa.pyin(audio1, f_min=80, f_max=400, sr=self.sample_rate)
        f0_2, voiced_flag2, voiced_probs2 = librosa.pyin(audio2, f_min=80, f_max=400, sr=self.sample_rate)
        
        time1 = np.linspace(0, len(audio1)/self.sample_rate, len(f0_1))
        time2 = np.linspace(0, len(audio2)/self.sample_rate, len(f0_2))
        
        ax5.plot(time1, f0_1, label=rec1, color="#00d4ff", linewidth=2)
        ax5.plot(time2, f0_2, label=rec2, color="#00ff88", linewidth=2)
        ax5.set_ylabel("F0 (Hz)", color="#e0e0e0")
        ax5.set_title("Fréquence Fondamentale (F0)", color="#e0e0e0")
        ax5.legend(loc='upper right', facecolor="#1a1f3a", edgecolor="#e0e0e0")
        ax5.set_facecolor("#1a1f3a")
        ax5.tick_params(colors="#e0e0e0")
        
        # Amplitude
        ax6 = fig.add_subplot(3, 2, 6)
        amp1 = np.abs(signal.hilbert(audio1))
        amp2 = np.abs(signal.hilbert(audio2))
        
        time_amp1 = np.linspace(0, len(audio1)/self.sample_rate, len(amp1))
        time_amp2 = np.linspace(0, len(audio2)/self.sample_rate, len(amp2))
        
        ax6.plot(time_amp1, amp1, label=rec1, color="#00d4ff", linewidth=2)
        ax6.plot(time_amp2, amp2, label=rec2, color="#00ff88", linewidth=2)
        ax6.set_ylabel("Amplitude", color="#e0e0e0")
        ax6.set_xlabel("Temps (s)", color="#e0e0e0")
        ax6.set_title("Enveloppe d'Amplitude", color="#e0e0e0")
        ax6.legend(loc='upper right', facecolor="#1a1f3a", edgecolor="#e0e0e0")
        ax6.set_facecolor("#1a1f3a")
        ax6.tick_params(colors="#e0e0e0")
        
        fig.tight_layout()
        
        # Afficher dans le canvas
        for widget in self.comparison_canvas_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.comparison_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Statistiques
        stats_text = self.generate_comparison_stats(audio1, audio2, f0_1, f0_2, rec1, rec2)
        stats_label = ttk.Label(self.comparison_canvas_frame, text=stats_text, 
                              font=("Courier New", 9), justify=tk.LEFT, wraplength=300)
        stats_label.pack(anchor=tk.W, padx=10, pady=10)
    
    def generate_comparison_stats(self, audio1, audio2, f0_1, f0_2, rec1, rec2):
        """Générer les statistiques de comparaison"""
        # Durée
        dur1 = len(audio1) / self.sample_rate
        dur2 = len(audio2) / self.sample_rate
        
        # RMS (amplitude moyenne)
        rms1 = np.sqrt(np.mean(audio1**2))
        rms2 = np.sqrt(np.mean(audio2**2))
        
        # F0 moyenne
        f0_mean1 = np.nanmean(f0_1[f0_1 > 0])
        f0_mean2 = np.nanmean(f0_2[f0_2 > 0])
        
        stats = f"""
COMPARAISON DES PARAMÈTRES ACOUSTIQUES

{rec1}:
  • Durée: {dur1:.2f}s
  • Amplitude RMS: {rms1:.4f}
  • F0 moyen: {f0_mean1:.1f} Hz

{rec2}:
  • Durée: {dur2:.2f}s
  • Amplitude RMS: {rms2:.4f}
  • F0 moyen: {f0_mean2:.1f} Hz

DIFFÉRENCES:
  • Durée: {abs(dur1-dur2):.2f}s ({((dur2-dur1)/dur1*100):+.1f}%)
  • Amplitude: {abs(rms1-rms2):.4f} ({((rms2-rms1)/rms1*100):+.1f}%)
  • F0: {abs(f0_mean1-f0_mean2):.1f} Hz ({((f0_mean2-f0_mean1)/f0_mean1*100):+.1f}%)
        """
        return stats

def main():
    root = tk.Tk()
    app = PhonologyAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

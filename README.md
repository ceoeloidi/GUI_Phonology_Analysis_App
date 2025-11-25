# Application d'Analyse de Phonologie Française

Application de bureau pour l'analyse phonématique et prosodique en français.

## Installation

1. Créer un environnement virtuel:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
\`\`\`

2. Installer les dépendances:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Lancer l'application:
\`\`\`bash
python main.py
\`\`\`

## Fonctionnalités

### Phonématique
- Visualisation des paires minimales en français
- Explication des différences phonémiques

### Prosodie
- Enregistrement de la phrase "Tu fermes la grande porte" en 4 modalités
- Analyse des paramètres acoustiques (F0, amplitude, durée)
- Comparaison visuelle des enregistrements
- Spectrogrammes et formes d'onde

### Enregistrement
- Interface intuitive d'enregistrement audio
- Stockage des enregistrements
- Lecture directe

### Comparaison
- Comparaison côte à côte de deux enregistrements
- Statistiques acoustiques détaillées
- Visualisations multiples

## Structure

- `main.py` - Interface graphique principale
- `modules/phoneme_analyzer.py` - Analyse phonématique
- `modules/prosody_analyzer.py` - Analyse prosodique
- `modules/audio_processor.py` - Traitement audio

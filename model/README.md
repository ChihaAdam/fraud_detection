# Projet ML - Détection de fraude (dataset A, SVM)

Lancer depuis le dossier `projetML` :

    python -m model.main              # affiche + sauvegarde les figures
    python -m model.main --no-show    # sauvegarde seulement (plus rapide)

## Architecture

| Fichier / dossier | Rôle (étape de l'énoncé) |
|---|---|
| `main.py` | Appelle toutes les étapes dans l'ordre |
| `config.py` | Chemins, constantes, grille d'hyperparamètres, CV = 4 |
| `utils.py` | Sauvegarde des figures/tableaux, titres |
| `dataset/loader.py` | Chargement de la dataset (A par défaut) |
| `exploration/data_display.py` | 1. Afficher et interpréter les données |
| `exploration/visualization.py` | 2. Visualisation seaborn (7 figures) |
| `exploration/outliers.py` | 3. Valeurs aberrantes (IQR) |
| `preprocessing/preprocessing.py` | 4. Nettoyage, split, OutlierClipper |
| `preprocessing/feature_selection.py` | 5. Sélection des caractéristiques |
| `ml_models/svm_explanation.py` | 6. Description du SVM + figures (marge, noyaux, C) |
| `ml_models/svm.py` | 7. Pipeline SVM + GridSearchCV (CV = 4) |
| `ml_models/evaluation.py` | 8-9. Matrices de confusion, ROC, tableaux récapitulatifs |
| `resultats/figures`, `resultats/tables` | Sorties générées (PNG / CSV) |

Pour changer de dataset : `DATASET_NAME` dans `config.py` ("A" à "E").
Pour ajouter un 2e modèle (l'énoncé en exige au moins 2) : créer
`ml_models/<modele>.py` sur le modèle de `svm.py` (pipeline + grille) et
l'appeler dans `main.py`.

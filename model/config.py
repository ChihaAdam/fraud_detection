"""Configuration centrale du projet : chemins, constantes et grille de l'SVM."""
from pathlib import Path

# ----------------------------------------------------------------- chemins
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
RESULTS_DIR = BASE_DIR / "resultats"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

# ----------------------------------------------------------------- données
DATASET_NAME = "A"          # A = 492 normales / 492 fraudes (NearMiss)
TARGET = "Class"            # 1 = fraude, 0 = transaction normale
LABELS = {0: "Normale", 1: "Fraude"}
PALETTE = {"Normale": "#3b7dd8", "Fraude": "#d8453b"}

# ----------------------------------------------------------- pré-traitement
RANDOM_STATE = 42
TEST_SIZE = 0.2
OUTLIER_FACTOR_DETECTION = 1.5   # règle classique de Tukey (détection)
OUTLIER_FACTOR_CLIPPING = 3.0    # valeurs extrêmes seulement (traitement)

# --------------------------------------------------------- validation croisée
CV_FOLDS = 4                     # imposé par l'énoncé (CV = 4)
SCORING = ["accuracy", "precision", "recall", "f1"]
REFIT_METRIC = "f1"

# ------------------------------------------------------------ grille de l'SVM
K_FEATURES = [10, 20, "all"]     # nombre de variables gardées (SelectKBest)
C_VALUES = [0.1, 1, 10, 100, 1000]
GAMMA_VALUES = ["scale", 0.001, 0.01, 0.1]

SVM_PARAM_GRID = [
    {   # noyau linéaire : pas de gamma
        "selector__k": K_FEATURES,
        "svm__kernel": ["linear"],
        "svm__C": C_VALUES,
    },
    {   # noyau RBF : C et gamma
        "selector__k": K_FEATURES,
        "svm__kernel": ["rbf"],
        "svm__C": C_VALUES,
        "svm__gamma": GAMMA_VALUES,
    },
]

# ----------------------------------------------------------------- affichage
SHOW_PLOTS = True                # False => sauvegarde seulement les figures

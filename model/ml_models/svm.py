"""Modèle SVM : pipeline complet + recherche des hyperparamètres (CV = 4)."""
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import config
from preprocessing.feature_selection import build_selector
from preprocessing.preprocessing import OutlierClipper
from utils import save_table, titre


def svm_model():
    """Version simple (conservée pour compatibilité avec main)."""
    from sklearn.pipeline import make_pipeline
    return make_pipeline(StandardScaler(), SVC(kernel="rbf"))


def build_svm_pipeline():
    """Clipping des outliers -> normalisation -> sélection de variables -> SVM."""
    scaler = StandardScaler()
    out = OutlierClipper()
    selector = build_selector()
    return Pipeline([
        ("clipper", out),
        ("scaler", scaler),
        ("selector", selector),
        ("svm", SVC(random_state=config.RANDOM_STATE)),
    ])

def tune_svm(X_train, y_train):
    """GridSearchCV (StratifiedKFold, CV = 4) ; sélection du meilleur F1."""
    titre("ÉTAPE 7 - APPRENTISSAGE SVM + RECHERCHE DES PARAMÈTRES (CV = 4)")
    cv = StratifiedKFold(n_splits=config.CV_FOLDS, shuffle=True,
                         random_state=config.RANDOM_STATE)
    grid = GridSearchCV(
        build_svm_pipeline(),
        param_grid=config.SVM_PARAM_GRID,
        scoring=config.SCORING,
        refit=config.REFIT_METRIC,
        cv=cv,
        n_jobs=-1,
        return_train_score=False,
    )
    grid.fit(X_train, y_train)

    n_combi = len(grid.cv_results_["params"])
    print(f"{n_combi} combinaisons x {config.CV_FOLDS} plis = "
          f"{n_combi * config.CV_FOLDS} entraînements.")
    print("\nMeilleurs paramètres :")
    for nom, val in grid.best_params_.items():
        print(f"  {nom:15s} = {val}")
    print(f"Meilleur F1 moyen en CV : {grid.best_score_:.4f}")
    return grid

def cv_results_table(grid, top=10):
    """Tableau des meilleures combinaisons testées en validation croisée."""
    res = pd.DataFrame(grid.cv_results_)
    f = config.REFIT_METRIC
    tableau = pd.DataFrame({
        "Rang": res[f"rank_test_{f}"],
        "Paramètres": res["params"].astype(str),
        "Accuracy": res["mean_test_accuracy"],
        "Precision": res["mean_test_precision"],
        "Recall": res["mean_test_recall"],
        "F1": res["mean_test_f1"],
        "F1 (écart-type)": res["std_test_f1"],
    }).sort_values("Rang").head(top).round(4).reset_index(drop=True)
    print(f"\n--- Top {top} des combinaisons (validation croisée, CV={config.CV_FOLDS}) ---")
    print(tableau.drop(columns="Paramètres").to_string(index=False))
    save_table(tableau, "svm_top_combinaisons_cv")
    return tableau

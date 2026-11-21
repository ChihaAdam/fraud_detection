"""Évaluation : métriques, matrices de confusion, courbe ROC, tableaux récapitulatifs."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (accuracy_score, auc, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score, roc_curve)
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from model import config
from model.utils import save_figure, save_table, titre


def evaluate_model(nom, modele, X_train, X_test, y_train, y_test, cls):
    """Entraîne le modèle puis calcule les métriques (Class = 1 -> fraude)."""
    modele.fit(X_train, y_train)
    y_pred = modele.predict(X_test)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "Dataset": cls,
        "Modèle": nom,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred, zero_division=0),
        "Fraudes détectées": f"{tp}/{tp + fn}",
        "Fausses alertes": fp,
    }


# --------------------------------------------------------------------- calculs
def _metriques(y_true, y_pred):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred),
        "F1": f1_score(y_true, y_pred, zero_division=0),
    }


def evaluate_svm(grid, X_train, y_train, X_test, y_test):
    """Évalue le meilleur SVM : prédictions CV sur le train + prédictions sur le test."""
    titre("ÉTAPE 8 - ÉVALUATION (MATRICES DE CONFUSION ET PERFORMANCES)")
    best = grid.best_estimator_

    cv = StratifiedKFold(n_splits=config.CV_FOLDS, shuffle=True,
                         random_state=config.RANDOM_STATE)
    y_pred_cv = cross_val_predict(best, X_train, y_train, cv=cv)
    y_pred_test = best.predict(X_test)

    cm_cv = confusion_matrix(y_train, y_pred_cv)
    cm_test = confusion_matrix(y_test, y_pred_test)

    print("\n--- Rapport de classification (jeu de test) ---")
    print(classification_report(y_test, y_pred_test,
                                target_names=list(config.LABELS.values()), digits=4))

    plot_confusion_matrices(cm_cv, cm_test)
    plot_roc_curve(best, X_test, y_test)
    plot_grid_heatmap(grid)

    return {
        "cm_cv": cm_cv, "cm_test": cm_test,
        "metrics_cv": _metriques(y_train, y_pred_cv),
        "metrics_test": _metriques(y_test, y_pred_test),
    }


# ------------------------------------------------------------------ graphiques
def plot_confusion_matrices(cm_cv, cm_test):
    noms = list(config.LABELS.values())
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, cm, titre_ax in zip(
        axes, [cm_cv, cm_test],
        [f"Train (prédictions CV = {config.CV_FOLDS})", "Test (20 % jamais vus)"],
    ):
        pct = cm / cm.sum(axis=1, keepdims=True) * 100
        etiquettes = [[f"{cm[i, j]}\n({pct[i, j]:.1f} %)" for j in range(2)]
                      for i in range(2)]
        sns.heatmap(cm, annot=etiquettes, fmt="", cmap="Blues", cbar=False,
                    xticklabels=noms, yticklabels=noms, annot_kws={"size": 13}, ax=ax)
        ax.set_title(titre_ax)
        ax.set_xlabel("Classe prédite")
        ax.set_ylabel("Classe réelle")
    fig.suptitle("Matrices de confusion - SVM", y=1.02)
    fig.tight_layout()
    save_figure(fig, "10_matrices_confusion_svm")


def plot_roc_curve(modele, X_test, y_test):
    scores = modele.decision_function(X_test)
    fpr, tpr, _ = roc_curve(y_test, scores)
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.plot(fpr, tpr, lw=2, label=f"SVM (AUC = {auc(fpr, tpr):.4f})")
    ax.plot([0, 1], [0, 1], "k--", label="Hasard")
    ax.set_xlabel("Taux de faux positifs")
    ax.set_ylabel("Taux de vrais positifs (Recall)")
    ax.set_title("Courbe ROC - jeu de test")
    ax.legend(loc="lower right")
    save_figure(fig, "11_courbe_roc_svm")


def plot_grid_heatmap(grid):
    """F1 moyen en CV selon C et gamma (noyau RBF, meilleur k)."""
    res = pd.DataFrame(grid.cv_results_)
    res = res[res["param_svm__kernel"] == "rbf"]
    if res.empty:
        return
    k_best = grid.best_params_["selector__k"]
    res = res[res["param_selector__k"].astype(str) == str(k_best)]
    pivot = res.pivot_table(index="param_svm__C", columns="param_svm__gamma",
                            values="mean_test_f1", aggfunc="max")
    pivot.columns = [str(c) for c in pivot.columns]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.heatmap(pivot, annot=True, fmt=".3f", cmap="viridis", ax=ax)
    ax.set_title(f"F1 moyen en CV (noyau RBF, k = {k_best})")
    ax.set_xlabel("gamma")
    ax.set_ylabel("C")
    ax.invert_yaxis()
    save_figure(fig, "12_grille_C_gamma")


# ---------------------------------------------------------------- récapitulatif
def summary_tables(grid, resultats, selected_features, n_features_total):
    """Tableaux récapitulatifs (affichés et sauvegardés)."""
    titre("ÉTAPE 9 - TABLEAUX RÉCAPITULATIFS")

    params = pd.DataFrame(
        [(k.split("__")[-1] if "__" in k else k, str(v))
         for k, v in grid.best_params_.items()],
        columns=["Hyperparamètre", "Valeur optimale"],
    )
    params.loc[len(params)] = ["variables retenues",
                               f"{len(selected_features)}/{n_features_total}"]
    print("\n--- Paramètres optimaux (CV = 4) ---")
    print(params.to_string(index=False))
    save_table(params, "svm_parametres_optimaux")

    perf = pd.DataFrame({
        "Train (CV=4)": resultats["metrics_cv"],
        "Test": resultats["metrics_test"],
    }).T.round(4)
    perf.index.name = "Jeu"
    print("\n--- Performances du SVM ---")
    print(perf.to_string())
    save_table(perf.reset_index(), "svm_performances")

    tn, fp, fn, tp = resultats["cm_test"].ravel()
    detail = pd.DataFrame({
        "Indicateur": ["Fraudes détectées (VP)", "Fraudes ratées (FN)",
                       "Fausses alertes (FP)", "Normales bien classées (VN)"],
        "Nombre (test)": [tp, fn, fp, tn],
    })
    print("\n--- Détail sur le jeu de test ---")
    print(detail.to_string(index=False))
    save_table(detail, "svm_detail_test")

    print(f"\nVariables retenues : {', '.join(selected_features)}")
    return params, perf, detail

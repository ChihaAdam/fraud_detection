"""Étape 5 : sélection des caractéristiques les plus pertinentes.

Deux mesures calculées sur le TRAIN uniquement :
  - test ANOVA (F-score)      : relation linéaire variable <-> classe
  - information mutuelle      : relation quelconque (non linéaire comprise)
Dans le Pipeline, SelectKBest(f_classif) garde les k meilleures variables ;
k est choisi par la validation croisée (GridSearchCV).
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

import config
from utils import save_figure, save_table, titre


def build_selector(k="all"):
    return SelectKBest(score_func=f_classif, k=k)


def compute_feature_scores(X_train, y_train):
    f_scores, _ = f_classif(X_train, y_train)
    mi = mutual_info_classif(X_train, y_train, random_state=config.RANDOM_STATE)
    scores = pd.DataFrame({
        "Variable": X_train.columns,
        "ANOVA F": f_scores,
        "Information mutuelle": mi,
    })
    scores["Rang F"] = scores["ANOVA F"].rank(ascending=False).astype(int)
    return scores.sort_values("ANOVA F", ascending=False).reset_index(drop=True)


def plot_feature_scores(scores):
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))
    sns.barplot(data=scores, x="ANOVA F", y="Variable", color="#5b8def", ax=axes[0])
    axes[0].set_title("Score ANOVA (F)")
    sns.barplot(data=scores, x="Information mutuelle", y="Variable",
                color="#e08a5b", ax=axes[1])
    axes[1].set_title("Information mutuelle")
    axes[1].set_ylabel("")
    fig.suptitle("Pertinence des variables (calculée sur le train)", y=1.0)
    fig.tight_layout()
    save_figure(fig, "09_selection_caracteristiques")


def get_selected_features(pipeline, columns):
    """Noms des variables retenues par le sélecteur du pipeline entraîné."""
    masque = pipeline.named_steps["selector"].get_support()
    return [c for c, garde in zip(columns, masque) if garde]


def analyze_features(X_train, y_train):
    titre("ÉTAPE 5 - SÉLECTION DES CARACTÉRISTIQUES")
    scores = compute_feature_scores(X_train, y_train)
    print(scores.head(10).round(3).to_string(index=False))
    save_table(scores.round(4), "scores_caracteristiques")
    plot_feature_scores(scores)
    print("\nLe nombre optimal k de variables conservées (10, 20 ou toutes) sera "
          "choisi par validation croisée avec les hyperparamètres du SVM.")
    return scores

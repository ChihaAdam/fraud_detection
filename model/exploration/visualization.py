"""Étape 2 : visualisation des données avec seaborn."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import config
from utils import save_figure, titre

sns.set_theme(style="whitegrid", context="notebook")


def _avec_libelle(df):
    """Copie du DataFrame avec une colonne 'Type' (Normale / Fraude) lisible."""
    d = df.copy()
    d["Type"] = d[config.TARGET].map(config.LABELS)
    return d


def _top_features(df, n):
    """Les n variables les plus corrélées (en valeur absolue) à la cible."""
    corr = df.corr()[config.TARGET].drop(config.TARGET).abs()
    return corr.sort_values(ascending=False).head(n).index.tolist()


def plot_class_distribution(df):
    d = _avec_libelle(df)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(data=d, x="Type", hue="Type", palette=config.PALETTE,
                  order=["Normale", "Fraude"], legend=False, ax=ax)
    for c in ax.containers:
        ax.bar_label(c)
    ax.set_title(f"Répartition des classes - dataset {config.DATASET_NAME}")
    ax.set_xlabel("")
    ax.set_ylabel("Nombre de transactions")
    save_figure(fig, "01_repartition_classes")


def plot_amount_time(df):
    d = _avec_libelle(df)
    d["log(1+Amount)"] = np.log1p(d["Amount"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data=d, x="log(1+Amount)", hue="Type", palette=config.PALETTE,
                 kde=True, element="step", ax=axes[0])
    axes[0].set_title("Distribution du montant (échelle log)")
    sns.histplot(data=d, x="Time", hue="Type", palette=config.PALETTE,
                 kde=True, element="step", ax=axes[1])
    axes[1].set_title("Distribution du temps")
    save_figure(fig, "02_montant_et_temps")


def plot_feature_distributions(df):
    d = _avec_libelle(df)
    features = [c for c in df.columns if c != config.TARGET]
    n_cols = 5
    n_rows = int(np.ceil(len(features) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 3 * n_rows))
    for ax, col in zip(axes.ravel(), features):
        sns.kdeplot(data=d, x=col, hue="Type", palette=config.PALETTE,
                    fill=True, common_norm=False, warn_singular=False,
                    legend=False, ax=ax)
        ax.set_title(col, fontsize=10)
        ax.set_xlabel("")
        ax.set_ylabel("")
    for ax in axes.ravel()[len(features):]:
        ax.axis("off")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in config.PALETTE.values()]
    fig.legend(handles, config.PALETTE.keys(), loc="upper right")
    fig.suptitle("Densité de chaque variable selon la classe", fontsize=14, y=1.0)
    fig.tight_layout()
    save_figure(fig, "03_distributions_variables")


def plot_correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(13, 10))
    sns.heatmap(df.corr(), cmap="coolwarm", center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.2, cbar_kws={"shrink": 0.7}, ax=ax)
    ax.set_title("Matrice de corrélation")
    save_figure(fig, "04_matrice_correlation")


def plot_correlation_with_target(df):
    corr = df.corr()[config.TARGET].drop(config.TARGET).sort_values()
    fig, ax = plt.subplots(figsize=(7, 8))
    sns.barplot(x=corr.values, y=corr.index, color="#5b8def", ax=ax)
    ax.set_title("Corrélation de chaque variable avec Class (fraude)")
    ax.set_xlabel("Coefficient de corrélation de Pearson")
    save_figure(fig, "05_correlation_avec_cible")


def plot_boxplots_top_features(df, n=8):
    d = _avec_libelle(df)
    top = _top_features(df, n)
    fig, axes = plt.subplots(2, n // 2, figsize=(4 * (n // 2), 8))
    for ax, col in zip(axes.ravel(), top):
        sns.boxplot(data=d, x="Type", y=col, hue="Type", palette=config.PALETTE,
                    order=["Normale", "Fraude"], legend=False, ax=ax)
        ax.set_title(col)
        ax.set_xlabel("")
    fig.suptitle(f"Boxplots des {n} variables les plus liées à la fraude", y=1.0)
    fig.tight_layout()
    save_figure(fig, "06_boxplots_top_variables")


def plot_pairplot(df, n=4):
    d = _avec_libelle(df)
    top = _top_features(df, n)
    grille = sns.pairplot(d[top + ["Type"]], hue="Type", palette=config.PALETTE,
                          corner=True, plot_kws={"s": 18, "alpha": 0.6})
    grille.figure.suptitle(f"Pairplot des {n} variables les plus discriminantes", y=1.02)
    save_figure(grille.figure, "07_pairplot_top_variables")


def visualize_data(df):
    titre("ÉTAPE 2 - VISUALISATION (seaborn)")
    plot_class_distribution(df)
    plot_amount_time(df)
    plot_feature_distributions(df)
    plot_correlation_heatmap(df)
    plot_correlation_with_target(df)
    plot_boxplots_top_features(df)
    plot_pairplot(df)
    print("\nLecture : les variables dont les densités des deux classes se "
          "séparent nettement (ex. V14, V4, V12...) sont les plus utiles pour "
          "détecter la fraude.")

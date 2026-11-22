"""Étape 2 : visualisation des données avec seaborn."""
import matplotlib.pyplot as plt
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


def plot_correlation_with_target(df):
    corr = df.corr()[config.TARGET].drop(config.TARGET).sort_values()
    fig, ax = plt.subplots(figsize=(7, 8))
    sns.barplot(x=corr.values, y=corr.index, color="#5b8def", ax=ax)
    ax.set_title("Corrélation de chaque variable avec Class (fraude)")
    ax.set_xlabel("Coefficient de corrélation de Pearson")
    save_figure(fig, "04_correlation_avec_cible")


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
    save_figure(fig, "05_boxplots_top_variables")


def visualize_data(df):
    titre("ÉTAPE 2 - VISUALISATION (seaborn)")
    plot_class_distribution(df)
    plot_correlation_with_target(df)
    plot_boxplots_top_features(df)
    print("\nLecture : les variables dont les distributions des deux classes "
          "se séparent nettement (ex. V14, V4, V12...) sont les plus utiles "
          "pour détecter la fraude.")
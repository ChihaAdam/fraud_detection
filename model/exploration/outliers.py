"""Étape 3 : détection des valeurs aberrantes (méthode IQR / Tukey)."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from model import config
from model.utils import save_figure, save_table, titre


def detect_outliers_iqr(X, factor=config.OUTLIER_FACTOR_DETECTION):
    """Masque booléen des valeurs hors de [Q1 - f*IQR ; Q3 + f*IQR]."""
    q1, q3 = X.quantile(0.25), X.quantile(0.75)
    iqr = q3 - q1
    bas, haut = q1 - factor * iqr, q3 + factor * iqr
    return (X < bas) | (X > haut)


def outliers_summary(df, factor=config.OUTLIER_FACTOR_DETECTION):
    X = df.drop(columns=[config.TARGET])
    y = df[config.TARGET]
    masque = detect_outliers_iqr(X, factor)

    resume = pd.DataFrame({
        "Variable": X.columns,
        "Nb outliers": masque.sum().values,
        "% outliers": (masque.mean() * 100).round(2).values,
        "% fraudes parmi les outliers": [
            round(float(y[masque[c]].mean() * 100), 1) if masque[c].any() else float("nan")
            for c in X.columns
        ],
    }).sort_values("% outliers", ascending=False).reset_index(drop=True)
    return resume, masque


def plot_outliers(df, resume):
    X = df.drop(columns=[config.TARGET])
    Z = (X - X.mean()) / X.std()
    long = Z.melt(var_name="Variable", value_name="Valeur standardisée")

    fig, axes = plt.subplots(1, 2, figsize=(18, 7),
                             gridspec_kw={"width_ratios": [2.2, 1]})
    sns.boxplot(data=long, x="Variable", y="Valeur standardisée", color="#9db8ee",
                fliersize=2, ax=axes[0])
    axes[0].tick_params(axis="x", rotation=90)
    axes[0].set_title("Boxplots des variables standardisées")

    ordre = resume.head(15)
    sns.barplot(data=ordre, x="% outliers", y="Variable", color="#e08a5b", ax=axes[1])
    axes[1].set_title("15 variables avec le plus d'outliers (IQR x 1,5)")
    fig.tight_layout()
    save_figure(fig, "08_valeurs_aberrantes")


def analyze_outliers(df):
    titre("ÉTAPE 3 - VALEURS ABERRANTES")
    resume, masque = outliers_summary(df)
    print(resume.head(10).to_string(index=False))
    save_table(resume, "outliers_par_variable")
    plot_outliers(df, resume)

    y = df[config.TARGET]
    a_outlier = masque.any(axis=1)
    taux_avec = y[a_outlier].mean() * 100
    taux_sans = y[~a_outlier].mean() * 100
    print(f"\n{a_outlier.mean() * 100:.1f} % des lignes ont au moins un outlier.")
    print(f"Taux de fraude : {taux_avec:.1f} % (lignes avec outlier) "
          f"vs {taux_sans:.1f} % (lignes sans outlier).")
    print("\nInterprétation : en détection de fraude, une transaction atypique "
          "est souvent la fraude elle-même -> on ne SUPPRIME PAS les outliers.")
    print(f"Choix : on les écrête (clipping) à {config.OUTLIER_FACTOR_CLIPPING} x IQR "
          "(valeurs extrêmes seulement), avec des bornes apprises sur le train "
          "uniquement, pour limiter leur influence sur le noyau RBF du SVM.")

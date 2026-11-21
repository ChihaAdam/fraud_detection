"""Description du modèle SVM : texte + figures pour la présentation.

Les figures sont dessinées en 2D sur les deux variables les plus discriminantes
(pour pouvoir visualiser hyperplan, marge et vecteurs de support).
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from model import config
from model.utils import save_figure, titre

DESCRIPTION = """
DÉFINITION
  Le SVM (Support Vector Machine / Séparateur à Vaste Marge) est un classifieur
  supervisé qui cherche l'hyperplan  w.x + b = 0  séparant les deux classes avec
  la MARGE MAXIMALE (distance 2/||w|| entre les deux classes).

IDÉES CLÉS
  * Vecteurs de support : les points les plus proches de la frontière ; ce sont
    les seuls qui définissent l'hyperplan.
  * Paramètre C : compromis marge large / erreurs tolérées (soft margin).
      C petit -> marge large, plus d'erreurs tolérées (risque de sous-apprentissage)
      C grand -> marge étroite, peu d'erreurs (risque de sur-apprentissage)
  * Astuce du noyau (kernel trick) : pour des données non séparables linéairement,
    on les projette implicitement dans un espace de plus grande dimension.
      Linéaire : K(x,z) = x.z
      RBF      : K(x,z) = exp(-gamma * ||x - z||^2)
  * gamma (noyau RBF) : portée d'influence d'un point (grand = frontière très
    sinueuse, petit = frontière lisse).

ÉTAPES DE NOTRE PIPELINE
  1. Nettoyage + découpage train/test stratifié (80/20)
  2. Écrêtage des valeurs extrêmes (OutlierClipper)
  3. Normalisation StandardScaler (le SVM utilise des distances)
  4. Sélection des k meilleures variables (SelectKBest, test ANOVA)
  5. Entraînement du SVC ; GridSearchCV (CV=4) sur k, noyau, C, gamma
  6. Évaluation sur le test : matrice de confusion, Accuracy, Precision, Recall, F1
"""


def print_svm_description():
    titre("ÉTAPE 6 - DESCRIPTION DU MODÈLE SVM")
    print(DESCRIPTION)


def _tracer_frontiere(ax, clf, X, y, titre_ax):
    x_min, x_max = np.percentile(X[:, 0], [1, 99])
    y_min, y_max = np.percentile(X[:, 1], [1, 99])
    mx, my = (x_max - x_min) * 0.15, (y_max - y_min) * 0.15
    xx, yy = np.meshgrid(np.linspace(x_min - mx, x_max + mx, 300),
                         np.linspace(y_min - my, y_max + my, 300))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    ax.contourf(xx, yy, Z, levels=[-np.inf, 0, np.inf],
                colors=[config.PALETTE["Normale"], config.PALETTE["Fraude"]], alpha=0.12)
    ax.contour(xx, yy, Z, levels=[-1, 0, 1], colors="k",
               linestyles=["--", "-", "--"], linewidths=[1, 2, 1])
    for classe, nom in config.LABELS.items():
        m = y == classe
        ax.scatter(X[m, 0], X[m, 1], s=14, alpha=0.6, c=config.PALETTE[nom], label=nom)
    ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=70,
               facecolors="none", edgecolors="k", linewidths=0.8, label="Vecteurs de support")
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_title(f"{titre_ax}\n({len(clf.support_vectors_)} vecteurs de support)", fontsize=10)


def plot_svm_illustrations(X_train, y_train, scores):
    """Deux figures : (1) noyau linéaire vs RBF ; (2) effet de C (marge)."""
    f1, f2 = scores["Variable"].iloc[:2]
    X2 = StandardScaler().fit_transform(X_train[[f1, f2]])
    y = y_train.to_numpy()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _tracer_frontiere(axes[0], SVC(kernel="linear", C=1).fit(X2, y), X2, y,
                      "Noyau linéaire (hyperplan + marge)")
    _tracer_frontiere(axes[1], SVC(kernel="rbf", C=1, gamma="scale").fit(X2, y), X2, y,
                      "Noyau RBF (frontière non linéaire)")
    for ax in axes:
        ax.set_xlabel(f1)
        ax.set_ylabel(f2)
    axes[0].legend(loc="lower left", fontsize=8)
    fig.suptitle(f"SVM sur les 2 variables les plus discriminantes ({f1}, {f2})", y=1.02)
    save_figure(fig, "13_svm_noyaux")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, C in zip(axes, [0.01, 100]):
        _tracer_frontiere(ax, SVC(kernel="linear", C=C).fit(X2, y), X2, y, f"C = {C}")
        ax.set_xlabel(f1)
        ax.set_ylabel(f2)
    fig.suptitle("Effet de C : C petit = marge large / C grand = marge étroite", y=1.02)
    save_figure(fig, "14_svm_effet_C")

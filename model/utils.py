"""Petites fonctions utilitaires : titres, sauvegarde des figures et tableaux."""
import matplotlib.pyplot as plt

from model import config


def titre(texte):
    print("\n" + "=" * 78)
    print(texte)
    print("=" * 78)


def save_figure(fig, nom):
    """Enregistre la figure dans resultats/figures/ puis l'affiche (si activé)."""
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    chemin = config.FIGURES_DIR / f"{nom}.png"
    fig.savefig(chemin, dpi=150, bbox_inches="tight")
    print(f"  [figure] {chemin.relative_to(config.BASE_DIR)}")
    if config.SHOW_PLOTS:
        plt.show()
    plt.close(fig)


def save_table(df, nom, index=False):
    """Enregistre un DataFrame dans resultats/tables/ en CSV."""
    config.TABLES_DIR.mkdir(parents=True, exist_ok=True)
    chemin = config.TABLES_DIR / f"{nom}.csv"
    df.to_csv(chemin, index=index, encoding="utf-8-sig")
    print(f"  [tableau] {chemin.relative_to(config.BASE_DIR)}")

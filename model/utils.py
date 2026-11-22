"""Petites fonctions utilitaires : titres, sauvegarde des figures, tableaux et modèle."""
import joblib
import matplotlib.pyplot as plt

import config


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


def save_model(model, n_features):
    """Enregistre le modèle entraîné (et le nombre de variables attendu) pour l'API."""
    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "n_features": n_features}, config.MODEL_PATH)
    print(f"  [modèle] {config.MODEL_PATH.relative_to(config.BASE_DIR)}")


def load_model():
    """Charge le modèle servi par l'API ; échoue clairement s'il n'existe pas."""
    if not config.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {config.MODEL_PATH}. Lancez d'abord "
            "'python -m model.main' pour l'entraîner."
        )
    return joblib.load(config.MODEL_PATH)

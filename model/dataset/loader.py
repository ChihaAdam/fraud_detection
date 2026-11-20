"""Chargement de la dataset NearMiss choisie (A, B, C, D ou E)."""
import pandas as pd

from model import config


def load_dataset(cls=config.DATASET_NAME):
    """Retourne le DataFrame complet (features + colonne Class)."""
    chemin = config.DATASET_DIR / f"creditcard_nearmiss_{cls}.csv"
    return pd.read_csv(chemin)


def split_xy(df):
    """Sépare les caractéristiques X et la cible y."""
    return df.drop(columns=[config.TARGET]), df[config.TARGET]

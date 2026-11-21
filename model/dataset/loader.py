"""Chargement de la dataset NearMiss choisie (A, B, C, D ou E)."""
import pandas as pd

import config


def load_dataset(cls=config.DATASET_NAME):
    chemin = config.DATASET_DIR / f"creditcard_nearmiss_{cls}.csv"
    return pd.read_csv(chemin)


def split_xy(df):
    return df.drop(columns=[config.TARGET]), df[config.TARGET]

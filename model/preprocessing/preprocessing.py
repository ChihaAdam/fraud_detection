"""Étape 4 : pré-traitement.

Tout ce qui "apprend" des données (bornes des outliers, moyenne/écart-type)
est placé dans le Pipeline et appris sur le train uniquement, pour éviter
toute fuite d'information vers le test.
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split

from model import config
from model.dataset.loader import split_xy
from model.utils import titre


class OutlierClipper(BaseEstimator, TransformerMixin):
    """Écrête chaque variable à [Q1 - f*IQR ; Q3 + f*IQR] (bornes apprises au fit)."""

    def __init__(self, factor=config.OUTLIER_FACTOR_CLIPPING):
        self.factor = factor

    def fit(self, X, y=None):
        X = np.asarray(X, dtype=float)
        q1, q3 = np.percentile(X, 25, axis=0), np.percentile(X, 75, axis=0)
        iqr = q3 - q1
        self.lower_ = q1 - self.factor * iqr
        self.upper_ = q3 + self.factor * iqr
        return self

    def transform(self, X):
        return np.clip(np.asarray(X, dtype=float), self.lower_, self.upper_)


def clean_data(df):
    """Supprime les doublons et les lignes avec valeurs manquantes."""
    n0 = len(df)
    df = df.drop_duplicates().dropna().reset_index(drop=True)
    print(f"Nettoyage : {n0 - len(df)} ligne(s) supprimée(s) "
          f"(doublons / valeurs manquantes) -> {len(df)} lignes restantes.")
    return df


def split_data(df):
    """Découpage train / test stratifié (80 % / 20 %)."""
    X, y = split_xy(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, stratify=y,
        random_state=config.RANDOM_STATE,
    )
    print(f"Train : {X_train.shape[0]} lignes | Test : {X_test.shape[0]} lignes "
          f"(stratifié, random_state={config.RANDOM_STATE})")
    print(f"Fraudes -> train : {int(y_train.sum())} | test : {int(y_test.sum())}")
    return X_train, X_test, y_train, y_test


def preprocess(df):
    """Nettoyage + split. Les étapes apprises (clipping, scaling) sont dans le Pipeline."""
    titre("ÉTAPE 4 - PRÉ-TRAITEMENT")
    df = clean_data(df)
    X_train, X_test, y_train, y_test = split_data(df)
    print("\nDans le Pipeline SVM (appris sur le train uniquement) :")
    print(f"  1. OutlierClipper ({config.OUTLIER_FACTOR_CLIPPING} x IQR)")
    print("  2. StandardScaler (moyenne 0, écart-type 1) - obligatoire pour un SVM")
    return X_train, X_test, y_train, y_test

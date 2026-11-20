"""Étape 1 : afficher et interpréter les données."""
from model import config
from model.utils import titre


def display_data(df):
    titre("ÉTAPE 1 - AFFICHAGE ET INTERPRÉTATION DES DONNÉES")

    print(f"\nDimensions : {df.shape[0]} lignes x {df.shape[1]} colonnes")
    print("\n--- Aperçu (5 premières lignes) ---")
    print(df.head().to_string())

    print("\n--- Types des colonnes ---")
    df.info()

    print("\n--- Statistiques descriptives ---")
    print(df.describe().T.round(3).to_string())

    n_manquantes = int(df.isna().sum().sum())
    n_doublons = int(df.duplicated().sum())
    print(f"\nValeurs manquantes : {n_manquantes}")
    print(f"Lignes dupliquées  : {n_doublons}")

    comptes = df[config.TARGET].value_counts().sort_index()
    print("\n--- Répartition des classes ---")
    for classe, n in comptes.items():
        print(f"  {config.LABELS[classe]:8s} (Class={classe}) : {n} "
              f"({n / len(df) * 100:.1f} %)")

    _interpreter(df, n_manquantes, n_doublons, comptes)


def _interpreter(df, n_manquantes, n_doublons, comptes):
    print("\n--- Interprétation ---")
    print("* Données : transactions par carte bancaire (Kaggle 'Credit Card Fraud').")
    print("* V1..V28 : composantes issues d'une ACP (variables anonymisées, déjà")
    print("  centrées) ; 'Time' = secondes depuis la 1re transaction ; 'Amount' = montant.")
    print("* Class : 1 = fraude, 0 = transaction normale.")
    print(f"* La dataset {config.DATASET_NAME} a été obtenue par sous-échantillonnage "
          "NearMiss-1 du jeu original très déséquilibré (0,17 % de fraudes).")
    equilibre = comptes.min() / comptes.max()
    print(f"* Rapport minorité/majorité = {equilibre:.2f} -> "
          f"{'classes équilibrées' if equilibre > 0.9 else 'classes déséquilibrées'} : "
          "l'accuracy est donc fiable, mais on suivra aussi le Recall (fraudes ratées).")
    print(f"* {n_manquantes} valeur manquante -> pas d'imputation nécessaire.")
    if n_doublons:
        print(f"* {n_doublons} doublons détectés -> seront supprimés au pré-traitement "
              "(sinon risque de fuite entre train et test).")
    print("* Échelles très différentes (Time ~ 10^5, Amount ~ 10^2, Vi ~ 1) -> "
          "normalisation indispensable pour un SVM.")

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

import ml_models
from ml_models import (svm_model, decision_tree_model,
                       logistic_regression_model, evaluate_model)

BASE = Path(__file__).parent
DATASET_DIR = BASE / "dataset"
RESULTS_DIR = Path(ml_models.__file__).parent / "resultats"   # dossier du vrai package


if __name__ == "__main__":
    resultats = []

    for cls in ["A", "B", "C", "D", "E"]:
        # 1) Charger le dataset NearMiss
        df = pd.read_csv(DATASET_DIR / f"creditcard_nearmiss_{cls}.csv")
        X = df.drop(columns=["Class"])
        y = df["Class"]

        # 2) Séparer train (80 %) / test (20 %)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        # 3) Tester les 3 algorithmes
        modeles = {
            "SVM": svm_model(),
            "Decision Tree": decision_tree_model(),
            "Logistic Regression": logistic_regression_model(),
        }
        for nom, modele in modeles.items():
            resultats.append(
                evaluate_model(nom, modele, X_train, X_test, y_train, y_test, cls)
            )

    # 4) Afficher et sauvegarder le tableau dans ml_models/resultats/
    tableau = pd.DataFrame(resultats).round(4)
    print(tableau.to_string(index=False))

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    tableau.to_csv(RESULTS_DIR / "resultats.csv", index=False)
    print("\nRésultats sauvegardés dans :", RESULTS_DIR)





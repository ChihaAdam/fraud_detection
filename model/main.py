"""Point d'entrée : exécute toutes les étapes du projet avec SVM sur la dataset A.

Lancer depuis le dossier projetML :   python -m model.main
ou directement :                      python model/main.py [--no-show]
"""
import argparse
import sys
from pathlib import Path

# permet aussi `python main.py` depuis le dossier model/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model import config
from model.dataset.loader import load_dataset
from model.exploration import display_data, visualize_data, analyze_outliers
from model.preprocessing.preprocessing import preprocess
from model.preprocessing import analyze_features, get_selected_features
from model.ml_models import (print_svm_description, plot_svm_illustrations,
                             tune_svm, cv_results_table, evaluate_svm, summary_tables)


def main():
    # 1-3) Données : affichage, visualisation seaborn, valeurs aberrantes
    df = load_dataset(config.DATASET_NAME)
    display_data(df)
    visualize_data(df)
    analyze_outliers(df)

    # 4) Pré-traitement (nettoyage + split train/test)
    X_train, X_test, y_train, y_test = preprocess(df)

    # 5) Sélection des caractéristiques (scores sur le train)
    scores = analyze_features(X_train, y_train)

    # 6) Description du modèle + figures explicatives
    print_svm_description()
    plot_svm_illustrations(X_train, y_train, scores)

    # 7) Apprentissage + paramètres optimaux (GridSearchCV, CV = 4)
    grid = tune_svm(X_train, y_train)
    cv_results_table(grid)

    # 8) Évaluation : matrices de confusion, ROC, métriques
    resultats = evaluate_svm(grid, X_train, y_train, X_test, y_test)

    # 9) Tableaux récapitulatifs
    selected = get_selected_features(grid.best_estimator_, X_train.columns)
    summary_tables(grid, resultats, selected, X_train.shape[1])

    print(f"\nTerminé. Résultats dans : {config.RESULTS_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Projet ML - SVM (dataset NearMiss)")
    parser.add_argument("--no-show", action="store_true",
                        help="ne pas afficher les figures (les sauvegarder seulement)")
    args = parser.parse_args()
    if args.no_show:
        config.SHOW_PLOTS = False
    main()

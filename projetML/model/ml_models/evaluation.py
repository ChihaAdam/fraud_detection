from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix)


def evaluate_model(nom, modele, X_train, X_test, y_train, y_test, cls):
    """Entraîne le modèle puis calcule les métriques (Class = 1 -> fraude)."""
    modele.fit(X_train, y_train)
    y_pred = modele.predict(X_test)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    return {
        "Dataset": cls,
        "Modèle": nom,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred, zero_division=0),
        "Fraudes détectées": f"{tp}/{tp + fn}",
        "Fausses alertes": fp,
    }




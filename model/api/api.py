import contextlib
import io
import math
import sys
from pathlib import Path

# permet `python model/api/api.py` comme `python -m model.api.api`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, Response, jsonify, request
from sklearn.metrics import confusion_matrix

import config
from dataset.loader import load_dataset
from preprocessing.preprocessing import preprocess
from utils import load_model

app = Flask(__name__)

_model = None
_n_features = None
_cm = None
_corr = None
_corr_png = None


def get_model():
    """Charge une seule fois le modèle entraîné et sauvegardé par `model.main`."""
    global _model, _n_features
    if _model is None:
        saved = load_model()
        _model, _n_features = saved["model"], saved["n_features"]
    return _model


def get_confusion_matrix():
    """Calcule une seule fois la matrice sur le jeu de test jamais vu au training."""
    global _cm
    if _cm is None:
        model = get_model()
        # `preprocess` affiche des informations de debug : on les garde hors de l'API.
        with contextlib.redirect_stdout(io.StringIO()):
            _, X_test, _, y_test = preprocess(load_dataset())
        if X_test.shape[1] != _n_features:
            raise ValueError(
                f"Le modèle attend {_n_features} variables, le dataset en contient "
                f"{X_test.shape[1]}."
            )
        y_pred = model.predict(X_test)
        # labels explicites pour garantir l'ordre [Normale, Fraude] de config.LABELS.
        _cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    return _cm


def get_correlation_matrix():
    """Matrice de corrélation de Pearson du dataset utilisé par le modèle."""
    global _corr
    if _corr is None:
        _corr = load_dataset().corr(method="pearson")
    return _corr


def _correlation_value(value):
    """Garde des nombres JSON valides (une corrélation indéfinie devient 0)."""
    value = float(value)
    return round(value, 6) if math.isfinite(value) else 0.0


def render_correlation_heatmap(corr):
    """Rend la matrice en PNG (mis en cache) pour un affichage direct."""
    global _corr_png
    if _corr_png is None:
        import matplotlib.pyplot as plt

        labels = [str(col) for col in corr.columns]
        fig, ax = plt.subplots(figsize=(12, 10))
        image = ax.imshow(corr.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(labels)), labels, rotation=90, ha="right", fontsize=7)
        ax.set_yticks(range(len(labels)), labels, fontsize=7)
        ax.set_title(f"Corrélation de Pearson - dataset {config.DATASET_NAME}")
        fig.colorbar(image, ax=ax, shrink=0.8, label="Pearson r")
        fig.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        _corr_png = buffer.getvalue()
    return _corr_png


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Le corps doit être un objet JSON."}), 400

    features = data.get("features")
    if (not isinstance(features, list) or not features
            or any(isinstance(v, bool) or not isinstance(v, (int, float))
                   or not math.isfinite(v) for v in features)):
        return jsonify({"error": "'features' doit être une liste de nombres."}), 400

    model = get_model()
    if len(features) != _n_features:
        return jsonify({"error": f"'features' doit contenir {_n_features} valeurs."}), 400

    pred = int(model.predict([features])[0])
    return jsonify({"prediction": pred, "label": config.LABELS[pred]})


@app.route("/confusion-matrix", methods=["GET"])
def confusion_matrix_endpoint():
    """Renvoie la matrice de confusion du modèle sur le jeu de test (20 %)."""
    try:
        cm = get_confusion_matrix()
    except (FileNotFoundError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 503

    tn, fp, fn, tp = (int(v) for v in cm.ravel())
    labels = [config.LABELS[0], config.LABELS[1]]
    return jsonify({
        "dataset": config.DATASET_NAME,
        "split": "test",
        "rows": "Classe réelle",
        "columns": "Classe prédite",
        "labels": labels,
        "matrix": cm.tolist(),
        "values": {
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
        },
    })


@app.route("/correlation-matrix", methods=["GET"])
def correlation_matrix_endpoint():
    """Corrélations de Pearson du dataset, en JSON ou en PNG avec ?format=png."""
    try:
        corr = get_correlation_matrix()
    except (FileNotFoundError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 503

    if request.args.get("format", "").lower() == "png":
        return Response(render_correlation_heatmap(corr), mimetype="image/png")

    target_corr = corr[config.TARGET].drop(config.TARGET)
    return jsonify({
        "dataset": config.DATASET_NAME,
        "method": "pearson",
        "target": config.TARGET,
        "labels": [str(col) for col in corr.columns],
        "matrix": [[_correlation_value(v) for v in row] for row in corr.to_numpy()],
        "target_correlations": {
            str(col): _correlation_value(value) for col, value in target_corr.items()
        },
    })


if __name__ == "__main__":
    app.run(debug=True)

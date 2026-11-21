import math
import sys
from pathlib import Path

# permet `python model/api/api.py` comme `python -m model.api.api`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
import joblib
from flask import Flask, jsonify, request
from dataset.loader import load_dataset, split_xy
from ml_models.svm import build_svm_pipeline
from preprocessing.preprocessing import clean_data

app = Flask(__name__)

_model = None
_n_features = None


def get_model():
    """Charge le modèle sauvegardé, ou l'entraîne une seule fois et le sauvegarde."""
    global _model, _n_features
    if _model is None:
        if config.MODEL_PATH.exists():
            saved = joblib.load(config.MODEL_PATH)
            _model, _n_features = saved["model"], saved["n_features"]
        else:
            X, y = split_xy(clean_data(load_dataset()))
            _model = build_svm_pipeline().fit(X, y)
            _n_features = X.shape[1]
            joblib.dump({"model": _model, "n_features": _n_features},
                        config.MODEL_PATH)
    return _model


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
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


if __name__ == "__main__":
    app.run(debug=True)

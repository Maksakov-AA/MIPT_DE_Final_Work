import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
import os

def evaluate(model_path, test_data_path, metrics_path):
    df = pd.read_csv(test_data_path)
    X_test = df.drop(columns=["target"])
    y_true = df["target"]

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred)
    }

    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    evaluate("models/model.pkl", "data/processed/test.csv", "results/metrics.json")
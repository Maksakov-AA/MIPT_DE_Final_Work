import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

def train_model(input_path, model_path):
    df = pd.read_csv(input_path)

    X = df.drop(columns=["target"])
    y = df["target"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_model("data/processed/train.csv", "models/model.pkl")
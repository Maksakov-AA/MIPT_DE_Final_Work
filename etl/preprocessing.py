import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def preprocess(input_path, output_path):
    df = pd.read_csv(input_path)

    # Целевая переменная
    y = df["diagnosis"].map({"M": 1, "B": 0})
    
    # Признаки
    X = df.drop(columns=["diagnosis"])

    # Масштабирование
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Собираем итоговый датафрейм
    df_out = pd.DataFrame(X_scaled, columns=X.columns)
    df_out["target"] = y

    # Сохраняем
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_out.to_csv(output_path, index=False)

if __name__ == "__main__":
    preprocess("data/train.csv", "data/processed/train.csv")
    preprocess("data/test.csv", "data/processed/test.csv")

import pandas as pd
from sklearn.model_selection import train_test_split
import os

def load_and_split():
    # Заголовки по описанию датасета
    column_names = [
        "id", "diagnosis",
        "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
        "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
        "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
        "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
        "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
        "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
    ]

    df = pd.read_csv("wdbc_data.csv", header=None, names=column_names)

    df = df.drop(columns=["id"])

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs("data", exist_ok=True)
    train_df.to_csv("data/train.csv", index=False)
    test_df.to_csv("data/test.csv", index=False)

if __name__ == "__main__":
    load_and_split()
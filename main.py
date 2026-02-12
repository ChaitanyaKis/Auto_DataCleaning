import pandas as pd
import os

from src.cleaner import AutoCleaner
from src.encoder import Encoder
from src.scaler import Scaler
from src.visualizer import Visualizer


def find_dataset(path="data/raw"):
    for file in os.listdir(path):
        if file.endswith(".csv"):
            return os.path.join(path, file)
    raise FileNotFoundError("No CSV dataset found in data/raw/")


def main():

    dataset_path = find_dataset()

    df = pd.read_csv(dataset_path)

    # ---------- VISUALIZE BEFORE CLEAN ----------
    visualizer = Visualizer()
    visualizer.plot_outliers(df)

    # ---------- CLEAN ----------
    cleaner = AutoCleaner()
    df_clean = cleaner.clean(df)

    # ---------- ENCODE ----------
    encoder = Encoder()
    df_encoded = encoder.transform(df_clean)

    # ---------- SCALE ----------
    scaler = Scaler()
    df_scaled = scaler.transform(df_encoded)

    # ---------- SAVE ----------
    os.makedirs("data/output", exist_ok=True)
    df_scaled.to_csv("data/output/cleaned_data.csv", index=False)

    print("Processing complete.")
    print("Cleaned dataset saved to: data/output/cleaned_data.csv")


if __name__ == "__main__":
    main()

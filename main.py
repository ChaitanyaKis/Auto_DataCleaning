import os
import pandas as pd
from src.cleaner import AutoCleaner


def find_dataset():
    raw_path = "data/raw"
    files = [f for f in os.listdir(raw_path) if f.endswith(".csv")]

    if not files:
        raise FileNotFoundError("❌ No CSV file found inside data/raw")

    return os.path.join(raw_path, files[0])


def main():
    print("\n🔎 Auto Detecting Dataset...\n")

    dataset_path = find_dataset()
    print(f"📂 Found Dataset: {dataset_path}")

    df = pd.read_csv(dataset_path)

    cleaner = AutoCleaner()
    cleaned_df = cleaner.clean(df)

    os.makedirs("data/output", exist_ok=True)
    output_path = "data/output/cleaned_data.csv"
    cleaned_df.to_csv(output_path, index=False)

    print("\n✅ Cleaning Complete.")
    print(f"📁 Saved to: {output_path}\n")


if __name__ == "__main__":
    main()

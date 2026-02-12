import pandas as pd
import numpy as np
from pathlib import Path


class DataQualityEvaluator:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def evaluate(self):
        print("\n🔎 Evaluating Cleaned Dataset Quality\n")

        if not self.file_path.exists():
            print("❌ File not found.")
            return

        df = pd.read_csv(self.file_path)

        total_cells = df.shape[0] * df.shape[1]

        # ---------------- Missing Values ----------------
        missing_count = df.isna().sum().sum()
        missing_ratio = missing_count / total_cells

        # ---------------- Duplicates ----------------
        duplicate_count = df.duplicated().sum()

        # ---------------- Data Types ----------------
        object_cols = df.select_dtypes(include="object").shape[1]
        numeric_cols = df.select_dtypes(include=np.number).shape[1]

        # ---------------- Outlier Check ----------------
        outlier_count = 0
        for col in df.select_dtypes(include=np.number).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_count += ((df[col] < lower) | (df[col] > upper)).sum()

        # ---------------- Skewness ----------------
        skewed_cols = 0
        for col in df.select_dtypes(include=np.number).columns:
            if abs(df[col].skew()) > 1:
                skewed_cols += 1

        # ---------------- Memory Usage ----------------
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2

        # ---------------- Quality Score ----------------
        score = 100

        score -= missing_ratio * 40
        score -= (duplicate_count / len(df)) * 20
        score -= min(outlier_count / total_cells, 0.2) * 20
        score -= (skewed_cols / max(1, numeric_cols)) * 20

        score = max(0, round(score, 2))

        # ---------------- Print Report ----------------
        print("📊 DATA QUALITY REPORT")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print(f"Missing Values: {missing_count}")
        print(f"Duplicate Rows: {duplicate_count}")
        print(f"Numeric Columns: {numeric_cols}")
        print(f"Object Columns: {object_cols}")
        print(f"Remaining Outliers: {outlier_count}")
        print(f"Heavily Skewed Columns: {skewed_cols}")
        print(f"Memory Usage: {memory_mb:.2f} MB")
        print("\n🏆 QUALITY SCORE:", score, "/ 100\n")


if __name__ == "__main__":
    evaluator = DataQualityEvaluator("data/output/cleaned_data.csv")
    evaluator.evaluate()

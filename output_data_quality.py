import pandas as pd
import numpy as np
from pathlib import Path


class DataQualityEvaluator:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    # --------------------------------------------------
    # MAIN EVALUATION
    # --------------------------------------------------
    def evaluate(self):

        print("\nDATASET QUALITY EVALUATION REPORT\n")

        if not self.file_path.exists():
            print("ERROR: Dataset file not found.\n")
            return

        df = pd.read_csv(self.file_path)

        rows, cols = df.shape
        total_cells = rows * cols if rows and cols else 1

        # --------------------------------------------------
        # Missing Values
        # --------------------------------------------------
        missing_count = df.isna().sum().sum()
        missing_ratio = missing_count / total_cells

        # --------------------------------------------------
        # Duplicate Rows
        # --------------------------------------------------
        duplicate_count = df.duplicated().sum()
        duplicate_ratio = duplicate_count / rows if rows else 0

        # --------------------------------------------------
        # Data Types
        # --------------------------------------------------
        numeric_cols = df.select_dtypes(include=np.number).columns
        object_cols = df.select_dtypes(include="object").columns

        # --------------------------------------------------
        # Outlier Detection (IQR)
        # --------------------------------------------------
        outlier_count = 0

        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outlier_count += ((df[col] < lower) | (df[col] > upper)).sum()

        outlier_ratio = outlier_count / total_cells

        # --------------------------------------------------
        # Skewness Check
        # --------------------------------------------------
        skewed_cols = [col for col in numeric_cols if abs(df[col].skew()) > 1]
        skew_ratio = len(skewed_cols) / max(1, len(numeric_cols))

        # --------------------------------------------------
        # Scaling Quality Check
        # --------------------------------------------------
        scaled_columns = 0

        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()

            # realistic scaled range
            if abs(mean) < 0.25 and 0.5 < std < 1.5:
                scaled_columns += 1

        scaling_ratio = scaled_columns / max(1, len(numeric_cols))

        # --------------------------------------------------
        # Encoding Check
        # --------------------------------------------------
        encoded_ok = len(object_cols) == 0

        # --------------------------------------------------
        # Memory Usage
        # --------------------------------------------------
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2

        # --------------------------------------------------
        # QUALITY SCORE (PROFESSIONAL METRIC)
        # --------------------------------------------------
        score = 100.0

        # Missing values penalty (max -40)
        score -= min(40, missing_ratio * 100)

        # Duplicate penalty (max -15)
        score -= min(15, duplicate_ratio * 100)

        # Outlier penalty (max -15)
        score -= min(15, outlier_ratio * 100)

        # Skew penalty (max -15)
        score -= skew_ratio * 15

        # Scaling penalty (max -15)
        score -= (1 - scaling_ratio) * 15

        # Encoding penalty
        if not encoded_ok:
            score -= 10

        # Clamp score
        score = max(0, min(100, round(score, 2)))

        # --------------------------------------------------
        # REPORT OUTPUT
        # --------------------------------------------------
        print("Dataset Overview")
        print("------------------")
        print(f"Rows: {rows}")
        print(f"Columns: {cols}")
        print(f"Memory Usage: {memory_mb:.2f} MB\n")

        print("Integrity Checks")
        print("------------------")
        print(f"Missing Values: {missing_count}")
        print(f"Duplicate Rows: {duplicate_count}")
        print(f"Remaining Outliers: {outlier_count}")
        print(f"Highly Skewed Columns: {len(skewed_cols)}\n")

        print("Feature Validation")
        print("------------------")
        print(f"Numeric Columns: {len(numeric_cols)}")
        print(f"Non-Numeric Columns Remaining: {len(object_cols)}")
        print(f"Properly Scaled Columns: {scaled_columns}/{len(numeric_cols)}")
        print(f"Encoding Status: {'PASS' if encoded_ok else 'FAIL'}\n")

        print("Final Assessment")
        print("------------------")
        print(f"Quality Score: {score} / 100\n")

        # --------------------------------------------------
        # RETURN RESULTS
        # --------------------------------------------------
        return {
            "rows": rows,
            "columns": cols,
            "missing": missing_count,
            "duplicates": duplicate_count,
            "outliers": outlier_count,
            "skewed_columns": len(skewed_cols),
            "scaled_columns": scaled_columns,
            "encoded": encoded_ok,
            "memory_mb": round(memory_mb, 2),
            "score": score
        }


# --------------------------------------------------
# CLI ENTRY
# --------------------------------------------------
if __name__ == "__main__":
    evaluator = DataQualityEvaluator("data/output/cleaned_data.csv")
    evaluator.evaluate()

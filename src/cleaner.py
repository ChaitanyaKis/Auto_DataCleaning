import pandas as pd
import numpy as np
from src.profiler import DataProfiler
from src.optimizer import MemoryOptimizer
from src.utils import cap_outliers_iqr


class AutoCleaner:

    def __init__(self):
        self.profiler = DataProfiler()
        self.optimizer = MemoryOptimizer()

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        print("\n=== Data Cleaning Pipeline Initiated ===\n")

        df = df.copy()

        # --------------------------------------------------
        # 1. Dataset Profiling
        # --------------------------------------------------
        profile = self.profiler.profile(df)

        # --------------------------------------------------
        # 2. Remove High Null Columns
        # --------------------------------------------------
        null_threshold = 0.7
        drop_cols = profile[profile["null_ratio"] > null_threshold].index.tolist()

        if drop_cols:
            df = df.drop(columns=drop_cols)

        print(f"[INFO] Removed {len(drop_cols)} columns with >70% missing values")

        # --------------------------------------------------
        # 3. Remove Duplicates
        # --------------------------------------------------
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed_duplicates = initial_rows - len(df)

        print(f"[INFO] Removed {removed_duplicates} duplicate rows")

        # --------------------------------------------------
        # 4. Clean Object Columns
        # --------------------------------------------------
        object_cols = df.select_dtypes(include="object").columns

        for col in object_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"": np.nan, "nan": np.nan})
            )

            # Attempt numeric conversion (if majority numeric)
            try:
                converted = pd.to_numeric(df[col])
                if converted.notna().sum() > 0.8 * len(df):
                    df[col] = converted
            except Exception:
                pass

        print(f"[INFO] Standardized {len(object_cols)} text columns")

        # --------------------------------------------------
        # 5. Handle Missing Values
        # --------------------------------------------------
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("missing")

        print("[INFO] Missing values imputed")

        # --------------------------------------------------
        # 6. Outlier Capping (IQR)
        # --------------------------------------------------
        numeric_cols = df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            df[col] = cap_outliers_iqr(df[col])

        print("[INFO] Outliers capped using IQR method")

        # --------------------------------------------------
        # 7. Skewness Correction
        # --------------------------------------------------
        for col in numeric_cols:
            skewness = df[col].skew()

            if abs(skewness) > 1:
                min_val = df[col].min()

                if min_val <= 0:
                    df[col] = np.log1p(df[col] - min_val + 1)
                else:
                    df[col] = np.log1p(df[col])

        print("[INFO] Skewed numerical features transformed")

        # --------------------------------------------------
        # 8. Memory Optimization
        # --------------------------------------------------
        df = self.optimizer.optimize(df)

        print("[INFO] Memory optimization completed")

        print("\n=== Data Cleaning Pipeline Completed ===\n")

        return df

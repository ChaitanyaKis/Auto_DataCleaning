import pandas as pd


class MemoryOptimizer:

    def optimize(self, df: pd.DataFrame) -> pd.DataFrame:

        for col in df.columns:

            if df[col].dtype == "int64":
                df[col] = pd.to_numeric(df[col], downcast="integer")

            elif df[col].dtype == "float64":
                df[col] = pd.to_numeric(df[col], downcast="float")

            elif df[col].dtype == "object":
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype("category")

        return df

import pandas as pd
from sklearn.preprocessing import StandardScaler


class Scaler:

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        numeric_cols = df.select_dtypes(include="number").columns

        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        return df

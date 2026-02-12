import pandas as pd


class Encoder:

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        categorical_cols = df.select_dtypes(include="object").columns

        for col in categorical_cols:
            if df[col].nunique() <= 15:
                df = pd.get_dummies(df, columns=[col], drop_first=True)
            else:
                df[col] = df[col].astype("category").cat.codes

        return df

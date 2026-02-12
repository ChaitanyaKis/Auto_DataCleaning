import pandas as pd


class DataProfiler:

    def profile(self, df: pd.DataFrame) -> pd.DataFrame:
        profile = pd.DataFrame()
        profile["dtype"] = df.dtypes
        profile["null_ratio"] = df.isnull().mean()
        profile["unique_count"] = df.nunique()
        return profile

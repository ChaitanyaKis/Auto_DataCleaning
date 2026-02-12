import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


class Visualizer:

    def plot_outliers(self, df: pd.DataFrame, save_dir="reports"):
        os.makedirs(save_dir, exist_ok=True)

        numeric_cols = df.select_dtypes(include="number").columns

        for col in numeric_cols:
            plt.figure()
            sns.boxplot(x=df[col])
            plt.title(f"Boxplot - {col}")
            plt.savefig(f"{save_dir}/{col}_boxplot.png")
            plt.close()

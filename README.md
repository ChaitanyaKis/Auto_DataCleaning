# 📦 Automated Data Cleaning Pipeline

A reusable, dataset-agnostic data cleaning solution that standardizes, imputes, and prepares structured data for analysis or machine learning workflows with zero manual configuration.

---

## 📌 Purpose

This repository provides a fully automated data cleaning engine capable of:

- Detecting input dataset
- Removing high-null and duplicate entries
- Normalizing text fields
- Handling missing values intelligently
- Detecting and capping outliers
- Correcting skewness
- Optimizing memory usage

The outcome is a production-ready, cleaned CSV suitable for downstream tasks.

---

## 🧩 Features

### ✔ Automatic Dataset Detection
Automatically picks the first CSV file found in `data/raw/`.

### ✔ Column Dropping Based on Missing Data
Columns with >70% missing values are removed.

### ✔ Duplicate Handling
Removes exact duplicates.

### ✔ Text Normalization
Cleans strings (trim, lower-case, missing categorization).

### ✔ Smart Type Conversion
Attempts numeric conversion when appropriate.

### ✔ Missing Value Strategy
- Numerical → Median
- Categorical → “missing”

### ✔ Outlier Capping (IQR)
Limits extreme values rather than removing data.

### ✔ Skewness Correction
Applies log transformation for numeric columns with significant skew.

### ✔ Memory Optimization
Downcasts numeric types and converts suitable text to category.

---

## 📁 Folder Structure

```
Task_1 - DataCleaning/
│
├── data/
│   ├── raw/        # Place any CSV dataset here
│   └── output/     # Cleaned output saved here
│
├── src/
│   ├── cleaner.py      # Core pipeline
│   ├── profiler.py     # Dataset analysis
│   ├── optimizer.py    # Memory optimizer
│   └── utils.py        # Helpers
│
├── main.py                 # Entry script
├── output_data_quality.py  # Output quality evaluation
├── requirements.txt
└── README.md
```




---

## 🚀 Setup

1. Clone repository
2. Create and activate virtual environment
3. Install dependencies


python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt


## ▶️ Usage

1. Place any `.csv` file inside:

data/raw/

2. Run the cleaning pipeline:

python main.pu

3. The cleaned dataset will be saved to:

data/output/cleaned_data.csv

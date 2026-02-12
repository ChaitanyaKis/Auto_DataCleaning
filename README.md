# 📦 Automated Data Cleaning Pipeline

A reusable, dataset-agnostic data cleaning solution that standardizes, imputes, and prepares structured data for analysis or machine learning workflows with zero manual configuration.

---

## 📌 Purpose

This repository provides a fully automated data cleaning engine capable of:

- Detecting input datasets automatically
- Removing high-null columns and duplicate rows
- Normalizing text features
- Handling missing values intelligently
- Detecting and capping outliers
- Correcting skewed distributions
- Optimizing memory usage

The output is a clean, structured CSV ready for analytics, modeling, or visualization.

---

## 🧩 Features

### ✔ Automatic Dataset Detection
Automatically selects the first CSV file found in:

```
data/raw/
```

---

### ✔ Column Removal Based on Missing Data
Columns containing more than **70% missing values** are automatically dropped.

---

### ✔ Duplicate Handling
Removes exact duplicate rows to ensure dataset integrity.

---

### ✔ Text Normalization
Standardizes string values by:
- trimming whitespace  
- converting to lowercase  
- handling empty values  

---

### ✔ Smart Type Conversion
Attempts numeric conversion when appropriate while preserving valid categorical values.

---

### ✔ Missing Value Strategy
| Data Type | Strategy |
|--------|----------|
Numeric | Median Imputation |
Categorical | `"missing"` placeholder |

---

### ✔ Outlier Capping (IQR Method)
Extreme values are capped instead of removed, preserving dataset size.

---

### ✔ Skewness Correction
Automatically applies log transformation to highly skewed numerical features.

---

### ✔ Memory Optimization
Reduces memory footprint by:
- downcasting numeric types
- converting suitable text columns to categorical dtype

---

## 📁 Project Structure

## 📁 Project Structure

```
Task_1 - DataCleaning/
│
├── data/
│   ├── raw/            # Place any CSV dataset here
│   └── output/         # Cleaned dataset saved here
│
├── src/
│   ├── cleaner.py      # Core cleaning pipeline
│   ├── profiler.py     # Dataset profiling logic
│   ├── optimizer.py    # Memory optimization utilities
│   ├── encoder.py      # Categorical encoding module
│   ├── scaler.py       # Feature scaling module
│   ├── visualizer.py   # Outlier visualization (boxplots)
│   └── utils.py        # Helper utilities
│
├── main.py                 # Entry script
├── output_data_quality.py  # Dataset quality evaluation
├── requirements.txt
└── README.md
```


---

## ⚙️ Setup

Clone the repository and install dependencies:

```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Place dataset

Put any `.csv` file inside:

```
data/raw/
```

---

### 2. Run pipeline

```bash
python main.py
```

---

### 3. Output location

The cleaned dataset will be saved automatically to:

```
data/output/cleaned_data.csv
```

---

## 📊 Dataset Quality Evaluation

After cleaning, evaluate the processed dataset:

```bash
python output_data_quality.py
```

This generates a structured quality report including:

- Missing values
- Duplicate rows
- Outlier count
- Skewed columns
- Scaling validation
- Encoding validation
- Memory usage
- Overall quality score

---

## 🎯 Design Goals

This pipeline is designed to be:

- Dataset-agnostic
- Deterministic
- Reproducible
- Efficient
- Production-ready

No manual preprocessing or dataset-specific configuration is required.

---

## 📜 License

This project is intended for educational and evaluation purposes.

---


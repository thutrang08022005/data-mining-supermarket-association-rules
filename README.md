# Data Mining - Supermarket Association Rules

This repository contains the source code and notebooks for the Data Mining final project: **Supermarket Association Rules Mining**.

The project applies frequent itemset mining and association rule mining on the Instacart Market Basket dataset to analyze customer purchasing behavior and generate product, aisle, and department relationship insights.

---

## Important Links

- Source code:  
  https://github.com/thutrang08022005/data-mining-supermarket-association-rules

- Experimental data and result files:  
  https://drive.google.com/drive/folders/1FWy_NC2RRu_T9_hyj0sjAkj3VcEDvOmr?usp=sharing

- Original dataset source:  
  https://www.kaggle.com/c/instacart-market-basket-analysis/data

---

## 1. GitHub Repository Structure

This GitHub repository only contains the source code, notebooks, `.gitignore`, and `README.md`.

The large dataset and generated result files are not uploaded directly to GitHub because their file sizes are too large.

```text
data-mining-supermarket-association-rules/
├── app/
│   └── app.py
│
├── notebooks/
│   ├── 01_check_processed_input.ipynb
│   ├── 02_frequent_itemsets_experiment.ipynb
│   ├── 03_association_rules_analysis.ipynb
│   └── 04_deep_analysis_labeled_data.ipynb
│
├── .gitignore
└── README.md
```

---

## 2. Dataset and Result Files

The full experimental dataset and generated result files are provided through Google Drive:

```text
https://drive.google.com/drive/folders/1FWy_NC2RRu_T9_hyj0sjAkj3VcEDvOmr?usp=sharing
```

The Google Drive folder contains both the original raw dataset, the processed dataset generated after the midterm stage, and the final experiment result files.

```text
data/
├── raw/
│   ├── aisles.csv
│   ├── departments.csv
│   ├── order_products__prior.csv
│   ├── order_products__train.csv
│   ├── orders.csv
│   └── products.csv
│
└── processed/
    ├── basket_data_sample.csv
    ├── basket_matrix_sparse.pkl
    ├── clean_aisles.csv
    ├── clean_departments.csv
    ├── clean_order_products_prior.csv
    ├── clean_orders_prior.csv
    ├── clean_products.csv
    ├── instacart_subset_for_rules.csv
    ├── order_product_pairs_sample.csv
    └── product_mapping_sample.csv

result/
└── generated experiment output files
```

---

## 3. Original Dataset Source

The original raw dataset is based on the **Instacart Market Basket Analysis** dataset from Kaggle.

Dataset source:

```text
https://www.kaggle.com/c/instacart-market-basket-analysis/data
```

The raw dataset contains order history, product information, aisle information, department information, and user purchase records.

---

## 4. Processed Dataset

The processed dataset was generated from the raw Instacart dataset during the midterm stage.

The processed files are used directly for the final experiment, including frequent itemset mining, association rule generation, and deeper product or department-level analysis.

Main processed files include:

```text
data/processed/basket_matrix_sparse.pkl
data/processed/product_mapping_sample.csv
data/processed/instacart_subset_for_rules.csv
data/processed/basket_data_sample.csv
data/processed/order_product_pairs_sample.csv
```

---

## 5. How to Run the Project

### Step 1: Clone this GitHub repository

```bash
git clone https://github.com/thutrang08022005/data-mining-supermarket-association-rules.git
```

### Step 2: Download the dataset and result files

Download the `data/` and `result/` folders from Google Drive:

```text
https://drive.google.com/drive/folders/1FWy_NC2RRu_T9_hyj0sjAkj3VcEDvOmr?usp=sharing
```

### Step 3: Place the downloaded folders into the project root directory

After downloading, the local project folder should have the following structure:

```text
data-mining-supermarket-association-rules/
├── app/
│   └── app.py
│
├── notebooks/
│   ├── 01_check_processed_input.ipynb
│   ├── 02_frequent_itemsets_experiment.ipynb
│   ├── 03_association_rules_analysis.ipynb
│   └── 04_deep_analysis_labeled_data.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
├── result/
│
├── .gitignore
└── README.md
```

### Step 4: Run the notebooks in order

```text
01_check_processed_input.ipynb
02_frequent_itemsets_experiment.ipynb
03_association_rules_analysis.ipynb
04_deep_analysis_labeled_data.ipynb
```

### Step 5: Run the application if needed

```bash
python app/app.py
```

---

## 6. Notes

The `data/` folder is not included directly in this GitHub repository because it contains large raw and processed dataset files.

The `result/` folder is also not included directly in this GitHub repository because it contains generated experiment output files.

To reproduce the experiment correctly, please download the `data/` and `result/` folders from the Google Drive link and place them in the project root directory before running the notebooks or source code.
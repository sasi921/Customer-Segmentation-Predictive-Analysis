# Customer Segmentation & Predictive Analysis

A data mining and machine-learning project that analyzes online retail transactions to identify meaningful customer segments, predict future spending behavior, and generate cluster-based product recommendations.

## Project Summary

The project uses the UCI Online Retail transactional dataset and combines customer segmentation, dimensionality reduction, predictive modeling, and recommendation techniques to support more targeted e-commerce marketing decisions.

The supplied dataset contains **541,909 transactions across 8 columns**. The workflow cleans the transactional data, engineers customer-level behavioral features, applies feature scaling and PCA, clusters customers with K-Means, evaluates the resulting clusters, and then uses the customer groups for predictive spending analysis and product recommendations.

## Main Goals

- Identify distinct customer groups from purchasing behavior.
- Build customer-centric features including RFM-style metrics and behavioral attributes.
- Use PCA to reduce dimensionality and visualize customer groups.
- Determine an appropriate number of clusters using the Elbow Method and Silhouette Score.
- Evaluate cluster quality using multiple clustering metrics.
- Predict future customer spending from historical transaction behavior.
- Recommend products using purchase patterns within each customer segment.

## Machine Learning Workflow

### 1. Data Cleaning

The notebook handles common transaction-data issues including:

- Missing `CustomerID` and product descriptions
- Duplicate records
- Cancelled transactions
- Date conversion and transaction-status creation
- Irregular stock-code and transaction patterns

### 2. Feature Engineering

Customer-level behavioral features are created from the cleaned transaction history, including measures related to:

- Recency
- Frequency
- Monetary behavior
- Product diversity
- Purchase timing
- Customer purchasing patterns

### 3. Scaling and PCA

Features are standardized before clustering. Principal Component Analysis (PCA) is used to reduce dimensionality and make customer clusters easier to analyze and visualize.

### 4. Customer Segmentation

K-Means clustering is evaluated across multiple values of `k`. The final analysis uses **3 customer clusters**.

Cluster evaluation in the notebook reports:

| Metric | Result |
| --- | ---: |
| Number of observations | 4,078 |
| Silhouette Score | 0.5878 |
| Calinski-Harabasz Score | 16,047.15 |
| Davies-Bouldin Score | 0.5018 |

### 5. Cluster Profiling

The project visualizes and compares cluster characteristics using:

- PCA cluster plots
- Cluster distribution analysis
- Radar charts of cluster centroids
- RFM-based customer visualizations

### 6. Recommendation System

The recommendation component analyzes top-selling products within each customer cluster. Customers can then be recommended popular products from their segment that they have not previously purchased.

### 7. Predictive Analysis

The project explores customer-spending prediction using regression models and historical RFM behavior. It also evaluates next-visit spending predictions using metrics including:

- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- R-squared

## Technologies

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Plotly
- SciPy
- Yellowbrick
- Tabulate

## Repository Contents

```text
.
├── Implementation_file.ipynb   # Complete data mining and ML workflow
├── Report.pdf                  # Final academic project report
├── data_sample.csv             # Small sample of the source dataset
├── scripts/
│   └── validate_dataset.py     # Preflight schema/value checks for the dataset
├── tests/
│   └── test_validate_dataset.py# Unit tests for the validator
├── requirements.txt            # Python dependencies
├── .gitignore                  # Local/generated file exclusions
└── README.md                   # Project documentation
```

## Dataset

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository. It contains real transactional data from a UK-based online retailer covering 2010–2011.

The full local `data.csv` used for the analysis is approximately 45 MB. To keep the repository lightweight and reproducible, the repository includes a small sample while the full dataset is excluded from version control.

To run the complete notebook, obtain the Online Retail dataset from UCI, convert/save it as CSV if needed, and place it in the repository root with the filename:

```text
data.csv
```

Before opening the notebook, run the lightweight preflight validator. It checks the expected UCI schema and catches malformed quantity, price, date, and customer-ID values early:

```bash
python scripts/validate_dataset.py data.csv
```

For a quick smoke check on a large file:

```bash
python scripts/validate_dataset.py data.csv --max-rows 10000
```

You can also validate the bundled sample immediately after cloning:

```bash
python scripts/validate_dataset.py data_sample.csv
```

## Run Locally

```bash
git clone https://github.com/sasi921/Customer-Segmentation-Predictive-Analysis.git
cd Customer-Segmentation-Predictive-Analysis
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
python scripts/validate_dataset.py data_sample.csv
python -m unittest discover -s tests -v
jupyter notebook Implementation_file.ipynb
```

Make sure `data.csv` is present in the project root before running the notebook from the beginning.

## Academic Project

This project was completed as a final data mining project at the **Missouri University of Science and Technology**.

### Team

- Keerthi Sri Cherukuri
- Ganesh Guddanti
- Kishore Kumar Jami
- Venkata Mokshagna Nadella
- Shruthi Shinde
- Sasidhar Reddy Velkuri

## Key Takeaway

The project demonstrates an end-to-end applied data mining workflow: cleaning raw retail transactions, transforming them into customer-level features, discovering customer segments with unsupervised learning, evaluating the quality of those segments, and extending the analysis into recommendation and predictive-spending use cases.

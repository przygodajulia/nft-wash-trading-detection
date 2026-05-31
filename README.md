# NFT Wash Trading Detection

This repository contains an engineering project focused on detecting suspicious NFT wash trading patterns using OpenSea transaction data.

The project follows a modular pipeline consisting of:

1. Data extraction
2. Data preprocessing
3. Feature engineering
4. Rule-based wash trading detection
5. Result analysis and visualization

The implementation is inspired by existing research on NFT wash trading detection and focuses on identifying suspicious trading behaviours such as self-trading, circular trading, repeated wallet interactions, short holding periods, and abnormal price patterns.

---

# Project Structure

```text
nft-wash-trading-detection/
├── notebooks
│   ├── exploratory
│   │   ├── 01_data_exploration.ipynb
│   │   └── 02_data_preprocessing_checks.ipynb
│   │
│   └── pipeline
│       ├── feature_engineering.ipynb
│       └── result_analysis.ipynb
│
├── src
│   ├── extraction
│   ├── preprocessing
│   ├── features
│   ├── detection
│   └── analysis
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/przygodajulia/nft-wash-trading-detection.git
cd nft-wash-trading-detection
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Data Extraction

The extraction module downloads NFT transaction data from the OpenSea API.

The extraction process is configurable through:

```text
src/extraction/config.py
```

Users can modify:

- NFT collections to analyse
- extraction time period
- API limits
- output locations

Example configuration:

```python
COLLECTION_SLUGS = [
    "cryptopunks",
    "pudgypenguins",
    "boredapeyachtclub"
]

AFTER_TIMESTAMP = int(datetime(2025, 4, 1).timestamp())
BEFORE_TIMESTAMP = int(datetime(2025, 10, 1).timestamp())
```

To analyse additional collections, simply add more collection slugs.

To analyse a longer period, update the timestamps accordingly.

Run extraction:

```bash
python -m src.extraction.extract_transactions
```

Raw responses are stored in:

```text
data/raw/opensea/
```

---

# OpenSea API Configuration

Create a `.env` file in the project root:

```text
OPENSEA_API_KEY=your_api_key_here
```

The extraction scripts automatically load the API key from this file.

---

# Data Preprocessing

The preprocessing module converts raw OpenSea API responses into a structured transaction dataset.

Responsibilities include:

- parsing raw JSON responses
- handling missing values
- standardising transaction fields
- preparing the dataset for feature engineering

Run preprocessing:

```bash
python -m src.preprocessing.preprocess_opensea
```

The resulting dataset is stored in a processed format and becomes the input for the feature engineering pipeline.

---

# Feature Engineering

The feature engineering module creates indicators describing NFT trading behaviour.

Implemented feature groups include:

### Base Features

Basic transaction attributes required by the detection pipeline.

### Self-Trading Features

Detects transactions where a wallet trades with itself.

### Circular Trading Features

Identifies ownership cycles that may indicate wash trading behaviour.

### NFT Flip Count

Measures how frequently a given NFT changes ownership.

### Holding Period

Calculates how long a wallet holds an NFT before selling it again.

### Wallet Pair Features

Measures repeated interactions between the same buyer and seller wallets.

### Price Anomaly Features

Flags transactions with unusual pricing behaviour.

The main pipeline combines all features into a single dataset used for scoring suspicious transactions.

---

# Detection Module

The detection module implements a rule-based wash trading detection approach.

The scoring system assigns risk points based on suspicious behavioural patterns.

Examples include:

- self-trading
- circular ownership patterns
- repeated wallet pair interactions
- extremely short holding periods
- unusual transaction prices

Transactions exceeding predefined thresholds are classified as suspicious.

The objective is not to prove fraud with certainty but to reduce a large dataset into a manageable set of transactions requiring further investigation.

---

# Notebooks

## Exploratory Notebooks

Location:

```text
notebooks/exploratory/
```

This section is intentionally flexible and serves as a sandbox environment for working with the data.

Typical uses include:

- dataset exploration
- quality checks
- validation of preprocessing steps
- testing new ideas
- ad-hoc analysis

These notebooks are not part of the final detection pipeline and can be modified freely.

---

## Pipeline Notebooks

Location:

```text
notebooks/pipeline/
```

This section contains the notebooks used to produce the final project results.

Typical workflow:

### Feature Engineering

```text
feature_engineering.ipynb
```

Runs the feature generation process and prepares the final transaction dataset.

### Result Analysis

```text
result_analysis.ipynb
```

Generates:

- suspicious transaction statistics
- collection-level analysis
- NFT-level analysis
- visualisations
- summary tables

The outputs from this notebook form the basis of the results chapter of the thesis.

---

# Typical Workflow

## 1. Configure extraction

Edit:

```text
src/extraction/config.py
```

Specify:

- collections
- date range
- extraction settings

---

## 2. Extract transaction data

```bash
python -m src.extraction.extract_transactions
```

---

## 3. Preprocess raw data

```bash
python -m src.preprocessing.preprocess_opensea
```

---

## 4. Generate features

Open:

```text
notebooks/pipeline/feature_engineering.ipynb
```

Execute all cells.

---

## 5. Run wash trading detection

The detection logic is executed within the feature engineering pipeline and produces transaction risk scores.

---

## 6. Analyse results

Open:

```text
notebooks/pipeline/result_analysis.ipynb
```

Execute all cells to generate:

- summary statistics
- collection comparisons
- suspicious NFT rankings
- visualisations
- final findings

---

# Research Context

Wash trading is a form of market manipulation where the same entity artificially creates trading activity to influence prices, generate misleading market signals, or exploit platform incentives.

NFT markets are particularly vulnerable due to pseudonymous wallet ownership and the absence of traditional regulatory oversight.

This project implements a rule-based detection framework inspired by academic research and applies it to real NFT transaction data collected from OpenSea.

---

# Project Goal

The goal of this project is to build a reproducible pipeline capable of identifying potentially suspicious NFT transactions and reducing a large transaction dataset into a smaller subset of transactions worthy of further investigation.

The project focuses on explainability and behavioural analysis rather than supervised machine learning, making the detection process transparent and interpretable.

---

# Notes

- New NFT collections can be analysed by modifying `COLLECTION_SLUGS` in the extraction configuration.
- Larger time periods can be analysed by changing the extraction timestamps.
- The exploratory notebooks are intended for experimentation.
- The pipeline notebooks are intended for generating the final project results.
- The project can be extended with additional behavioural features or machine learning models in future work.
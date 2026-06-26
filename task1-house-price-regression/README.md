# Task 1 — House Price Prediction (Linear Regression)

Predicts house prices from features like area, bedrooms, bathrooms,
stories, parking, and amenities (air conditioning, hot water heating,
preferred area, furnishing status, etc.), using Linear Regression and
Ridge Regression for comparison.

## Dataset

`data/house.csv` — 545 rows, 13 columns:

| Column | Description |
|---|---|
| `price` | Target variable (sale price) |
| `area` | Plot/house area (sq ft) |
| `bedrooms`, `bathrooms`, `stories` | Counts |
| `mainroad`, `guestroom`, `basement`, `hotwaterheating`, `airconditioning`, `prefarea` | yes/no amenities |
| `parking` | Number of parking spots |
| `furnishingstatus` | furnished / semi-furnished / unfurnished |

## Setup

```bash
pip install -r requirements.txt
```

## ⚠️ Before running: update the dataset path

The script currently has a hardcoded Windows path from local development:

```python
df = pd.read_csv(r"C:\Users\PRATEEK\OneDrive\Imports\Documents\code\internship\house.csv")
```

Change this line in `house_price_regression.py` to point at the bundled
dataset (relative to wherever you run the script from), for example:

```python
df = pd.read_csv("data/house.csv")
```

## Run it

```bash
python house_price_regression.py
```

This was verified to run end-to-end against `data/house.csv` once the
path above is updated, producing:

- Console output: dataset summary, preprocessing steps, model metrics
  (R², RMSE, MAE, 5-fold cross-validated R²) for Linear Regression and
  two Ridge variants, feature coefficients, sample predictions, and an
  example prediction for a new house.
- `house_price_result.png`: an 8-panel figure with actual-vs-predicted,
  model comparison, residual plots, feature importance, price
  distribution, area-vs-price, and a correlation heatmap.

### Verified results on the bundled dataset

| Model | R² | RMSE | MAE |
|---|---|---|---|
| Linear Regression | 0.661 | ₹1,083,568 | ₹795,234 |
| Ridge (α=1) | 0.661 | ₹1,083,928 | ₹795,493 |
| Ridge (α=10) | 0.659 | ₹1,087,213 | ₹797,786 |

Linear Regression performs best (~66% of price variance explained).
`area`, `bathrooms`, and `stories` are the strongest positive
predictors of price.

## Pipeline overview

1. **Load** — reads the CSV with pandas.
2. **Explore** — prints summary statistics and price range.
3. **Preprocess** — encodes yes/no columns to 1/0, encodes
   `furnishingstatus` ordinally, removes price outliers using the IQR
   method, then does an 80/20 train/test split.
4. **Train** — fits Linear Regression and two Ridge models (each inside
   a `Pipeline` with `StandardScaler`), evaluating with R², RMSE, MAE,
   and 5-fold cross-validation.
5. **Interpret** — extracts and ranks Linear Regression coefficients to
   show which features drive price most.
6. **Visualize** — saves an 8-panel diagnostic figure.
7. **Predict** — shows sample test-set predictions and a prediction for
   one new, hand-specified house.

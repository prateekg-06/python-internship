import sys
sys.stdout.reconfigure(encoding="utf-8")

"""
House Price Prediction - Linear Regression
Dataset: house.csv (545 rows, 13 columns)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------
print("=" * 60)
print("  HOUSE PRICE PREDICTION - LINEAR REGRESSION")
print("  Dataset: house.csv")
print("=" * 60)

df = pd.read_csv(r"C:\Users\PRATEEK\OneDrive\Imports\Documents\code\internship\house.csv")
print(f"\n[1] Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\n    Columns: {list(df.columns)}")
print(f"\n    First 3 rows:\n{df.head(3).to_string()}")

# ---------------------------------------------
# 2. EXPLORATORY DATA ANALYSIS
# ---------------------------------------------
print("\n[2] Basic Statistics:")
print(df.describe().round(2).to_string())
print(f"\n    Missing values: {df.isnull().sum().sum()} (none - clean dataset!)")
print(f"    Price range   : Rs.{df['price'].min():,}  –  Rs.{df['price'].max():,}")
print(f"    Mean price    : Rs.{df['price'].mean():,.0f}")

# ---------------------------------------------
# 3. PREPROCESSING
# ---------------------------------------------
print("\n[3] Preprocessing ...")

df_model = df.copy()

# Encode binary yes/no columns -> 1/0
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating',
               'airconditioning', 'prefarea']
for col in binary_cols:
    df_model[col] = df_model[col].map({'yes': 1, 'no': 0})

# Encode furnishingstatus -> ordinal (unfurnished=0, semi=1, furnished=2)
furnish_map = {'unfurnished': 0, 'semi-furnished': 1, 'furnished': 2}
df_model['furnishingstatus'] = df_model['furnishingstatus'].map(furnish_map)

print("    [OK] Encoded binary columns (yes->1, no->0)")
print("    [OK] Encoded furnishingstatus (unfurnished=0, semi=1, furnished=2)")

# Remove outliers using IQR on price
Q1, Q3 = df_model['price'].quantile([0.25, 0.75])
IQR = Q3 - Q1
before = len(df_model)
df_model = df_model[
    (df_model['price'] >= Q1 - 1.5 * IQR) &
    (df_model['price'] <= Q3 + 1.5 * IQR)
]
print(f"    [OK] Outlier removal: {before} -> {len(df_model)} rows")

# Features & Target
FEATURES = ['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
            'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
            'parking', 'prefarea', 'furnishingstatus']
TARGET = 'price'

X = df_model[FEATURES]
y = df_model[TARGET]

# Train / Test Split (80 / 20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"    [OK] Train/Test split -> Train: {len(X_train)}, Test: {len(X_test)}")

# ---------------------------------------------
# 4. MODEL TRAINING
# ---------------------------------------------
print("\n[4] Training Models ...")

models = {
    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model",  LinearRegression()),
    ]),
    "Ridge (α=1)": Pipeline([
        ("scaler", StandardScaler()),
        ("model",  Ridge(alpha=1.0)),
    ]),
    "Ridge (α=10)": Pipeline([
        ("scaler", StandardScaler()),
        ("model",  Ridge(alpha=10.0)),
    ]),
}

results = {}
for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    cv_r2  = cross_val_score(pipe, X_train, y_train, cv=5, scoring="r2").mean()
    results[name] = {
        "pipe":   pipe,
        "y_pred": y_pred,
        "RMSE":   np.sqrt(mean_squared_error(y_test, y_pred)),
        "MAE":    mean_absolute_error(y_test, y_pred),
        "R2":     r2_score(y_test, y_pred),
        "CV_R2":  cv_r2,
    }
    print(f"\n    -- {name}")
    print(f"       R²   = {results[name]['R2']:.4f}   (CV R² = {cv_r2:.4f})")
    print(f"       RMSE = Rs.{results[name]['RMSE']:,.0f}")
    print(f"       MAE  = Rs.{results[name]['MAE']:,.0f}")

best_name = max(results, key=lambda k: results[k]["R2"])
best      = results[best_name]
print(f"\n    * Best model: {best_name}  (R² = {best['R2']:.4f})")

# ---------------------------------------------
# 5. FEATURE IMPORTANCE
# ---------------------------------------------
lr_pipe   = results["Linear Regression"]["pipe"]
lr_model  = lr_pipe.named_steps["model"]
importance_df = pd.DataFrame({
    "Feature":     FEATURES,
    "Coefficient": lr_model.coef_,
}).sort_values("Coefficient", key=abs, ascending=False)

print("\n[5] Feature Coefficients (Linear Regression):")
print(importance_df.to_string(index=False))

# ---------------------------------------------
# 6. VISUALISATIONS
# ---------------------------------------------
sns.set_theme(style="whitegrid", palette="muted")
fig = plt.figure(figsize=(20, 18))
fig.suptitle("House Price Prediction - Linear Regression\n(house.csv Dataset)",
             fontsize=17, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

y_pred_best = best["y_pred"]
residuals   = y_test - y_pred_best

# (a) Actual vs Predicted
ax1 = fig.add_subplot(gs[0, :2])
ax1.scatter(y_test / 1e6, y_pred_best / 1e6, alpha=0.5, s=30, color="#4C72B0")
lim = [y_test.min() / 1e6 - 0.2, y_test.max() / 1e6 + 0.2]
ax1.plot(lim, lim, "r--", lw=1.5, label="Perfect prediction")
ax1.set_xlabel("Actual Price (Rs. Millions)", fontsize=11)
ax1.set_ylabel("Predicted Price (Rs. Millions)", fontsize=11)
ax1.set_title(f"Actual vs Predicted  [{best_name}]", fontsize=12)
ax1.legend()

# (b) Model R² comparison
ax2 = fig.add_subplot(gs[0, 2])
model_names  = list(results.keys())
r2_vals      = [results[n]["R2"] for n in model_names]
short_labels = ["Linear\nReg.", "Ridge\n(α=1)", "Ridge\n(α=10)"]
bars = ax2.bar(short_labels, r2_vals,
               color=["#4C72B0", "#DD8452", "#55A868"], edgecolor="white")
ax2.set_ylim(min(r2_vals) - 0.02, max(r2_vals) + 0.02)
for bar, val in zip(bars, r2_vals):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.002, f"{val:.4f}", ha="center", fontsize=9)
ax2.set_title("R² Score - Model Comparison", fontsize=12)
ax2.set_ylabel("R² Score")

# (c) Residuals distribution
ax3 = fig.add_subplot(gs[1, 0])
ax3.hist(residuals / 1e6, bins=40, color="#4C72B0", edgecolor="white", alpha=0.85)
ax3.axvline(0, color="red", linestyle="--")
ax3.set_xlabel("Residual (Rs. Millions)", fontsize=11)
ax3.set_title("Residuals Distribution", fontsize=12)

# (d) Residuals vs Predicted
ax4 = fig.add_subplot(gs[1, 1])
ax4.scatter(y_pred_best / 1e6, residuals / 1e6, alpha=0.45, s=25, color="#DD8452")
ax4.axhline(0, color="red", linestyle="--", lw=1.5)
ax4.set_xlabel("Predicted Price (Rs. Millions)", fontsize=11)
ax4.set_ylabel("Residual (Rs. Millions)", fontsize=11)
ax4.set_title("Residuals vs Predicted", fontsize=12)

# (e) Feature importance (coefficients)
ax5 = fig.add_subplot(gs[1, 2])
colors = ["#55A868" if c > 0 else "#C44E52"
          for c in importance_df["Coefficient"]]
ax5.barh(importance_df["Feature"], importance_df["Coefficient"],
         color=colors, edgecolor="white")
ax5.axvline(0, color="black", linewidth=0.8)
ax5.set_xlabel("Coefficient Value", fontsize=11)
ax5.set_title("Feature Importance\n(Linear Regression Coefficients)", fontsize=12)

# (f) Price distribution
ax6 = fig.add_subplot(gs[2, 0])
ax6.hist(y / 1e6, bins=40, color="#55A868", edgecolor="white", alpha=0.85)
ax6.set_xlabel("Price (Rs. Millions)", fontsize=11)
ax6.set_title("Target Price Distribution", fontsize=12)

# (g) Area vs Price scatter
ax7 = fig.add_subplot(gs[2, 1])
ax7.scatter(df_model['area'], df_model['price'] / 1e6,
            alpha=0.35, s=20, color="#9467BD")
ax7.set_xlabel("Area (sq ft)", fontsize=11)
ax7.set_ylabel("Price (Rs. Millions)", fontsize=11)
ax7.set_title("Area vs Price", fontsize=12)

# (h) Correlation heatmap
ax8 = fig.add_subplot(gs[2, 2])
corr = df_model[FEATURES + [TARGET]].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, ax=ax8, annot_kws={"size": 7}, linewidths=0.5)
ax8.set_title("Feature Correlation Heatmap", fontsize=12)

plt.savefig("house_price_result.png",
            dpi=150, bbox_inches="tight")
print("\n[6] Visualisation saved.")

# ---------------------------------------------
# 7. SAMPLE PREDICTIONS
# ---------------------------------------------
print("\n[7] Sample Predictions vs Actual (first 10):")
sample = pd.DataFrame({
    "Actual (Rs.)":    y_test.values[:10],
    "Predicted (Rs.)": y_pred_best[:10].astype(int),
    "Error (Rs.)":     (y_pred_best[:10] - y_test.values[:10]).astype(int),
})
sample["Error %"] = (sample["Error (Rs.)"] / sample["Actual (Rs.)"] * 100).round(1)
print(sample.to_string(index=False))

# ---------------------------------------------
# 8. PREDICT A NEW HOUSE (example)
# ---------------------------------------------
print("\n[8] Predict price for a new house:")
new_house = pd.DataFrame([{
    'area': 5000, 'bedrooms': 3, 'bathrooms': 2, 'stories': 2,
    'mainroad': 1, 'guestroom': 0, 'basement': 1,
    'hotwaterheating': 0, 'airconditioning': 1,
    'parking': 1, 'prefarea': 1, 'furnishingstatus': 2
}])
predicted_price = best["pipe"].predict(new_house)[0]
print(f"    Input  : Area=5000 sqft, 3 bed, 2 bath, AC=Yes, Prefarea=Yes")
print(f"    Prediction: Rs.{predicted_price:,.0f}  (~Rs.{predicted_price/1e6:.2f} Million)")

print("\n" + "=" * 60)
print("  FINAL RESULTS SUMMARY")
print("=" * 60)
print(f"  Dataset       : house.csv ({len(df)} rows, {df.shape[1]} features)")
print(f"  Best Model    : {best_name}")
print(f"  R² Score      : {best['R2']:.4f}  ({best['R2']*100:.1f}% variance explained)")
print(f"  CV R² (5-fold): {best['CV_R2']:.4f}")
print(f"  RMSE          : Rs.{best['RMSE']:,.0f}")
print(f"  MAE           : Rs.{best['MAE']:,.0f}")
print("=" * 60)

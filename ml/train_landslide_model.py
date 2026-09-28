import geopandas as gpd
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score
)


# -------------------------------------------------
# Paths
# -------------------------------------------------

INPUT_PATH = "data/processed/pune_landslide_ml_ready.gpkg"


# -------------------------------------------------
# Load dataset
# -------------------------------------------------

data = gpd.read_file(INPUT_PATH)

print("Total samples:", len(data))


# -------------------------------------------------
# Select ML features
# -------------------------------------------------

features = [
    "slope_degrees",
    "elevation_m",
    "rainfall_2024_mm"
]

X = data[features]
y = data["label"]


# -------------------------------------------------
# Train / test split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -------------------------------------------------
# Create Random Forest
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


# -------------------------------------------------
# Train
# -------------------------------------------------

print("\nTraining Random Forest...")

model.fit(
    X_train,
    y_train
)

print("Training complete.")


# -------------------------------------------------
# Predictions
# -------------------------------------------------

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# -------------------------------------------------
# Evaluation
# -------------------------------------------------

print("\nMODEL PERFORMANCE")
print("-----------------")

print(
    "Accuracy:",
    round(accuracy_score(y_test, y_pred), 4)
)

print(
    "ROC-AUC:",
    round(roc_auc_score(y_test, y_probability), 4)
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Non-landslide",
            "Landslide"
        ]
    )
)


# -------------------------------------------------
# Feature importance
# -------------------------------------------------

print("\nFEATURE IMPORTANCE")
print("------------------")

importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(
    ascending=False
)

print(importance)

# -------------------------------------------------
# Save trained model
# -------------------------------------------------

MODEL_PATH = "ml/landslide_model.pkl"

joblib.dump(model, MODEL_PATH)

print("\nModel saved to:")
print(MODEL_PATH)
from pathlib import Path
import joblib
import json

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model paths
model_path = BASE_DIR / "Model" / "fraud_model.pkl"

threshold_path = BASE_DIR / "Model" / "threshold.json"

# Load model
model = joblib.load(model_path)

# Load threshold
with open(threshold_path, "r") as f:
    threshold = json.load(f)["threshold"]

import pandas as pd

def score_transaction(txn):
    df = pd.DataFrame([txn])

    # Same Feature Engineering
    df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    df['transaction_hour'] = df['transaction_time'].dt.hour


    # drop ip
    df = df.drop(columns=['ip_address'])

    # encode
    df = pd.get_dummies(df, columns=['location', 'device_id'], drop_first=True)

    # align columns with training
    model_features = model.feature_names_in_
    df = df.reindex(columns=model_features, fill_value=0)

    # predict
    proba = model.predict_proba(df)[:, 1][0]

    prediction = 1 if proba >= threshold else 0

    return prediction, proba
import streamlit as st
import pandas as pd
import joblib
import json
import plotly.express as px
from pathlib import Path

# Page Config

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

st.title("Fraud Detection Intelligence Dashboard")

# Load Data

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "CSV (DB updates)" / "scored_transactions.csv"

df = pd.read_csv(csv_path)

df['transaction_time'] = pd.to_datetime(df['transaction_time'])

# Load Model and Threshold

model_path = BASE_DIR / "Model" / "fraud_model.pkl"

feature_path = BASE_DIR / "Model" / "model_features.pkl"

threshold_path = BASE_DIR / "Model" / "threshold.json"

model = joblib.load(model_path)

model_features = joblib.load(feature_path)

with open(threshold_path, "r") as f:
    threshold_data = json.load(f)

saved_threshold = threshold_data["threshold"]

# Sidebar Controls

st.sidebar.header("Dashboard Controls")

# Refresh Button
if st.sidebar.button("Refresh Data"):
    st.rerun()

# Threshold Slider
threshold = st.sidebar.slider(
    "Fraud Probability Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.4,
    step=0.05
)

# Fraud Only Toggle
fraud_only = st.sidebar.checkbox(
    "Show Fraud Predictions Only"
)

# Location Filter
locations = st.sidebar.multiselect(
    "Filter by Location",
    options=sorted(df['location'].dropna().unique())
)

# Device Filter
devices = st.sidebar.multiselect(
    "Filter by Device",
    options=sorted(df['device_id'].dropna().unique())
)

# Apply filters
filtered_df = df.copy()

filtered_df['adjusted_prediction'] = (
    filtered_df['model_probability'] >= threshold
).astype(int)

# Fraud-only filter
if fraud_only:
    filtered_df = filtered_df[
        filtered_df['adjusted_prediction'] == 1
    ]

# Location filter
if locations:
    filtered_df = filtered_df[
        filtered_df['location'].isin(locations)
    ]

# Device filter
if devices:
    filtered_df = filtered_df[
        filtered_df['device_id'].isin(devices)
    ]

# KPIs and Metrics

total_transactions = len(filtered_df)

fraud_cases = filtered_df[
    'adjusted_prediction'
].sum()

fraud_rate = round(
    (fraud_cases / total_transactions) * 100,
    2
) if total_transactions > 0 else 0

accuracy = round(
    (
        filtered_df['adjusted_prediction']
        ==
        filtered_df['is_fraud']
    ).mean() * 100,
    2
) if total_transactions > 0 else 0

avg_probability = round(
    filtered_df['model_probability'].mean(),
    2
) if total_transactions > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Transactions",
    total_transactions
)

col2.metric(
    "Fraud Detected",
    fraud_cases
)

col3.metric(
    "Fraud Rate %",
    fraud_rate
)

col4.metric(
    "Model Accuracy %",
    accuracy
)

col5.metric(
    "Avg Fraud Probability",
    avg_probability
)

st.divider()

# High risk alerts

st.subheader("High Risk Fraud Alerts")

alerts = filtered_df[
    filtered_df['model_probability'] >= threshold
]

st.dataframe(
    alerts[
        [
            'transaction_id',
            'customer_id',
            'transaction_amount',
            'location',
            'device_id',
            'model_probability',
            'is_fraud',
            'adjusted_prediction'
        ]
    ].sort_values(
        by='model_probability',
        ascending=False
    ),
    use_container_width=True
)

# Fraud probability distribution

st.subheader("Fraud Probability Distribution")

fig = px.histogram(
    filtered_df,
    x='model_probability',
    nbins=30
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Prediction Analysis

st.subheader("Prediction Analysis")

filtered_df['prediction_match'] = (
    filtered_df['adjusted_prediction']
    ==
    filtered_df['is_fraud']
)

false_positives = filtered_df[
    (filtered_df['adjusted_prediction'] == 1)
    &
    (filtered_df['is_fraud'] == 0)
]

false_negatives = filtered_df[
    (filtered_df['adjusted_prediction'] == 0)
    &
    (filtered_df['is_fraud'] == 1)
]

correct_fraud = filtered_df[
    (filtered_df['adjusted_prediction'] == 1)
    &
    (filtered_df['is_fraud'] == 1)
]

correct_legit = filtered_df[
    (filtered_df['adjusted_prediction'] == 0)
    &
    (filtered_df['is_fraud'] == 0)
]

col6, col7, col8, col9 = st.columns(4)

col6.metric(
    "False Positives",
    len(false_positives)
)

col7.metric(
    "False Negatives",
    len(false_negatives)
)

col8.metric(
    "Correct Fraud",
    len(correct_fraud)
)

col9.metric(
    "Correct Legitimate",
    len(correct_legit)
)

# CSV Download

st.subheader("Download Filtered Dataset")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_fraud_analysis.csv",
    mime="text/csv"
)

# Transaction Explorer

st.subheader("Transaction Explorer")

search_customer = st.text_input(
    "Search Customer ID"
)

explorer_df = filtered_df.copy()

if search_customer:
    explorer_df = explorer_df[
        explorer_df['customer_id']
        .astype(str)
        .str.contains(search_customer)
    ]

st.dataframe(
    explorer_df.sort_values(
        by='transaction_time',
        ascending=False
    ),
    use_container_width=True
)

# Upload Your Own CSV

st.subheader("Test Model on Your CSV (Ensure it has the required columns)")

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)

if uploaded_file is not None:

    uploaded_df = pd.read_csv(uploaded_file)

    st.write("Uploaded Dataset Preview")

    st.dataframe(
        uploaded_df.head(),
        use_container_width=True
    )

    required_columns = [
        'transaction_id',
        'customer_id',
        'transaction_amount',
        'transaction_time',
        'location',
        'device_id'
    ]

    missing_cols = [
        col for col in required_columns
        if col not in uploaded_df.columns
    ]

    if missing_cols:

        st.error(
            f"Missing Required Columns: {missing_cols}"
        )

    else:

        # Feature Engineering
        uploaded_df['transaction_time'] = pd.to_datetime(
            uploaded_df['transaction_time']
        )

        uploaded_df['transaction_hour'] = (
            uploaded_df['transaction_time'].dt.hour
        )

        # Placeholder engineered features
        uploaded_df['time_diff'] = 9999
        uploaded_df['txn_count'] = 1
        uploaded_df['avg_amount'] = (
            uploaded_df['transaction_amount']
        )

        uploaded_df['relative_amount'] = 1

        # Optional columns
        if 'ip_address' in uploaded_df.columns:
            uploaded_df = uploaded_df.drop(
                columns=['ip_address']
            )

        # Encode categorical columns
        uploaded_encoded = pd.get_dummies(
            uploaded_df,
            columns=['location', 'device_id'],
            drop_first=True
        )

        # Align columns
        uploaded_encoded = uploaded_encoded.reindex(
            columns=model_features,
            fill_value=0
        )

        # Predict probabilities
        probabilities = model.predict_proba(
            uploaded_encoded
        )[:, 1]

        predictions = (
            probabilities >= saved_threshold
        ).astype(int)

        # Add results
        uploaded_df['model_probability'] = probabilities

        uploaded_df['model_prediction'] = predictions

        st.subheader("Scored Transactions")

        st.dataframe(
            uploaded_df,
            use_container_width=True
        )

        # Download button
        scored_csv = uploaded_df.to_csv(index=False)

        st.download_button(
            label="Download Scored CSV",
            data=scored_csv,
            file_name="scored_uploaded_transactions.csv",
            mime="text/csv"
        )
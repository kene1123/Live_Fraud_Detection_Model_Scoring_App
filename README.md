# Live Fraud Detection Model Scoring System

Streamlit Dashboard:
https://live-fraud-detection-scoring.streamlit.app/

## Project Overview

This project simulates how a modern fraud detection system behaves in a near-live production environment.

Instead of stopping at model training and evaluation, the system was extended into a fully automated fraud monitoring pipeline capable of:

* Generating continuous transaction activity
* Storing transactions in a live PostgreSQL database
* Scoring transactions with a machine learning fraud model
* Tracking fraud probabilities and prediction performance
* Exporting updated fraud reports automatically
* Powering an interactive Streamlit dashboard for users and recruiters to explore

The project combines:

* Machine Learning
* Data Engineering
* Automation
* Cloud Scheduling
* Database Integration
* Interactive Analytics

This repository reflects the transition from a notebook-based machine learning project into a deployable fraud monitoring system.

---

# Live Application

## Streamlit Dashboard

The deployed dashboard allows users to:

* Monitor fraud predictions
* Explore fraud probabilities
* Filter by location and device
* Analyze prediction performance
* Upload their own transaction CSV files for fraud scoring
* Investigate failed and successful fraud predictions

The application continuously updates as GitHub Actions refreshes the fraud scoring pipeline.

---

# Key Features

## Machine Learning Fraud Detection

The fraud model was trained using engineered transaction behavior patterns including:

* Transaction amount behavior
* Relative transaction spikes
* Transaction frequency
* Time difference between transactions
* Device and location behavior

The final model was tuned using threshold optimization to balance:

* Fraud Recall
* Precision
* Overall Stability

---

## Near-Live Fraud Simulation

A transaction generator continuously creates realistic transaction activity.

Each transaction:

* Enters the PostgreSQL database
* Preserves historical customer behavior
* Gets scored by the fraud model
* Receives fraud probability outputs
* Updates reporting datasets automatically

The system preserves transaction history over time, allowing the model to evaluate customer behavior patterns instead of isolated transactions.

---

## Automated Scoring Pipeline

The scoring engine:

1. Pulls newly inserted transactions
2. Retrieves historical customer activity
3. Engineers fraud detection features
4. Scores transactions using the trained model
5. Writes predictions back into the database
6. Exports updated CSV reports

Automation runs through GitHub Actions on a scheduled workflow.

---

## Interactive Streamlit Dashboard

The dashboard includes:

* KPI Monitoring
* Fraud Rate Analysis
* Fraud Probability Distribution
* Prediction Match Analysis
* Fraud-Only Filtering
* Device Filters
* Location Filters
* Transaction Drilldown Tables
* User CSV Upload Fraud Scoring

The dashboard was intentionally designed with:

* Simplicity
* Clarity
* Recruiter accessibility
* Clean UI principles

---

# Upload Your Own CSV

Users can upload their own transaction dataset for fraud scoring.

Important:

* The uploaded dataset is scored using the already trained fraud detection model
* The upload feature does NOT retrain the model
* Uploaded CSVs should follow a structure similar to the project transaction schema

Required fields typically include:

* transaction_amount
* transaction_time
* location
* device_id
* customer_id

The uploaded file is processed temporarily within the dashboard for fraud prediction analysis.

---

# Tech Stack

## Languages

* Python
* SQL

## Machine Learning

* Scikit-learn
* Joblib

## Data Processing

* Pandas
* NumPy

## Database

* PostgreSQL (Neon DB)
* Psycopg2

## Automation

* GitHub Actions

## Dashboard

* Streamlit
* Plotly

## Environment Management

* Python Dotenv

---

# Project Architecture

## Data Flow

Transaction Generator
↓
PostgreSQL Database
↓
Fraud Scoring Engine
↓
Prediction Storage
↓
CSV Export
↓
Streamlit Dashboard
↓
User Interaction

---

# Automation Workflow

GitHub Actions automates the entire pipeline:

1. Runs scheduled workflows
2. Connects securely to Neon PostgreSQL
3. Generates new transactions
4. Scores transactions
5. Updates fraud reports
6. Pushes updated CSV outputs back to GitHub

This enables the dashboard to continuously reflect newly generated fraud activity.

---

# Model Performance

The fraud model was optimized using threshold tuning rather than relying only on default classification settings.

Final evaluation focused on:

* Fraud recall
* Precision balance
* ROC-AUC performance
* Practical fraud detection behavior

The project prioritizes realistic fraud detection tradeoffs rather than artificially inflated accuracy metrics.

---

# Documentation

Additional documentation and development notes are available in the `Documentation` folder.

This includes:

* Fraud analysis reasoning
* Feature explanations
* Development thinking process
* Modeling decisions
* Pipeline evolution notes

These documents help explain not only the final system, but also the engineering decisions behind it.

---

# What Makes This Project Different

Many fraud detection projects stop after:

* model training
* notebook evaluation
* static prediction outputs

This project extends further into:

* database integration
* automation
* scheduled execution
* live scoring behavior
* cloud deployment
* dashboard interaction
* historical transaction tracking

The result is a much closer simulation of how fraud monitoring systems behave in real production environments.

---

# Future Improvements

Potential future enhancements include:

* Real-time streaming pipelines
* Model retraining workflows
* Advanced anomaly detection
* User authentication
* API-based scoring endpoints
* Cloud container deployment
* Alert notification systems

---

# Repository Structure

```text
Fraud Detection Project
│
├── Documentation
├── Kaggle Fraud Data for Testing
├── Near Live Simulation of Fraud Detection
│   ├── Model
│   ├── Scripts
│   ├── Streamlit_App
│   ├── CSV (DB updates)
│   └── Notebooks
├── .github/workflows
├── requirements.txt
└── README.md
```

---

# About the Developer

This project was developed as part of a broader effort to move beyond traditional analytics projects into systems-oriented machine learning engineering.

The focus was not only on building a predictive model, but on designing an end-to-end fraud monitoring workflow that demonstrates:

* analytical thinking
* automation design
* production awareness
* cloud workflow integration
* data infrastructure understanding
* interactive product thinking

---

# Final Note

This project represents the evolution of a fraud detection model into a deployable analytical system.

It combines machine learning, automation, cloud workflows, database integration, and interactive analytics into a single continuously updating fraud monitoring environment.

The goal was to build something closer to how real enterprise fraud systems operate while maintaining accessibility for recruiters, analysts, and technical reviewers.

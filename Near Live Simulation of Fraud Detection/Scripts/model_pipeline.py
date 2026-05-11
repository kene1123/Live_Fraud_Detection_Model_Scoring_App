import psycopg2
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score


# In[2]:


# Connect to database
from db_config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()
query = "SELECT * FROM transactions"
FD = pd.read_sql(query, conn)

FD.head()


# In[3]:


# REPROCESSING

# Convert time
FD['transaction_time'] = pd.to_datetime(FD['transaction_time'])

# Sort for time-based features
FD = FD.sort_values(['customer_id', 'transaction_time'])


# In[4]:


# Feature engineering
FD['time_diff'] = FD.groupby('customer_id')['transaction_time'].diff().dt.total_seconds()
FD['time_diff'] = FD['time_diff'].fillna(9999)

FD['transaction_hour'] = FD['transaction_time'].dt.hour

FD['txn_count'] = FD.groupby('customer_id').cumcount() + 1

FD['avg_amount'] = FD.groupby('customer_id')['transaction_amount'].transform('mean')

FD['relative_amount'] = FD['transaction_amount'] / (FD['avg_amount'] + 1)


# In[5]:


# Drop unused/high cardinality
FD = FD.drop(columns=['ip_address'])

# Encode categorical features
FD = pd.get_dummies(FD, columns=['location', 'device_id'], drop_first=True)


# In[6]:


# Features & target
X = FD.drop(columns=['is_fraud', 'transaction_time', 'transaction_id'])
y = FD['is_fraud']


# In[7]:


# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y)


# In[8]:


# Model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=3,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)


# In[9]:


# Train
model.fit(X_train, y_train)


# In[10]:


# Evaluation
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

roc = roc_auc_score(y_test, y_proba)
print("\nROC-AUC:", roc)


# In[12]:


import numpy as np
y_proba = model.predict_proba(X_test)[:, 1]

threshold = [0.3, 0.4, 0.5, 0.6, 0.7]

for t in threshold:
    print(f"\nThreshold: {t}")

    y_pred = (y_proba >= t).astype(int)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


# In[15]:


import joblib
import json

joblib.dump(model, "C:\\Users\\ty\\Downloads\\Kene_projects\\Fraud Detection Project\\Near Live Simulation of Fraud Detection\\Model\\fraud_model.pkl")

with open("C:\\Users\\ty\\Downloads\\Kene_projects\\Fraud Detection Project\\Near Live Simulation of Fraud Detection\\Model\\threshold.json", "w") as f:
    json.dump({"threshold": 0.4}, f)

import joblib

joblib.dump(
    model.feature_names_in_.tolist(),
    "C:\\Users\\ty\\Downloads\\Kene_projects\\Fraud Detection Project\\Near Live Simulation of Fraud Detection\\Model\\model_features.pkl"
)

# In[ ]:





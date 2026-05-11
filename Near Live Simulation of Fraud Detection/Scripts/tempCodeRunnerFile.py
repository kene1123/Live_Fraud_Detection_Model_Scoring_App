import pandas as pd
import psycopg2

from db_config import DB_CONFIG

# Connect to DB
conn = psycopg2.connect(**DB_CONFIG)

# Pull scored transactions
query = """
SELECT *
FROM transactions
WHERE model_prediction IS NOT NULL
ORDER BY transaction_time ASC
"""

df = pd.read_sql(query, conn)

# Add comparison column
df['prediction_match'] = (
    df['is_fraud'] == df['model_prediction']
)

# Export CSV
df.to_csv("Near Live Simulation of Fraud Detection\\CSV (DB updates)\\scored_transactions.csv", index=False)

print("CSV Export Updated Successfully")
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
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "CSV (DB updates)" / "scored_transactions.csv"

df.to_csv(csv_path, index=False)
print("CSV Export Updated Successfully")
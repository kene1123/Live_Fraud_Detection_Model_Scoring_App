import psycopg2
import pandas as pd

from scoring import score_transaction
from db_config import DB_CONFIG

# Connect to DB
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Pull unscored transactions
query = """
SELECT *
FROM transactions
WHERE model_prediction IS NULL
ORDER BY transaction_time ASC, transaction_id ASC
LIMIT 1000
"""

df = pd.read_sql(query, conn)

if df.empty:
    print("No new transactions to score")

else:

    print(f"Scoring {len(df)} transactions...")

    results = []

    for _, row in df.iterrows():

        txn = row.to_dict()

        customer_id = txn['customer_id']
        txn_time = txn['transaction_time']

        # Pull customer history BEFORE this transaction
        history_query = """
        SELECT
            COUNT(*) as txn_count,
            AVG(transaction_amount) as avg_amount,
            MAX(transaction_time) as last_time
        FROM transactions
        WHERE customer_id = %s
        AND transaction_time < %s
        """

        cursor.execute(history_query, (customer_id, txn_time))
        history = cursor.fetchone()

        txn_count = history[0] if history[0] else 0

        avg_amount = (
            float(history[1])
            if history[1]
            else txn['transaction_amount']
        )

        last_time = history[2]

        # Time difference
        if last_time:
            time_diff = (txn_time - last_time).seconds
        else:
            time_diff = 9999

        # Feature Engineering
        txn['txn_count'] = txn_count
        txn['avg_amount'] = avg_amount
        txn['time_diff'] = time_diff

        txn['relative_amount'] = (
            txn['transaction_amount'] / (avg_amount + 1)
        )

        # Score
        prediction, proba = score_transaction(txn)

        results.append((
            int(prediction),
            float(proba),
            txn['transaction_id']
        ))

    # Update predictions
    update_query = """
    UPDATE transactions
    SET
        model_prediction = %s,
        model_probability = %s
    WHERE transaction_id = %s
    """

    cursor.executemany(update_query, results)

    conn.commit()

    print(f"{len(results)} transactions scored successfully")

cursor.close()
conn.close()
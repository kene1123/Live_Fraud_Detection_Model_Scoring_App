# coding: utf-8

# In[3]:


import psycopg2
from psycopg2.extras import execute_values
from generator import generate_transaction


# In[16]:


# Connect to database
from db_config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()


# In[17]:


# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGINT,
    customer_id INT,
    transaction_amount FLOAT,
    transaction_time TIMESTAMP,
    location TEXT,
    ip_address TEXT,
    device_id TEXT,
    is_foreign_transaction INT,
    device_change_flag INT,
    is_fraud INT,
    model_prediction INT,
    model_probability FLOAT
);
""")

conn.commit()


# In[18]:


# Create Insert Function
def insert_batch(transactions):

    values = [
        (
            txn['transaction_id'],
            txn['customer_id'],
            txn['transaction_amount'],
            txn['transaction_time'],
            txn['location'],
            txn['ip_address'],
            txn['device_id'],
            txn['is_foreign_transaction'],
            txn['device_change_flag'],
            txn['is_fraud']
        )
        for txn in transactions
    ]

    query = """
    INSERT INTO transactions (
    transaction_id,
    customer_id,
    transaction_amount,
    transaction_time,
    location,
    ip_address,
    device_id,
    is_foreign_transaction,
    device_change_flag,
    is_fraud

    ) VALUES %s
    """

    execute_values(cursor, query, values)
    conn.commit()


# In[19]:


# Insert Batch
def generate_batch(size=100):
    return [generate_transaction() for _ in range(size)]


# In[20]:


batch = generate_batch(5000)
insert_batch(batch)

print("Inserted 5000 transactions")


# In[ ]:





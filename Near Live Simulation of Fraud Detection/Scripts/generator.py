import random
from datetime import datetime, timedelta

# Customer State Tracking
customer_last_time = {}
customer_txn_count = {}
customer_total_amount = {}

customer_home_location = {}
customer_last_device = {}
customer_last_ip = {}

# sample pools
locations = ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan"]
devices = ["mobile", "web", "tablet"]

def generate_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def generate_transaction():

    transaction_id = int(datetime.now().timestamp() * 1000000) + random.randint(1, 999)
    customer_id = random.randint(1, 100)

    # Time Handling
    last_time = customer_last_time.get(customer_id)

    if last_time:
        time_gap = random.randint(5, 600)
        current_time = last_time + timedelta(seconds=time_gap)
    else:
        current_time = datetime.now()

    # Basic Features
    transaction_amount = round(random.uniform(100, 50000), 2)

    txn_count = customer_txn_count.get(customer_id, 0)
    total_amount = customer_total_amount.get(customer_id, 0)

    if last_time:
        time_diff = (current_time - last_time).seconds
    else:
        time_diff = 9999

    avg_amount = total_amount / txn_count if txn_count > 0 else transaction_amount
    relative_amount = transaction_amount / (avg_amount + 1)

    # Location (Home VS Current)
    if customer_id not in customer_home_location:
        customer_home_location[customer_id] = random.choice(locations)

    home_location = customer_home_location[customer_id]

    # 80% same location, 20% different
    if random.random() < 0.8:
        location = home_location
    else:
        location = random.choice(locations)

    is_foreign_transaction = 1 if location != home_location else 0

    # Device
    if customer_id not in customer_last_device:
        customer_last_device[customer_id] = random.choice(devices)

    if random.random() < 0.85:
        device_id = customer_last_device[customer_id]
    else:
        device_id = random.choice(devices)

    device_change_flag = 1 if device_id != customer_last_device[customer_id] else 0

    # IP Address
    if customer_id not in customer_last_ip:
        customer_last_ip[customer_id] = generate_ip()

    if random.random() < 0.8:
        ip_address = customer_last_ip[customer_id]
    else:
        ip_address = generate_ip()

    # Fraud Logic
    fraud_score = 0

    if transaction_amount > 40000:
        fraud_score += 0.5

    if relative_amount > 4:
        fraud_score += 0.4

    if time_diff < 20 and txn_count > 3:
        fraud_score += 0.4

    if is_foreign_transaction:
        fraud_score += 0.3

    if device_change_flag:
        fraud_score += 0.3

    # Noise
    fraud_score += random.uniform(0, 0.1)

    fraud_probability = min(fraud_score, 1)

    is_fraud = 1 if random.random() < fraud_probability else 0

    # Update State
    customer_last_time[customer_id] = current_time
    customer_txn_count[customer_id] = txn_count + 1
    customer_total_amount[customer_id] = total_amount + transaction_amount

    customer_last_device[customer_id] = device_id
    customer_last_ip[customer_id] = ip_address

    # Return transaction
    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_amount": transaction_amount,
        "transaction_time": current_time,
        "location": location,
        "ip_address": ip_address,
        "device_id": device_id,
        "is_foreign_transaction": is_foreign_transaction,
        "device_change_flag": device_change_flag,
        "is_fraud": is_fraud
    }
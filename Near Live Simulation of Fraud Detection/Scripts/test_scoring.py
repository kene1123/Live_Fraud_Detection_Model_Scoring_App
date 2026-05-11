from generator import generate_transaction
from scoring import score_transaction

txn = generate_transaction()
prediction, proba = score_transaction(txn)

print("Model Prediction:", prediction)
print("Probability:", proba)
print("Generator Label:", txn["is_fraud"])
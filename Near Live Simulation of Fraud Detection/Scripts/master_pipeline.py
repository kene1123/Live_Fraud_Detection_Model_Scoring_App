from pathlib import Path
import sys

print("Starting Fraud Detection Pipeline...")

BASE_DIR = Path(__file__).resolve().parent

scripts = [
    "DB_Data_Entry_Automated.py",
    "db_scoring.py",
    "export_csv.py"
]

steps = [
    "DB Data Entry",
    "Scoring Pipeline",
    "Export CSV"
]

for step, script in zip(steps, scripts):
    print(f"Running {step}...")

    script_path = BASE_DIR / script
    exec(open(script_path).read())

print("Pipeline Completed Successfully.")
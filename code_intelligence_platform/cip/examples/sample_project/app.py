import subprocess
import pickle

API_TOKEN = "demo-secret-token-value"

def run_command(user_input):
    return subprocess.run(user_input, shell=True)

def load_data(blob):
    return pickle.loads(blob)

def calculate_total(values):
    return sum(values)

from pathlib import Path
from dotenv import load_dotenv
import os

# Mimic the logic in agents.py
env_path = Path('c:/Users/MOHD TALHA/Downloads/kaggle Capstone/backend/.env')
print(f"Loading from: {env_path}")
load_dotenv(dotenv_path=env_path)

key = os.getenv("GOOGLE_API_KEY")
print(f"Key loaded: {key}")

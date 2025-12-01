import os
import sys
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

models_to_test = ['gemini-2.0-flash', 'gemini-1.5-flash']

for model in models_to_test:
    print(f"Testing {model}...", flush=True)
    try:
        response = client.models.generate_content(
            model=model,
            contents='Hello',
        )
        print(f"SUCCESS: {model} works", flush=True)
        break
    except Exception as e:
        print(f"FAILED: {model} - {e}", flush=True)

import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

models_to_test = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-2.0-flash-exp']

for model in models_to_test:
    try:
        print(f"Testing {model}...")
        response = client.models.generate_content(
            model=model,
            contents='Hello',
        )
        print(f"SUCCESS: {model} works")
        break
    except Exception as e:
        print(f"FAILED: {model} - {e}")

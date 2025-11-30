import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Hello',
    )
    print("gemini-1.5-flash works")
except Exception as e:
    print(f"gemini-1.5-flash failed: {e}")

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents='Hello',
    )
    print("gemini-2.0-flash works")
except Exception as e:
    print(f"gemini-2.0-flash failed: {e}")

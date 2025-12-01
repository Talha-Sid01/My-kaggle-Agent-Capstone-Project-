import os
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

key = os.getenv("GOOGLE_API_KEY")
print(f"Loaded Key: {key[:5]}...{key[-5:] if key else 'None'}")

client = genai.Client(api_key=key)

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents='Hello',
    )
    print("gemini-2.0-flash works")
except Exception as e:
    print(f"gemini-2.0-flash failed: {e}")

import os
import json
import re
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from backend.models import SymptomExtract, TriageResult, TriageEnum, TrustedInfo

from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GOOGLE_API_KEY")
# Initialize client only if API key is present to avoid immediate crash on import, 
# but it will fail at runtime if not set.
client = genai.Client(api_key=API_KEY) if API_KEY else None

# Hardcoded Trusted Sources
TRUSTED_SOURCES = {
    "fever": {
        "title": "Fever Management",
        "summary": "Rest and drink plenty of fluids. Medication is not needed for a low-grade fever.",
        "url": "https://www.mayoclinic.org/diseases-conditions/fever/symptoms-causes/syc-20352759"
    },
    "chest pain": {
        "title": "Chest Pain: When to see a doctor",
        "summary": "Chest pain can be a sign of a heart attack. Seek emergency help if you have crushing pain.",
        "url": "https://www.mayoclinic.org/diseases-conditions/chest-pain/symptoms-causes/syc-20370838"
    }
}

SYMPTOM_PROMPT = """You are a medical triage assistant that extracts symptoms from a user's description.
Return STRICT JSON in the following format:
{
    "symptoms": ["list", "of", "symptoms"],
    "duration": "duration if mentioned, else null",
    "severity": "severity if mentioned, else null",
    "age_if_mentioned": "age if mentioned, else null"
}
"""

TRIAGE_PROMPT = """You are a medical triage AI. Analyze the symptoms and determine the triage level.
Possible levels: SELF_CARE, SEE_DOCTOR, EMERGENCY.
Provide a reason for your decision.
Return STRICT JSON:
{
    "triage": "LEVEL",
    "reason": "explanation"
}
"""

def clean_json_text(text: str) -> str:
    # Remove markdown code blocks if present
    text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    return text.strip()

class SymptomExtractorAgent:
    def run(self, user_input: str) -> SymptomExtract:
        if not client:
            raise ValueError("GOOGLE_API_KEY not set")
            
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{SYMPTOM_PROMPT}\nUser Input: {user_input}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        try:
            text = clean_json_text(response.text)
            data = json.loads(text)
            return SymptomExtract(**data)
        except Exception as e:
            print(f"JSON Parse Error in SymptomExtractor: {e}")
            # Fallback: try to find JSON object with regex
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                    return SymptomExtract(**data)
                except:
                    pass
            return SymptomExtract(symptoms=[])

class TriageAgent:
    def run(self, symptoms: SymptomExtract) -> TriageResult:
        if not client:
            raise ValueError("GOOGLE_API_KEY not set")

        # Rule-based fallback
        symptoms_lower = [s.lower() for s in symptoms.symptoms]
        if "chest pain" in symptoms_lower:
            return TriageResult(triage=TriageEnum.EMERGENCY, reason="Chest pain is a critical symptom requiring immediate attention.")
        
        # AI Triage
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{TRIAGE_PROMPT}\nSymptoms: {symptoms.model_dump_json()}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        try:
            text = clean_json_text(response.text)
            data = json.loads(text)
            return TriageResult(**data)
        except Exception as e:
            print(f"JSON Parse Error in TriageAgent: {e}")
            return TriageResult(triage=TriageEnum.SEE_DOCTOR, reason="Error in analysis, please consult a doctor.")

class InfoRetrieverAgent:
    def run(self, symptoms: SymptomExtract) -> List[TrustedInfo]:
        results = []
        for s in symptoms.symptoms:
            key = s.lower()
            # Simple substring match for the hardcoded list
            for trusted_key, info in TRUSTED_SOURCES.items():
                if trusted_key in key or key in trusted_key:
                    # Avoid duplicates
                    if not any(r.title == info['title'] for r in results):
                        results.append(TrustedInfo(**info))
        return results

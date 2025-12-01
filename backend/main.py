from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import UserMessage, TriageResponse
from backend.agents import SymptomExtractorAgent, TriageAgent, InfoRetrieverAgent
import uvicorn

app = FastAPI(title="Healthage AI Triage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

symptom_agent = SymptomExtractorAgent()
triage_agent = TriageAgent()
info_agent = InfoRetrieverAgent()

@app.get("/")
async def root():
    return {"message": "Healthage AI Triage API is running"}

@app.post("/api/triage", response_model=TriageResponse)
async def triage_endpoint(user_message: UserMessage):
    try:
        # 1. Extract
        symptoms = symptom_agent.run(user_message.message)
        
        # 2. Triage
        triage_result = triage_agent.run(symptoms)
        
        # 3. Retrieve Info
        trusted_info = info_agent.run(symptoms)
        
        return TriageResponse(
            symptom_analysis=symptoms,
            triage_result=triage_result,
            trusted_info=trusted_info
        )
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

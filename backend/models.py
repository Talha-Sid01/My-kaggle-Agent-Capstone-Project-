from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class TriageEnum(str, Enum):
    SELF_CARE = "SELF_CARE"
    SEE_DOCTOR = "SEE_DOCTOR"
    EMERGENCY = "EMERGENCY"

class SymptomExtract(BaseModel):
    symptoms: List[str]
    duration: Optional[str] = None
    severity: Optional[str] = None
    age_if_mentioned: Optional[str] = None

class TriageResult(BaseModel):
    triage: TriageEnum
    reason: str

class TrustedInfo(BaseModel):
    title: str
    summary: str
    url: str

class TriageResponse(BaseModel):
    symptom_analysis: SymptomExtract
    triage_result: TriageResult
    trusted_info: List[TrustedInfo]

class UserMessage(BaseModel):
    message: str

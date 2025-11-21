from pydantic import BaseModel
from typing import List, Optional, Dict

class Summary(BaseModel):
    bullet_points: List[str]

class LegislativeSection(BaseModel):
    definitions: Optional[List[str]] = []
    obligations: Optional[List[str]] = []
    responsibilities: Optional[List[str]] = []
    eligibility: Optional[List[str]] = []
    payments: Optional[List[str]] = []
    penalties: Optional[List[str]] = []

class Report(BaseModel):
    summary: Summary
    sections: LegislativeSection

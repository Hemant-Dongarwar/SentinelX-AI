from pydantic import BaseModel


class AIAnalysisResponse(BaseModel):
    name: str
    tactic: str
    risk_score: float
    analysis: str
    recommendation: list[str]
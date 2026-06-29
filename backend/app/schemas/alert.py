from pydantic import BaseModel


class AlertCreate(BaseModel):
    title: str
    description: str
    severity: str
    mitre: str


class AlertResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    mitre: str
    status: str

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    status: str
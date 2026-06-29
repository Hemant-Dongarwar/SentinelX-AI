from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_alerts: int
    open_alerts: int
    closed_alerts: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int
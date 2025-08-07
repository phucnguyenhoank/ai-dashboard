from pydantic import BaseModel


class AlertTypePercentage(BaseModel):
    type: str
    count: int
    percentage: float

class AlertStatistics(BaseModel):
    total_alerts: int
    unread_alerts: int
    read_alerts: int
    total_alert_percentages: list[AlertTypePercentage]
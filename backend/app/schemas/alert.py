from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.enums import AlertFrequency

class CreateAlert(BaseModel):
    query: str
    frequency: AlertFrequency = AlertFrequency.daily
    source: str = "google_rss"
    is_active: bool = True


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    query: str
    frequency: AlertFrequency
    source: str
    is_active: bool
    last_checked_at: datetime | None

     
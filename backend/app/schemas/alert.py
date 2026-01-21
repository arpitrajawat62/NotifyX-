from pydantic import BaseModel



class CreateAlert(BaseModel):
    query: str
    frequncy: str = "daily"

class AlertResponse(BaseModel):
    id: int
    query: str
    frequency: str
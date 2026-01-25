from pydantic import BaseModel



class CreateAlert(BaseModel):
    user_id: int
    query: str
    frequency: str = "daily"

class AlertResponse(BaseModel):
    id: int
    query: str
    frequency: str
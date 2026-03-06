from enum import Enum

class AlertFrequency(str, Enum):
    daily = "daily"
    weekly = "weekly"
    hourly = "hourly"
from pydantic import BaseModel
from datetime import date


class BookingModel(BaseModel):
    id: int
    guest_name: str
    booking_date: date
    length_of_stay: int
    daily_rate: float

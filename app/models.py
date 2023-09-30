from sqlalchemy import Column, Integer, String, Float, Date
from database import Base


# Определите модель SQLAlchemy на основе данных из DataFrame
class Booking(Base):
    __tablename__ = 'bookings'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    booking_date = Column(Date)
    length_of_stay = Column(Integer)
    guest_name = Column(String)
    daily_rate = Column(Float)

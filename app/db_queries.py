from sqlalchemy.orm import Session
from . import models, schemas


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def search_booking(db: Session, guest_name: str, book_date: str, length_of_stay: int):
    query = db.query(models.Booking)

    if guest_name:
        query = query.filter(models.Booking.guest_name == guest_name)

    if book_date:
        query = query.filter(models.Booking.booking_date == book_date)

    if length_of_stay is not None:
        query = query.filter(models.Booking.length_of_stay == length_of_stay)

    results = query.all()

    return results


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Annotated
from database import db_dependencies
from app.schemas import BookingModel
from app import db_queries
import settings
import app.dependencies as dep

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)


@router.get(
    '/',
    summary="Get a list of all bookings",
    status_code=status.HTTP_200_OK,
    response_model=list[BookingModel]
)
async def get_bookings(
        db: db_dependencies, skip: Annotated[int | None, Query(title="Number of values to skip",
                                                               description="Number of values to skip (from the beginning)")] = 0,
        limit: Annotated[int | None, Query(title="Limit number of entries",
                                           description="Limit number of entries (100 is optimal)")] = 100
):
    """
    Get a list of all bookings.

    Returns a list of all bookings in the database.

    - **db**: Dependency to obtain a database session.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    bookings = db_queries.get_bookings(db, skip=skip, limit=limit)
    return bookings


@router.get(
    '/search',
    summary="Search for bookings",
    status_code=status.HTTP_200_OK,
    response_model=list[BookingModel]
)
async def search_booking(
        db: db_dependencies,
        guest_name: Annotated[
            str | None, Query(title="Name of quest", description="Name of the guest to search for")] = None,
        book_date: Annotated[
            str | None, Query(title="Booking creating date", description="Booking date to search for", min_length=10,
                              max_length=10)] = None,
        length_of_stay: Annotated[
            int | None, Query(title="Number of days of stay", description="Length of stay to search for", ge=0)] = None
):
    """
    Search for bookings based on optional criteria.

    Returns a list of bookings that match the specified criteria.

    - **guest_name**: Name of the guest to search for.
    - **book_date**: Booking date to search for.
    - **length_of_stay**: Length of stay to search for.
    - **db**: Dependency to obtain a database session.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    results = db_queries.search_booking(db, guest_name, book_date, length_of_stay)

    if not results:
        raise HTTPException(status_code=404, detail="No bookings found")

    return results


@router.get(
    '/stats',
    summary="Provides statistical information about the dataset",
    status_code=status.HTTP_200_OK
)
async def get_stats():
    """
    Retrieve statistical information about the booking dataset.

    This endpoint calculates and returns various statistics based on the dataset of bookings.

    Returns a dictionary containing statistics such as the number of bookings, average length of stay,
             average daily rate, ten most common guest names, and ten most popular booking dates.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.stats_calculation()


@router.get(
    '/analysis',
    summary="Performs advanced analysis on the dataset",
    status_code=status.HTTP_200_OK
)
async def get_analysis():
    """
    Perform advanced analysis on the booking dataset.

    This endpoint performs advanced analysis on the dataset of bookings, generating insights and trends
    based on specific criteria such as booking trends by month and the popularity of meal packages.

    Returns a dictionary containing analysis results, including booking trends by month and the trends
             of meal packages based on booking frequency.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.analysis_calculation()


@router.get(
    '/{booking_id}',
    summary="Get a booking by its ID",
    status_code=status.HTTP_200_OK,
    response_model=BookingModel
)
async def get_booking_by_id(
        booking_id: Annotated[
            int, Path(..., title="Booking ID", description="The ID of the booking to retrieve", ge=0)],
        db: db_dependencies
):
    """
    Get a booking by its ID.

    Returns a single booking based on the provided ID.

    - **booking_id**: The ID of the booking to retrieve.
    - **db**: Dependency to obtain a database session.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    booking_by_id = db_queries.get_booking_by_id(db, booking_id)

    if not booking_by_id:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking_by_id

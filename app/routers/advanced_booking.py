from fastapi import APIRouter, HTTPException, Query, status
from typing import Annotated
from auth_dep import auth_dependencies
from app.schemas import BookingModel
import app.dependencies as dep
import settings

router = APIRouter(
    prefix='/bookings',
    tags=['Advanced bookings']
)


@router.get(
    '/nationality',
    summary="Get bookings based on nationality",
    status_code=status.HTTP_200_OK,
    response_model=list[BookingModel]
)
async def get_booking_by_nationality(
        country: Annotated[
            str, Query(title="The country", description="The country of nationality for which to retrieve bookings")]
):
    """
    Get bookings based on nationality.

    Returns bookings matching the provided nationality.

    Valid values: PRT, GBR, FRA, ESP, DEU, ITA, IRL, BEL, BRA, NLD, USA, CHE, CN, AUT, SWE, CHN, POL, ISR, RUS, NOR, ROU, FIN, DNK, AUS, AGO, LUX, MAR, TUR, HUN, ARG, JPN, CZE, IND, KOR, GRC, DZA, SRB, HRV, MEX, EST, IRN, LTU, ZAF, BGR, NZL, COL, UKR, MOZ, CHL, SVK, THA, SVN, ISL, LVA, ARE, CYP, TWN, SAU, PHL, TUN, SGP, IDN, NGA, EGY, URY, LBN, PER, HKG, MYS, ECU, VEN, BLR, CPV, GEO, JOR, KAZ, CRI, GIB, MLT, OMN, AZE, KWT, MAC, QAT, IRQ, DOM, PAK, BIH, MDV, BGD, ALB, PRI, SEN, CMR, MKD, BOL, PAN, GNB, TJK, VNM, CUB, ARM, JEY, LBY, AND, MUS, LKA, CIV, JAM, KEN, FRO, MNE, TZA, BHR, CAF, SUR, PRY, BRB, GTM, UZB, MCO, GAB, GHA, ZWE, ETH, TMP, LIE, GGY, SYR, BEN, GLP, SLV, ATA, MYT, ABW, KHM, LAO, STP, ZMB, MWI, IMN, COM, TGO, UGA, KNA, RWA, SYC, KIR, SDN, NCL, AIA, ASM, FJI, ATF, LCA, GUY, PYF, DMA, SLE, MRT, NIC, BDI, PLW, MLI, CYM, BFA, MDG, MMR, NPL, BHS, UMI, SMR, DJI, BWA, HND, VGB, NAM

    - **country**: The country of nationality for which to retrieve bookings.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    results = dep.filtering_by_nationality(country)

    if not results:
        raise HTTPException(status_code=404, detail="No bookings found")

    return results


@router.get(
    '/popular_meal_package',
    summary="Retrieves the most popular meal package among all bookings",
    status_code=status.HTTP_200_OK
)
async def get_popular_meal_package():
    """
    Retrieves the most popular meal package among all bookings.

    Returns the most popular meal package.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.popular_meal_package()


@router.get(
    '/avg_length_of_stay',
    summary="Retrieves the average length of stay grouped by booking year and hotel type",
    status_code=status.HTTP_200_OK
)
async def get_avg_length_of_stay():
    """
    Retrieves the average length of stay grouped by booking year and hotel type.

    Returns the average length of stay for each combination of booking year and hotel type.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.avg_length_of_stay()


@router.get(
    '/total_revenue',
    summary="Retrieves the total revenue",
    status_code=status.HTTP_200_OK
)
async def get_total_revenue():
    """
    Retrieves the total revenue grouped by booking month and hotel type.

    Returns the total revenue for each combination of booking month and hotel type.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.total_revenue()


@router.get(
    '/top_countries',
    summary="Retrieves the top 5 countries with the highest number of bookings",
    status_code=status.HTTP_200_OK
)
async def get_top_countries():
    """
    Retrieves the top 5 countries with the highest number of bookings.

    Returns the top 5 countries with the most bookings.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.top_countries()


@router.get(
    '/repeated_guests_percentage',
    summary="Retrieves the percentage of repeated guests among all bookings",
    status_code=status.HTTP_200_OK
)
async def get_repeated_guests_percentages():
    """
    Retrieves the percentage of repeated guests among all bookings.

    Returns the percentage of repeated guests.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.repeated_guests_percentages()


@router.get(
    '/total_guests_by_year',
    summary="Retrieves the total number of guests (adults, children, and babies) by booking year",
    status_code=status.HTTP_200_OK
)
async def get_total_guests_by_year():
    """
    Retrieves the total number of guests (adults, children, and babies) by booking year.

    Returns the total number of guests by booking year.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.total_guests_by_year()


@router.get(
    '/avg_daily_rate_resort',
    summary="Retrieves the average daily rate by month for resort hotel bookings",
    status_code=status.HTTP_200_OK
)
async def get_avg_daily_rate_resort(username: auth_dependencies):
    """
    Retrieves the average daily rate by month for resort hotel bookings.

    Returns the average daily rate by month for resort hotel bookings.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.avg_daily_rate_resort()


@router.get(
    '/most_common_arrival_day_city',
    summary="Retrieves the most common arrival date day of the week for city hotel bookings",
    status_code=status.HTTP_200_OK
)
async def get_most_common_arrival_day_city(username: auth_dependencies):
    """
    Retrieves the most common arrival date day of the week for city hotel bookings.

    Returns the most common arrival date day of the week for city hotel.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.most_common_arrival_day_city()


@router.get(
    '/count_by_hotel_meal',
    summary="Retrieves the count of bookings grouped by hotel type and meal package",
    status_code=status.HTTP_200_OK
)
async def get_count_by_hotel_meal(username: auth_dependencies):
    """
    Retrieves the count of bookings grouped by hotel type and meal package.

    Returns the count of bookings by hotel type and meal package.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.count_by_hotel_meal()


@router.get(
    '/total_revenue_resort_by_country',
    summary="Retrieves the total revenue by country for resort hotel bookings",
    status_code=status.HTTP_200_OK
)
async def get_total_revenue_resort_by_country(username: auth_dependencies):
    """
    Retrieves the total revenue by country for resort hotel bookings.

    Returns the total revenue by country for resort hotel bookings.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.total_revenue_resort_by_country()


@router.get(
    '/count_by_hotel_repeated_guest',
    summary="Retrieves the count of bookings grouped by hotel type and repeated guest status",
    status_code=status.HTTP_200_OK
)
async def get_count_by_hotel_repeated_guest(username: auth_dependencies):
    """
    Retrieves the count of bookings grouped by hotel type and repeated guest status.

    Returns the count of bookings by hotel type and repeated guest status.
    """
    if not settings.file_uploaded:
        raise HTTPException(status_code=400, detail="File not uploaded yet")

    return dep.count_by_hotel_repeated_guest()

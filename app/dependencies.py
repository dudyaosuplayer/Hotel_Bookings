from datetime import datetime
from config import settings
# from database import SQLALCHEMY_DATABASE_URL
import pandas as pd


def stats_calculation() -> dict:
    """
    Calculate statistics based on the data in the DataFrame `new_df`.

    Returns a dictionary containing the following statistics:

    - 'number_of_bookings': Total number of bookings in the dataset.
    - 'average_length_of_stay': Average length of stay across all bookings.
    - 'average_daily_rate': Average daily rate across all bookings.
    - 'ten_most_common_quests': List of ten most common guest names.
    - 'ten_most_popular_dates': List of ten most popular booking dates.

    Returns a dictionary with calculated statistics.
    """
    new_df = pd.read_sql_table('bookings', settings.DATABASE_URL_psycopg)
    number_of_bookings = len(new_df)
    average_length_of_stay = new_df['length_of_stay'].mean()
    average_daily_rate = new_df['daily_rate'].mean()
    ten_most_common_guests = new_df['guest_name'].value_counts().head(10).index.to_list()
    ten_most_popular_dates = new_df['booking_date'].value_counts().head(10).index.to_list()

    return {
        'number_of_bookings': number_of_bookings,
        'average_length_of_stay': average_length_of_stay,
        'average_daily_rate': average_daily_rate,
        'ten_most_common_guests': ten_most_common_guests,
        'ten_most_popular_dates': ten_most_popular_dates
    }


def analysis_calculation() -> dict:
    """
    Calculate advanced analysis based on the data in the DataFrame `df`.

    Returns a dictionary containing the following analysis results:

    - 'booking_trends_by_month': Trends of bookings by month.
    - 'meal_packages_trends': Trends of meal packages.

    Returns a dictionary with calculated analysis results.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    trends_by_month = df['arrival_date_month'].value_counts().to_dict()
    trends_meal_packages = df['meal'].value_counts().to_dict()
    guest_demographics = df['country'].value_counts().to_dict()
    analysis = df.describe().to_dict()

    return {
        'booking_trends_by_month': trends_by_month,
        'meal_packages_trends': trends_meal_packages,
        'guest_demographics': guest_demographics,
        'analysis': analysis
    }


def filtering_by_nationality(country: str) -> list:
    """
    Filters booking data by guest nationality and returns the result as a list of dictionaries.

    Args:
        country (str): The nationality to filter by.

    Returns:
        list[dict]: A list of dictionaries containing booking data filtered by the specified nationality.
            Each dictionary represents a single booking and includes the following keys:
            - 'id': Unique booking identifier.
            - 'booking_date': Booking date.
            - 'length_of_stay': Length of stay in days.
            - 'guest_name': Guest's name.
            - 'daily_rate': Daily rate.

    """
    new_df = pd.read_sql_table('bookings', settings.DATABASE_URL_psycopg)
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    filtered_df = df[df['country'] == country]
    selected_indices = filtered_df.index
    filtered_by_country = new_df.loc[
        new_df.index.isin(selected_indices), ['id', 'booking_date', 'length_of_stay', 'guest_name', 'daily_rate']]
    return filtered_by_country.to_dict(orient='records')


def popular_meal_package() -> dict:
    """
    Determines the most popular meal package based on booking data and returns information about it.

    Returns:
        dict: A dictionary containing information about the most popular meal package:
            - 'Top meal': The name of the most popular meal package.
            - 'Frequency': The number of times this package was selected.

    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    result = df['meal'].value_counts().nlargest(1)
    top_meal = str(result.index[0])
    frequency = int(result.iloc[0])

    response_data = {
        "Top meal": top_meal,
        "Frequency": frequency
    }

    return response_data


def avg_length_of_stay() -> list:
    """
    Calculate the average length of stay per year and hotel.

    This function calculates the average length of stay for guests based on the provided DataFrame.
    It groups the data by 'arrival_date_year' and 'hotel', calculates the mean length of stay,
    and returns the result as a list of dictionaries.

    Returns:
        List[Dict[str, Union[int, float]]]: A list of dictionaries, each containing:
            - 'arrival_date_year' (int): The year of arrival.
            - 'hotel' (str): The type of hotel.
            - 'length_of_stay' (float): The average length of stay for the specified year and hotel.
    """
    new_df = pd.read_sql_table('bookings', settings.DATABASE_URL_psycopg)
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['stays_in_weekend_nights', 'stays_in_week_nights', 'arrival_date_year', 'arrival_date_month',
                    'arrival_date_day_of_month', 'hotel']].copy()

    copied_df['length_of_stay'] = copied_df['stays_in_weekend_nights'] + copied_df['stays_in_week_nights']

    copied_df['booking_date_year'] = pd.to_datetime(new_df['booking_date']).dt.year

    # Calculate the mean and reset the index
    result_df = copied_df.groupby(['booking_date_year', 'hotel'])['length_of_stay'].mean().reset_index()

    # Convert the result to a dictionary
    result_dict = result_df.to_dict(orient='records')
    return result_dict


def total_revenue() -> list:
    """
    Calculates the total revenue by month and hotel.

    This function calculates the total revenue generated by each hotel for each month,
    excluding canceled bookings. It filters the DataFrame for non-canceled bookings,
    groups the data by arrival month and hotel, and sums the 'adr' (average daily rate) column.
    The result is returned as a list of dictionaries.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries, where each dictionary
        contains the 'arrival_date_month', 'hotel', and 'adr_sum' (total revenue) for a specific
        month and hotel.

    """
    new_df = pd.read_sql_table('bookings', settings.DATABASE_URL_psycopg)
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[
        ['adr', 'stays_in_weekend_nights', 'stays_in_week_nights', 'is_canceled', 'arrival_date_month', 'hotel']].copy()
    copied_df['booking_date_month'] = pd.to_datetime(new_df['booking_date']).dt.strftime('%B')
    copied_df['revenue'] = copied_df['adr'] * (copied_df['stays_in_weekend_nights'] + copied_df['stays_in_week_nights'])
    result_df = copied_df[copied_df['is_canceled'] == 0].groupby(['booking_date_month', 'hotel'])[
        'revenue'].sum().reset_index()
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def top_countries() -> dict:
    """
    Retrieves the top five countries with the most bookings.

    This function counts the number of bookings made by each country in the dataset
    and returns the top five countries with the highest booking counts as a dictionary.

    Returns:
        Dict[str, int]: A dictionary where keys are country codes and values are the
        respective booking counts.

    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    return df['country'].value_counts().head(5).to_dict()


def repeated_guests_percentages() -> dict:
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    repeated_guests = len(df[df['is_repeated_guest'] == 1])
    all_guests = len(df)

    return {
        'all_bookings': all_guests,
        'repeated_guests': repeated_guests,
        'percentage_of_repeated_guests': repeated_guests / all_guests * 100
    }


def total_guests_by_year() -> list:
    """
    Calculate the total number of guests (adults, children, and babies) by booking year.

    Returns:
        list: A list of dictionaries, each representing the total number of guests by booking year.
            Each dictionary includes the following keys:
            - 'booking_date_year': The booking year.
            - 'total_guests': The total number of guests for that year.
    """
    new_df = pd.read_sql_table('bookings', settings.DATABASE_URL_psycopg)
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['adults', 'children', 'babies']].copy()
    copied_df['booking_date_year'] = pd.to_datetime(new_df['booking_date']).dt.year
    copied_df['total_guests'] = copied_df[['adults', 'children', 'babies']].sum(axis=1)

    result_df = copied_df.groupby('booking_date_year')['total_guests'].sum().reset_index()
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def avg_daily_rate_resort() -> list:
    """
    Calculate the average daily rate for the 'Resort Hotel' by month.

    Returns:
        list: A list of dictionaries, each representing the average daily rate for the 'Resort Hotel' by month.
            Each dictionary includes the following keys:
            - 'month': The month of arrival.
            - 'adr': The average daily rate for that month.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['hotel', 'arrival_date_month', 'adr']]
    copied_df = copied_df.rename(columns={'arrival_date_month': 'month'})
    filtered_df = copied_df[copied_df['hotel'] == 'Resort Hotel']
    result_df = filtered_df.groupby('month')['adr'].mean().reset_index()
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def most_common_arrival_day_city() -> list:
    """
    Find the most common arrival day for the 'City Hotel'.

    Returns:
        list: A list of dictionaries, each representing the most common arrival day for the 'City Hotel'.
            Each dictionary includes the following keys:
            - 'most_common_arrival_day': The most common arrival day of the week.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    df['arrival_date_month'] = df['arrival_date_month'].apply(lambda x: datetime.strptime(x, '%B').month)
    df['booking_date_arrival'] = df.apply(
        lambda row: datetime(row['arrival_date_year'], row['arrival_date_month'], row['arrival_date_day_of_month']),
        axis=1)
    df['booking_date_arrival'] = df['booking_date_arrival'].dt.strftime('%Y-%m-%d')
    copied_df = df[['booking_date_arrival', 'hotel']].copy()
    copied_df['booking_date_arrival'] = pd.to_datetime(copied_df['booking_date_arrival']).dt.strftime('%A')
    copied_df = copied_df.rename(columns={'booking_date_arrival': 'most_common_arrival_day'})
    result_df = copied_df[copied_df['hotel'] == 'City Hotel']['most_common_arrival_day'].value_counts().head(
        1).reset_index()
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def count_by_hotel_meal() -> list:
    """
    Count the number of bookings by hotel and meal type.

    Returns a list of dictionaries where each dictionary contains the following keys:
    - 'hotel': The hotel name.
    - 'meal': The meal type.
    - 'count': The number of bookings for the hotel and meal type.

    Returns:
        list[dict]: A list of dictionaries representing the count of bookings by hotel and meal type.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['hotel', 'meal']]
    result_df = copied_df.groupby(['hotel', 'meal']).size().reset_index(name='count').sort_values(by='count',
                                                                                                  ascending=False)
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def total_revenue_resort_by_country() -> list:
    """
    Calculate the total revenue for Resort Hotel by country.

    Returns a list of dictionaries where each dictionary contains the following keys:
    - 'country': The country name.
    - 'total_revenue': The total revenue generated by bookings in the Resort Hotel for that country.

    Returns:
        list[dict]: A list of dictionaries representing the total revenue for Resort Hotel by country.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['adr', 'stays_in_weekend_nights', 'stays_in_week_nights', 'is_canceled', 'hotel', 'country']].copy()
    copied_df['total_revenue'] = copied_df['adr'] * (
            copied_df['stays_in_weekend_nights'] + copied_df['stays_in_week_nights'])
    result_df = copied_df[(copied_df['is_canceled'] == 0) & (copied_df['hotel'] == 'Resort Hotel')].groupby('country')[
        'total_revenue'].sum().reset_index().sort_values(by='total_revenue', ascending=False)
    result_dict = result_df.to_dict(orient='records')

    return result_dict


def count_by_hotel_repeated_guest() -> list:
    """
    Count the number of repeated and not repeated guests by hotel.

    Returns a list of dictionaries where each dictionary contains the following keys:
    - 'hotel': The hotel name.
    - 'is_repeated_guest': Whether the guest is repeated or not ('repeated' or 'not_repeated').
    - 'count': The number of guests in each category for the hotel.

    Returns:
        list[dict]: A list of dictionaries representing the count of repeated and not repeated guests by hotel.
    """
    df = pd.read_csv('app/data/hotel_booking_data.csv')
    copied_df = df[['is_repeated_guest', 'hotel']]
    result_df = copied_df.groupby(['hotel', 'is_repeated_guest']).size().reset_index(name='count')

    result_df['is_repeated_guest'] = result_df['is_repeated_guest'].replace({0: 'not_repeated', 1: 'repeated'})
    result_dict = result_df.to_dict(orient='records')

    return result_dict

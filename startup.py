import os
from datetime import datetime
from database import engine
import pandas as pd


async def process_and_save_csv(df):
    """
    Process a DataFrame and save it to a SQL database.

    :param df: A pandas DataFrame containing data to be processed and saved.
    :return: A dictionary with a success message.
    """
    selected_columns = ['name', 'adr', 'stays_in_weekend_nights', 'stays_in_week_nights', 'arrival_date_year',
                        'arrival_date_month', 'arrival_date_day_of_month', 'hotel']
    new_df = df[selected_columns]

    new_df = new_df.rename(columns={
        'name': 'guest_name',
        'adr': 'daily_rate',
        'stays_in_weekend_nights': 'stays_in_weekend_nights',
        'stays_in_week_nights': 'stays_in_week_nights',
        'arrival_date_year': 'booking_date_year',
        'arrival_date_month': 'booking_date_month',
        'arrival_date_day_of_month': 'booking_date_day',
    })

    new_df['id'] = list(new_df.index)

    new_df['booking_date_month'] = new_df['booking_date_month'].apply(lambda x: datetime.strptime(x, '%B').month)
    new_df['booking_date_arrival'] = new_df.apply(
        lambda row: datetime(row['booking_date_year'], row['booking_date_month'], row['booking_date_day']), axis=1)
    new_df['booking_date_arrival'] = new_df['booking_date_arrival'].dt.strftime('%Y-%m-%d')

    new_df['booking_date'] = pd.to_datetime(new_df['booking_date_arrival']) - pd.to_timedelta(df['lead_time'], unit='D')
    new_df['booking_date'] = new_df['booking_date'].dt.strftime('%Y-%m-%d')

    new_df['length_of_stay'] = new_df['stays_in_weekend_nights'] + new_df['stays_in_week_nights']

    new_df[['id', 'booking_date', 'length_of_stay', 'guest_name', 'daily_rate']].to_sql('bookings', engine,
                                                                                        if_exists='replace',
                                                                                        index=False)
    return {"message": "CSV file processed and data saved successfully"}


def save_dataframe_as_csv(df, filename):
    """
    Save a DataFrame as a CSV file.

    :param df: A pandas DataFrame to be saved.
    :param filename: The name of the CSV file.
    """
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/data")

    output_path = os.path.join(data_dir, filename)
    df.to_csv(output_path, index=False)

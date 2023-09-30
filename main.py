import pandas as pd
import config
import uvicorn
import atexit
import os
import settings
from typing import Annotated
from fastapi import FastAPI, UploadFile, File, status
from app.routers import booking, advanced_booking
from user.routes import router as user_routes
from database import engine
from startup import process_and_save_csv, save_dataframe_as_csv
from user import models as user_models
from app import models as app_models


# Function to delete all files in the folder on application exit
def delete_files_in_folder_on_exit():
    """
    Delete files in the 'app/data' folder on application exit.

    This function attempts to delete all files located in the 'app/data' folder when the application exits.
    It iterates through the files in the folder and removes each file individually. Any errors encountered during
    file deletion are caught and printed as error messages.

    Note:
    The function is designed to run on application exit and may not work as expected if called explicitly.
    """
    try:
        current_directory = os.path.dirname(__file__)
        data_directory = os.path.join(current_directory, 'app', 'data')
        for filename in os.listdir(data_directory):
            file_path = os.path.join(data_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File {file_path} successfully deleted")
            except Exception as e:
                print(f"Error deleting file {file_path}: {str(e)}")
    except NameError:
        pass


# Register the function to be executed on application exit
atexit.register(delete_files_in_folder_on_exit)

user_models.Base.metadata.create_all(engine)
app_models.Base.metadata.create_all(engine)

app = FastAPI()


@app.post(
    "/upload-and-process-csv",
    tags=["CSV file upload"],
    summary="Upload booking data from csv file",
    status_code=status.HTTP_200_OK
)
async def upload_and_process_csv(csv_file: Annotated[UploadFile, File(..., description="Csv file with booking data")]):
    """
    Upload booking data from csv file and create filling bookings table with it.

    Returns a message about result of operation.

    - **csv_file**: Csv file with booking data.
    """
    df = pd.read_csv(csv_file.file)
    result = await process_and_save_csv(df)
    save_dataframe_as_csv(df, csv_file.filename)

    settings.file_uploaded = True

    return result


app.include_router(user_routes)
app.include_router(advanced_booking.router)
app.include_router(booking.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host=config.HOST, port=int(config.PORT), reload=True)

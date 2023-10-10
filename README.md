Hotels Booking FastAPI application.

Used in the project:
- **SQLAlchemy**
- **FastAPI**
- **Pandas**


Steps to start a project:

1. Run project from main.py;
2. Wait until the server starts;
3. Go to URL: http://127.0.0.1:8000/docs (Swagger UI);
4. First upload the file 'hotel_booking_data.csv' via endpoint: **/upload-and-process-csv**;
    - Wait until the file downloads!
5. Use edpoints that do not require authentication;
6. To access private endpoints, you need to create a user via POST **/users** endpoint, or authenticate through existing users (the list of users can be obtained by GET **/users** endpoint)
7. You can also change (PUT **/users**) or delete (DELETE **/users**) a user, but you need to be authenticated to do this!
8. **After stopping the application, the downloaded file is deleted!!!**

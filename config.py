from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
DB_NAME = os.environ.get('DB_NAME')
USERNAME_AUTH = os.environ.get('USERNAME_AUTH')
PASSWORD_AUTH = os.environ.get('PASSWORD_AUTH')

# Connection to the Olive Owl's database (PostgreSQL)
import os
import psycopg # PostgreSQL database adapter for Python

from pathlib import Path
from dotenv import load_dotenv


# Get the .env file in the project's root directory
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def get_database_connection():
    """ Create & return the PostgreSQL database connection """
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),

        connect_timeout=5,
    )

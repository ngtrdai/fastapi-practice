import os
from dotenv import load_dotenv

load_dotenv()

def get_connection_string():
    db_engine = os.getenv("DATABASE_DIALECT")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_name = os.getenv("POSTGRES_DB")
    return f"{db_engine}://{db_user}:{db_password}@{db_host}/{db_name}"

# Database Setting
SQLALCHEMY_DATABASE_URI = get_connection_string()
ADMIN_DEFAULT_PASSWORD = os.getenv("ADMIN_DEFAULT_PASSWORD")

# JWT Setting
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
from sqlmodel import create_engine, Session
from app.database.config import settings

# Construct the PostgreSQL connection string using values from the settings
# DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create the SQLite engine
engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
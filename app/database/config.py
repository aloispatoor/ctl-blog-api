import os
from dotenv import load_dotenv
from pathlib import Path

# Define the path to .env file
env_path = Path('') / '.env'

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)


class Settings:
    # SQLite config
    database_url: str = "sqlite:///blog.db"
    PROJECT_NAME: str = "Blog API"
    PROJECT_VERSION: str = "0.1.0"

    # Database connection settings using environment variables
    # database_username: str = os.getenv("POSTGRES_USERNAME", "postgres")
    # database_password: str = os.getenv("POSTGRES_PASSWORD", "S3cr3t")
    # database_hostname: str = os.getenv("POSTGRES_HOSTNAME", "localhost")
    # database_port: int = os.getenv("POSTGRES_PORT", 5432)
    # database_name: str = os.getenv("POSTGRES_DB", "blog")


# Instantiate the Settings class
settings = Settings()
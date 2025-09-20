from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from fastapi import FastAPI

from app.database.db import engine
from app.database.config import settings
from app.routers import posts


# def wait_for_db():
#     max_retries = 30
#     retry_count = 0
#     DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#     print(f"🔗 Database URL : {DATABASE_URL}")
#
#     while retry_count < max_retries:
#         try:
#             with engine.connect() as connection:
#                 print("database connection established")
#                 return True
#         except Exception as e:
#             retry_count += 1
#             print(f"Retry attempt #{retry_count}")
#             print(f"Detailed error : {type(e).__name__}: {str(e)}")
#     raise Exception("Timed out")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up")
    # wait_for_db()
    # Create the database tables if they don't exist yet
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown or cleanup
    print("Shutting down")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

@app.get("/")
async def root():
    return {"message": f'Welcome to {settings.PROJECT_NAME}'}
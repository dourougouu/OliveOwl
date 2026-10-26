from fastapi import FastAPI, HTTPException
from psycopg import Error

from app.database import get_database_connection
from app.routes import router

app = FastAPI(
    title="Olive Owl API",
    description="An Olive mill management application",
    version="0.1.0",
)

app.include_router(router)

@app.get("/")
def root():
    return{ "message": "Welcome to Olive Owl API!",
            "status": "running",
            }

@app.get("/health")
def health():
    return { "status": "healthy",
            }

## endpoint select to check which db we are using & the PostgreSQL version
@app.get("/health/database")
def health_of_database():
    try:
        with get_database_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT current_database(), version()")
                database_name, database_version = cursor.fetchone()

        return {
            "status": "connected",
            "database": database_name,
            "postgreSQL_version": database_version,
        }

    except (Error, OSError):
        raise HTTPException(status_code=503, detail="Database connection has failed. Check again the configuration.",)

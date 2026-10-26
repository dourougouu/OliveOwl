from fastapi import APIRouter, HTTPException, status
from psycopg import Error
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation

from app.database import get_database_connection
from app.schemas import ProducerCreate

router = APIRouter()

@router.get("/producers")
def get_producers():
    try:
        with get_database_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(""" SELECT id,
                                          first_name,
                                          last_name,
                                          dhmos
                                    FROM producer
                                    ORDER BY last_name, first_name; """)

                producers = cursor.fetchall()
        return {"producers": producers,
                "count": len(producers)}

    except Error:
        raise HTTPException(status_code=503, detail="Could not retrieve producers from the database!")

@router.post("/producers", status_code=status.HTTP_201_CREATED)
def create_producer(producer: ProducerCreate):
    query = """ INSERT INTO producer (
                                        first_name,
                                        last_name,
                                        fathers_name,
                                        phone_number,
                                        home_number,
                                        address,
                                        afm,
                                        "adt",
                                        tk,
                                        dhmos,
                                        doy,
                                        notes
                                        ) 
                VALUES (
                        %(first_name)s,
                        %(last_name)s,
                        %(fathers_name)s,
                        %(phone_number)s,
                        %(home_number)s,
                        %(address)s,
                        %(afm)s,
                        %(adt)s,
                        %(tk)s,
                        %(dhmos)s,
                        %(doy)s,
                        %(notes)s
                        ) 
                RETURNING id, first_name, last_name, dhmos; """

    try:
        with get_database_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, producer.model_dump())
                new_producer = cursor.fetchone()

        return {"message": "Producer created successfully!", "producer": new_producer,}

    except UniqueViolation:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Producer with the same AFM already exists!",)

    except Error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Could not create producer in the database",)

    
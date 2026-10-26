from fastapi import APIRouter, HTTPException, status
from psycopg import Error
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from app.database import get_database_connection
from app.schemas import ProducerCreate, DeliveryCreate

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



@router.get("/product_deliveries")
def get_deliveries():
    query = """ SELECT  d.id,
                        d.producer_id,
                        p.first_name,
                        p.last_name,
                        d.delivery_date,
                        d.olive_weight_kg,
                        d.olive_variety,
                        d.notes,
                        d.created_at
                FROM olive_productdeliv AS d
                JOIN producer AS p
                    ON p.id = d.producer_id
                ORDER BY d.delivery_date DESC, d.id DESC; """

    try:
        with get_database_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                deliveries = cursor.fetchall()

        return {
            "product_deliveries": deliveries,
            "count": len(deliveries),
        }

    except Error:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve deliveries from the database.",
        )


@router.post("/product_deliveries", status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate):
    query = """ INSERT INTO olive_productdeliv(
                                                producer_id,
                                                delivery_date,
                                                olive_weight_kg,
                                                olive_variety,
                                                notes
                                                )
                VALUES (
                        %(producer_id)s,
                        %(delivery_date)s,
                        %(olive_weight_kg)s,
                        %(olive_variety)s,
                        %(notes)s
                        )
                RETURNING id, producer_id, delivery_date, olive_weight_kg, olive_variety, notes, created_at; """

    try: 
        with get_database_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, delivery.model_dump())
                new_delivery = cursor.fetchone()

        return {
            "message": "Delivery created successfully!",
            "product_delivery": new_delivery,
        }

    except ForeignKeyViolation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The specified producer doesn't exist in the database!",)

    except Error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Could not create delivery in the database",)

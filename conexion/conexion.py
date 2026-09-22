import os
import psycopg2


def obtener_conexion():
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="kookie",
        database="ferreteria"
    )
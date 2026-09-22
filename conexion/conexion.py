import psycopg2


def obtener_conexion():
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="kookie",
        database="ferreteria"
    )

    return conexion
import mysql.connector

def db_connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='tienda_libros'
    )
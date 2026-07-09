import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kartik@07",
        database="face_attendance"
    )

    return connection
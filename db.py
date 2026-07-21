import mysql.connector

def get_db_connection():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radhi",
        database="employee_management"
    )
    return con
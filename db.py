import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="harini",
        database="hospital_db"
    )
from flask import Flask
import psycopg2

# from classes.database_handler import DatabaseHandler
# from PyQt6.QtSql import QSqlQuery

app = Flask(__name__)

DB_HOST = "localhost"
DB_PORT = 5432
# DB_PORT = 5435  # Docker
DB_NAME = "lotnisko"
DB_USER = "postgres"
DB_PASSWORD = "password"


def connect_to_database():
    connection = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return connection


def get_from_database(query):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    except Exception as e:
        print({"error": str(e)})


@app.route("/api/data/<table_name>")
def get_data(table_name):
    data = get_from_database(f"SELECT * FROM {table_name}")
    print(type(data))
    return data


if __name__ == "__main__":
    # db_handler = DatabaseHandler(
    #     database_name=DB_NAME,
    #     host=DB_HOST,
    #     username=DB_USER,
    #     password=DB_PASSWORD,
    #     port=DB_PORT,
    # )
    # db_handler.create_connection()
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)

    # http://192.168.100.26:5000/get_data

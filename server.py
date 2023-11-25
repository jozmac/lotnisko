from flask import Flask
import psycopg2

# from classes.database_handler import DatabaseHandler
# from PyQt6.QtSql import QSqlQuery

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "lotnisko",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432,
    # "port": 5435, # Docker
}


def connect_to_database():
    connection = psycopg2.connect(**DB_CONFIG)
    return connection


def get_from_database(query, params=None):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    except Exception as e:
        print({"error": str(e)})


@app.route("/api/data/<table_name>")
def get_data(table_name):
    query = "SELECT * FROM %(table_name)s"
    params = {"table_name": table_name}
    data = get_from_database(query, params)
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

from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "lotnisko"
DB_USER = "postgres"
DB_PASSWORD = "password"


def connect_to_database():
    connection = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return connection


@app.route("/")
def hello():
    return """
        <html>
            <head><title>Czesc!</title><head>
            <body>
                <h1>Witam</h1>
            </body>
        </html>
    """


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
        return {"error": str(e)}


@app.route("/get_data")
def get_data():
    data = get_from_database("SELECT * FROM osoba")
    print(type(data))
    result = [{"id": row[0], "imie": row[1], "nazwisko": row[2]} for row in data]
    print(type(result))
    return result


@app.route("/<url_query>")
def hello_name(url_query):
    query = url_query.replace("%", " ")
    data = get_from_database(query)
    return data


# @app.route("/query", methods=["GET", "POST"])
# def query():
#     return render_template("query.html")


if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run()

    # http://192.168.100.26:5000/get_data

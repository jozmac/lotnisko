from PyQt6.QtSql import QSqlDatabase


def create_connection():
    try:
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("localhost")
        db.setDatabaseName("lotnisko")
        db.setUserName("postgres")
        db.setPassword("password")
        db.setPort(5432)

        if not db.open():
            raise ConnectionError(
                f"Could not open database. Error: {db.lastError().text()}"
            )
        return db
    except Exception as e:
        raise ConnectionError(f"Connection error: {e}")


class DatabaseHandler:
    def __init__(self):
        self.db = create_connection()

    def close_connection(self):
        self.db.close()
        if self.db.isOpen():
            print("Database is still open.")
        else:
            print("Database closed.")

# import psycopg2 as pg2


# class DatabaseHandler:
#     def __init__(self, database_name="lotnisko"):
#         self.database_name = database_name
#         # self.con = None

#     def create_connection(self):
#         try:
#             self.con = pg2.connect(
#                 host="localhost",
#                 database=self.database_name,
#                 user="postgres",
#                 password="password",
#                 port="5432",
#             )
#             return self.con
#         except Exception as e:
#             raise ConnectionError(f"Connection error: {e}")

#     def close_connection(self):
#         if self.con:
#             self.con.close()
#             self.con = None
#             print("Database closed.")
#         else:
#             print("No open database connection to close.")

#     def execute_query(self, query):
#         if not self.con:
#             raise ConnectionError("No open database connection.")
#         try:
#             with self.con.cursor() as cursor:
#                 cursor.execute(query)
#                 self.con.commit()
#             print("Query executed successfully.")
#         except Exception as e:
#             print(f"Error executing query: {e}")


from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class DatabaseHandler:
    def __init__(self, database_name="lotnisko"):
        self.database_name = database_name

    def create_connection(self):
        try:
            self.con = QSqlDatabase.addDatabase("QPSQL")
            self.con.setHostName("localhost")
            self.con.setDatabaseName(self.database_name)
            self.con.setUserName("postgres")
            self.con.setPassword("password")
            self.con.setPort(5432)

            if not self.con.open():
                raise ConnectionError(
                    f"Could not open database. Error: {self.con.lastError().text()}"
                )
            return self.con
        except Exception as e:
            raise ConnectionError(f"Connection error: {e}")

    def close_connection(self):
        self.con.close()
        if self.con.isOpen():
            print("Database is still open.")
        else:
            print("Database closed.")

    def execute_query(self, query):
        qsqlquery = QSqlQuery(query, self.con)
        print(qsqlquery.exec())
        # if qsqlquery.exec():
        #     print(f"Data inserted successfully.")
        # else:
        #     # print(f"Error inserting data: {query.lastError().text()}")
        #     print("Error inserting data.")


# TODO
# from PyQt6.QtSql import QSqlDatabase

# connection_string = f"postgresql://{username}:{password}@localhost:5432/{database_name}"

# class DatabaseHandler:
#     def __init__(self, connection_string="postgresql://postgres:password@localhost:5432/lotnisko"):
#         self.connection_string = connection_string
#         self.db = self.create_connection()

#     def create_connection(self):
#         try:
#             db = QSqlDatabase.addDatabase("QPSQL")
#             db.setDatabaseName(self.connection_string)

#             if not db.open():
#                 raise ConnectionError(
#                     f"Could not open database. Error: {db.lastError().text()}"
#                 )
#             return db
#         except Exception as e:
#             raise ConnectionError(f"Connection error: {e}")

#     def close_connection(self):
#         self.db.close()
#         if self.db.isOpen():
#             print("Database is still open.")
#         else:
#             print("Database closed.")

#     def execute_query(self, query):
#         if query.exec():
#             print(f"Data inserted successfully.")
#         else:
#             print(f"Error inserting data: {query.lastError().text()}")


# from PyQt6.QtSql import QSqlDatabase


# class DatabaseHandler:
#     def __init__(
#         self, database_name="lotnisko", username="postgres", password="password"
#     ):
#         self.connection_string = (
#             f"postgresql://{username}:{password}@localhost:5432/{database_name}"
#         )

#     def create_connection(self):
#         try:
#             self.con = QSqlDatabase.addDatabase("QPSQL")
#             self.con.setDatabaseName(self.connection_string)

#             if not self.con.open():
#                 raise ConnectionError(
#                     f"Could not open database. Error: {self.con.lastError().text()}"
#                 )
#             return self.con
#         except Exception as e:
#             raise ConnectionError(f"Connection error: {e}")

#     def close_connection(self):
#         self.db.close()
#         if self.db.isOpen():
#             print("Database is still open.")
#         else:
#             print("Database closed.")

#     def execute_query(self, query):
#         if query.exec():
#             print(f"Data inserted successfully.")
#         else:
#             print(f"Error inserting data: {query.lastError().text()}")
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QIcon
import sys, os
from Classes.DatabaseHandler import DatabaseHandler


class PersonDialog(QDialog):
    def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.init_gui()

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "person_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))
        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)
        # self.lineEdit_imie.setText("Jozef")

    def get_data(self):
        self.imie = self.lineEdit_imie.text()
        self.nazwisko = self.lineEdit_nazwisko.text()
        self.stanowisko = self.lineEdit_stanowisko.text()

    def insert_into_database(self):
        self.get_data()
        self.query = (
            f"INSERT INTO osoba (imie, nazwisko, stanowisko) "
            f"VALUES ('{self.imie}', '{self.nazwisko}', '{self.stanowisko}');"
        )
        self.db_handler.execute_query(self.query)

    def update_database(self, id: int):
        self.get_data()
        self.query = (
            f"UPDATE osoba SET "
            f"imie = '{self.imie}', "
            f"nazwisko = '{self.nazwisko}', "
            f"stanowisko = '{self.stanowisko}' "
            f"WHERE osoba_id = '{id}';"
        )
        self.db_handler.execute_query(self.query)

    # def insert_into_database(self):
    #     self.get_data()
    #     self.query = f"""INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES ('{self.imie}', '{self.nazwisko}', '{self.stanowisko}')"""
    #     self.db_handler.execute_query(self.query)

    # def update_database(self, id: int):
    #     self.get_data()
    #     self.query = f"""UPDATE osoba
    #         SET imie = '{self.imie}', nazwisko = '{self.nazwisko}', stanowisko = '{self.stanowisko}'
    #         WHERE osoba_id = '{id}';
    #         """
    #     self.db_handler.execute_query(self.query)

    # def insert_into_database(self):
    #     self.get_data()
    #     self.query = QSqlQuery()
    #     self.query.prepare(
    #         "INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES (?, ?, ?)"
    #     )
    #     self.query.addBindValue(self.imie)
    #     self.query.addBindValue(self.nazwisko)
    #     self.query.addBindValue(self.stanowisko)
    #     self.db_handler.execute_query(self.query)
    #     print(self.query.lastQuery())

    # def update_database(self, id: int):
    #     self.get_data()
    #     self.query = QSqlQuery()
    #     self.query.prepare(
    #         "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
    #     )
    #     self.query.addBindValue(self.imie)
    #     self.query.addBindValue(self.nazwisko)
    #     self.query.addBindValue(self.stanowisko)
    #     self.query.addBindValue(id)
    #     self.db_handler.execute_query(self.query)

    # def exec_query(self):
    #     self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_handler = DatabaseHandler()
    db_handler.create_connection()
    window = PersonDialog(db_handler)
    window.show()

    sys.exit(app.exec())


# import os
# import sys
# from PyQt6.QtWidgets import QDialog, QApplication
# from PyQt6.uic import loadUi
# from PyQt6.QtSql import QSqlQuery
# from PyQt6.QtGui import QIcon
# from Classes.DatabaseHandler import DatabaseHandler
# from dataclasses import dataclass


# # @dataclass(frozen=True, order=True)
# @dataclass(frozen=True, order=True)
# class Person:
#     imie: str = ""
#     nazwisko: str = ""
#     stanowisko: str = ""

#     def insert_into_database(self, db_handler: DatabaseHandler):
#         query = QSqlQuery()
#         query.prepare("INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES (?, ?, ?)")
#         query.addBindValue(self.imie)
#         query.addBindValue(self.nazwisko)
#         query.addBindValue(self.stanowisko)
#         db_handler.execute_query(query)

#     def update_database(self, db_handler: DatabaseHandler, person_id: int):
#         query = QSqlQuery()
#         query.prepare(
#             "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
#         )
#         query.addBindValue(self.imie)
#         query.addBindValue(self.nazwisko)
#         query.addBindValue(self.stanowisko)
#         query.addBindValue(person_id)
#         db_handler.execute_query(query)


# class PersonDialog(QDialog):
#     def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.db_handler = db_handler
#         self.init_gui()

#     def init_gui(self):
#         directory = os.path.dirname(os.path.abspath(__file__))
#         ui_file = os.path.join(directory, "GUI", "person_dialog.ui")
#         loadUi(ui_file, self)

#         self.setWindowTitle("Airport Management System")
#         self.setWindowIcon(QIcon("images/airport.png"))

#     def get_data(self):
#         self.person_data = Person(
#             self.lineEdit_imie.text(),
#             self.lineEdit_nazwisko.text(),
#             self.lineEdit_stanowisko.text(),
#         )


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     db_handler = DatabaseHandler()
#     db_handler.create_connection()
#     window = PersonDialog(db_handler)
#     window.show()
#     sys.exit(app.exec())

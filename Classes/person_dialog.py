from classes.database_handler import DatabaseHandler

from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QIcon
import sys, os


class PersonDialog(QDialog):
    def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.init_gui()

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        # print(directory)
        directory = os.path.join(directory, "..")
        # print(directory)
        ui_file = os.path.join(directory, "GUI", "person_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))
        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)
        # self.lineEdit_imie.setText("Jozef")

    def get_data(self):
        self.imie = self.lineEdit_imie.text()
        self.nazwisko = self.lineEdit_nazwisko.text()
        self.stanowisko = self.lineEdit_stanowisko.text()

    def insert_into_database(self):
        self.get_data()
        self.query = QSqlQuery()
        self.query.prepare(
            "INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES (?, ?, ?)"
        )
        self.query.addBindValue(self.imie)
        self.query.addBindValue(self.nazwisko)
        self.query.addBindValue(self.stanowisko)
        self.db_handler.execute_query(self.query)

        # print(self.query.lastQuery())
        # print(self.query.boundValues())
        # self.last_query = self.query.lastQuery()
        # self.bound_values = self.query.boundValues()
        # print(self.bound_values)
        # print(self.query)

    def update_database(self, id: int):
        self.get_data()
        self.query = QSqlQuery()
        self.query.prepare(
            "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
        )
        self.query.addBindValue(self.imie)
        self.query.addBindValue(self.nazwisko)
        self.query.addBindValue(self.stanowisko)
        self.query.addBindValue(id)
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_handler = DatabaseHandler()
    db_handler.create_connection()
    window = PersonDialog(db_handler)
    window.show()

    sys.exit(app.exec())

    # def insert_into_database(self):
    #     self.get_data()
    #     self.query = (
    #         f"INSERT INTO osoba (imie, nazwisko, stanowisko) "
    #         f"VALUES ('{self.imie}', '{self.nazwisko}', '{self.stanowisko}');"
    #     )
    #     self.db_handler.execute_query(self.query)

    # def update_database(self, id: int):
    #     self.get_data()
    #     self.query = (
    #         f"UPDATE osoba SET "
    #         f"imie = '{self.imie}', "
    #         f"nazwisko = '{self.nazwisko}', "
    #         f"stanowisko = '{self.stanowisko}' "
    #         f"WHERE osoba_id = '{id}';"
    #     )
    #     self.db_handler.execute_query(self.query)

    # def insert_into_database(self):
    #     self.get_data()
    #     self.query = QSqlQuery(None, self.db_handler.con)
    #     self.query.prepare(
    #         "INSERT INTO osoba (imie, nazwisko, stanowisko) "
    #         "VALUES (:imie, :nazwisko, :stanowisko)"
    #     )
    #     self.query.addBindValue(":imie", self.imie)
    #     self.query.addBindValue(":nazwisko", self.nazwisko)
    #     self.query.addBindValue("stanowisko", self.stanowisko)
    #     self.db_handler.execute_query(self.query)
    #     print(self.query.lastQuery())

    # def update_database(self, id: int):
    #     self.get_data()
    #     self.query = QSqlQuery()
    #     self.query.prepare(
    #         "UPDATE osoba SET "
    #         "imie = :imie, "
    #         "nazwisko = :nazwisko, "
    #         "stanowisko = :stanowisko "
    #         "WHERE osoba_id = :osoba_id"
    #     )
    #     self.query.addBindValue(":imie", self.imie)
    #     self.query.addBindValue(":nazwisko", self.nazwisko)
    #     self.query.addBindValue(":stanowisko", self.stanowisko)
    #     self.query.addBindValue("osoba_id", id)
    #     self.db_handler.execute_query(self.query)

from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QIcon
import sys, os


class PersonDialog(QDialog):
    def __init__(self, db_handler, row_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.row_id = row_id
        self.init_gui()
        if self.row_id:
            self.set_edit_values()

    def init_gui(self):
        # TODO - path management
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(directory, "..")
        ui_file = os.path.join(directory, "GUI", "person_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))
        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)

    def get_data(self):
        self.imie = self.lineEdit_imie.text()
        self.nazwisko = self.lineEdit_nazwisko.text()
        self.stanowisko = self.lineEdit_stanowisko.text()

    def insert_into_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
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

    def set_edit_values(self):
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "SELECT imie, nazwisko, stanowisko FROM osoba WHERE osoba_id = ?"
        )
        self.query.addBindValue(self.row_id)
        self.query.exec()
        self.query.next()
        self.lineEdit_imie.setText(self.query.value(0))
        self.lineEdit_nazwisko.setText(self.query.value(1))
        self.lineEdit_stanowisko.setText(self.query.value(2))

    def update_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
        )
        self.query.addBindValue(self.imie)
        self.query.addBindValue(self.nazwisko)
        self.query.addBindValue(self.stanowisko)
        self.query.addBindValue(self.row_id)
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    from run_test_dialog import RunTestDialog

    test_window = RunTestDialog(PersonDialog, row_id=6)

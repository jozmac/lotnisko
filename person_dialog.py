from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QIcon
import sys, os


class PersonDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, "GUI")
        os.chdir(gui_directory)
        loadUi("person_dialog.ui", self)
        os.chdir(directory)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))

        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)

    def get_data(self):
        self.imie = self.lineEdit_imie.text()
        self.nazwisko = self.lineEdit_nazwisko.text()
        self.stanowisko = self.lineEdit_stanowisko.text()

    def insert_to_database(self):
        self.get_data()
        query = QSqlQuery()
        query.prepare("INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES (?, ?, ?)")
        query.addBindValue(self.imie)
        query.addBindValue(self.nazwisko)
        query.addBindValue(self.stanowisko)
        if query.exec():
            print(f"Data inserted successfully.")
        else:
            print(f"Error inserting data: {query.lastError().text()}")

    # def get_selected_options(self):
    #     return [
    #         self.lineEdit_imie.text(),
    #         self.lineEdit_nazwisko.text(),
    #         self.lineEdit_stanowisko.text(),
    #     ]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonDialog()
    window.show()

    sys.exit(app.exec())

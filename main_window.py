from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys
import os

from functions import get_data, drop_tables, create_tables

# drop_tables()
# create_tables()
osoba, lotnisko, samolot = get_data()


# TODO:
# - widok tworzenia bazy danych postgres - schemat(tools - EDB tool)
# - sekwenje - ID - ticket_id
# - skasować niepotrzebne kolumny w lotniskach
# - zatrudnienie - 2 kolumny jako klucz główny
# - zamienić nazwę tabeli konto na osoba
# - import os
###################################################################
# - klucze obce - indeksy na kolumnę(drzewko postgresowe)
# - zakładki na tabele i sygnały klikania
# -
# - gui - biblioteka do ścieżek - import os
# - osobna klasa do ładowania danych(i otwoeranie bazy w klasie a nie na początku kodu)
# - SRP = single response principle - jedna klasa - jedna funkcja
# - osobne pliki dla wszystkich klas
# - dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxyb), data(kalendarz)
# - Wczytywanie listy dostępnych miejsc
# db.close()
# -
# - sprawdzenie błędu "QSqlDatabase: QPSQL driver not loaded" na ubuntu
# - na githuba


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # print(os.getcwd())
        # os.chdir('\PycharmProjects\lotnisko')
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("lotnisko1.ui", self)

        self.pushButton_pasazerowie.clicked.connect(lambda: self.load_data(osoba))
        self.pushButton_lotnisko.clicked.connect(lambda: self.load_data(lotnisko))
        self.pushButton_loty.clicked.connect(lambda: self.load_data(samolot))

        self.tableWidget.cellClicked.connect(self.get_clicked_cell)

    def load_data(self, table_name):
        self.table_name = table_name
        self.tableWidget.setRowCount(len(table_name))
        self.tableWidget.setColumnCount(len(table_name[0]))
        for row_number, row_data in enumerate(table_name):
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column, QTableWidgetItem(str(data)))
        # self.tableWidget.setHorizontalHeaderLabels(["id", "model", "ilosc_miejsc"])


    def get_clicked_cell(self, row, column):
        print(f"Clicked cell: [{row}, {column}]")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

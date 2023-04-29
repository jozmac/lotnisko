from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys
import os
from functions import get_data, drop_tables, create_tables


# # Temat projektu
# System zarządzania lotami

# # Ogólne wymagania względem aplikacji
# -	Aplikacja musi spełniać wymagania funkcjonalne
# -	Aplikacja musi posiadać intuicyjny intefejs graficzny
# -	Aplikacja musi współpracować z bazą danych zaprojektowaną w modelu relacyjnym

# # Wymagania funkcjonalne
# - Dodaj/Edytuj/Usuń pasażera
# - Dodaj/Edytuj/Usuń pracownika wraz z jego funkcją
# - Rezerwacja biletu dla pasażera
# - Zmiana klasy miejsca w samolocie
# - W samolocie dostępne są dwie klasy: ekonomiczna oraz biznesowa.
#     Od rodzaju klasy zależy ilość miejsc,
#     cena oraz dostępność dodatkowych usług.
# - Pracownicy są z góry przypisani do danego lotu.
# - Do samolotu wsiadają pasażerowie. Pasażer może wybrać określony lot.
#     Każdy pasażer musi zostać zarejestrowany do konkretnego lotu
#     przy użyciu systemu automatycznej rejestracji pasażerów samolotu.
# - System automatycznej rejestracji pasażerów samolotu umożliwia:
#     - rejestrację pasażera do lotu,
#     - weryfikację wprowadzonych danych,
#     - zmianę miejsca w samolocie,
#     - zmianę klasy lotu,
#     - drukowanie karty pokładowej,
#     - zamówienie pomocy asystenta,
#     - sprawdzenie informacji o bramce odlotu,
#     - sprawdzenie parametrów lotu.


# DONE:
# widok tworzenia bazy danych postgres - schemat(tools - EDB tool)
# sekwenje - ticket_id, osoba_id
# skasować niepotrzebne kolumny w lotniskach (ładowanie danych jest )
# zatrudnienie - 2 kolumny jako klucz główny
# zamienić nazwę tabeli konto na osoba
# import os
# na githuba
# TODO:
# klucze obce - indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
# zakładki na tabele i sygnały klikania
# 
# SRP = single response principle - jedna klasa - jedna funkcja
# Wczytywanie listy dostępnych miejsc
# dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxy), data(kalendarz)
# rozdzielić klasy do osobnych plików - (main_window, klasy, dialog_window, db_connection (otwoeranie bazy w klasie a nie na początku kodu))
# db.close()
# 
# sprawdzenie błędu "QSqlDatabase: QPSQL driver not loaded" na ubuntu


# drop_tables()
# create_tables()
osoba, lotnisko, samolot = get_data()

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

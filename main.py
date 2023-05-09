from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys, os
from functions import get_data, drop_tables, create_tables, select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
from PyQt6 import QtGui
from booking_dialog import Booking_dialog
import psycopg2 as pg2

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
# zakładki na tabele i sygnały klikania
# dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxy), data(kalendarz)
# TODO:
# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
# pytest
#
# rozdzielić klasy do osobnych plików - (main_window, klasy, dialog_window, db_connection (otwoeranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# Wczytywanie listy dostępnych miejsc
# db.close()
#
# sprawdzenie błędu "QSqlDatabase: QPSQL driver not loaded" na ubuntu

# Pytania:
# - sposób ładowania danych
# - comboboxy
# - nazwy kolumn
# - QSQL
# - @dataclass
# - testy
# - miejsce / siedzenia


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("main_window_v2.ui", self)

        self.tabWidget.setMovable(True)
        # self.tabWidget.setTabsClosable(True)

        self.tabWidget.setTabText(0, "Osoba")
        self.tabWidget.setTabText(1, "Bilet")
        self.tabWidget.setTabText(2, "Zatrudnienie")
        self.tabWidget.setTabText(3, "Lot")
        self.tabWidget.setTabText(4, "Samolot")
        self.tabWidget.setTabText(5, "Miejsce")
        self.tabWidget.setTabText(6, "Zajete_miejsce")
        self.tabWidget.setTabText(7, "Lotnisko")
        self.tabWidget.setTabText(8, "Pracownik")

        # self.tabWidget.addTab(QWidget(), "New Tab")
        # self.tabWidget.removeTab(8)
        
        self.tabWidget.tabBarClicked.connect(self.tabChanged)

        # Default table
        self.load_data(self.tableWidget_0, select_osoba())

        # if self.index == 1:
        #     self.pushButton_add.clicked.connected(self.bilet)

        self.pushButton_dodaj_1.clicked.connect(self.rezerwuj_bilet)

        

    def load_data(self, tab, data):
        if not len(data):
            return False
        tab.setRowCount(len(data))
        tab.setColumnCount(len(data[0]))
        for row_number, row_data in enumerate(data):
            for column, data in enumerate(row_data):
                tab.setItem(row_number, column, QTableWidgetItem(str(data)))
        # self.tableWidget.setHorizontalHeaderLabels(["id", "model", "ilosc_miejsc"])
        tab.cellClicked.connect(self.get_clicked_cell)


    def get_clicked_cell(self, row, column):
        print(f"Clicked cell: [{row}, {column}]")
        
    # def tabChanged(self):
    #     index = self.tabWidget.currentIndex()
    #     print(index)

    def tabChanged(self, index):
        self.index = index
        print(f"Selected tab: {index} - {self.tabWidget.tabText(index).lower()}")

        self.load_data(eval(f"self.tableWidget_{index}"), eval(f"select_{self.tabWidget.tabText(index).lower()}()"))

        # if index == 0:
        #     self.load_data(self.tableWidget_0, select_osoba())
        # elif index == 1:
        #     self.load_data(self.tableWidget_1, select_bilet())
        # elif index == 2:
        #     self.load_data(self.tableWidget_2, select_zatrudnienie())
        # elif index == 3:
        #     self.load_data(self.tableWidget_3, select_lot())
        # elif index == 4:
        #     self.load_data(self.tableWidget_4, select_samolot())
        # elif index == 5:
        #     self.load_data(self.tableWidget_5, select_miejsce())
        # elif index == 6:
        #     self.load_data(self.tableWidget_6, select_zajete_miejsce())
        # elif index == 7:
        #     self.load_data(self.tableWidget_7, select_lotnisko())


    def rezerwuj_bilet(self):
        window = Booking_dialog()
        if window.exec():
            # osoba, z, do, klasa, seat, asystent = self.get_selected_options()
            combo1, combo2, combo3, combo4, combo5, combo6, date, time = window.get_selected_options()
            print(f"Selected options:, {combo1}, {combo2}, {combo3}, {combo4}, {combo5}, {combo6}, {date}, {time}")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # if not createConnection("contacts.sqlite"):
    #     sys.exit(1)

    try:
        db = pg2.connect(
            database="lotnisko",
            host="localhost",
            user='postgres',
            password='password',
            port='5432'
        )
        print(db)
        cur = db.cursor()
    except pg2.Error as e:
        # self.label_result.setText("Error")
        print(e)
        sys.exit(1)

    # drop_tables()
    # create_tables()
    # osoba, lotnisko, samolot = get_data()

    window = Window()
    window.show()
    # db.close()
    sys.exit(app.exec())


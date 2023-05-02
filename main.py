from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys, os
from functions import get_data, drop_tables, create_tables
from PyQt6 import QtGui


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
# TODO:
# dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxy), data(kalendarz)
# klucze obce - indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
#
# SRP = single response principle - jedna klasa - jedna funkcja
# rozdzielić klasy do osobnych plików - (main_window, klasy, dialog_window, db_connection (otwoeranie bazy w klasie a nie na początku kodu))
# Wczytywanie listy dostępnych miejsc
# db.close()
#
# sprawdzenie błędu "QSqlDatabase: QPSQL driver not loaded" na ubuntu
# Pytania:
# - sposób ładowania danych - lista tabel?
# - nazwy kolumn
# - 


# drop_tables()
# create_tables()



class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("main_window.ui", self)

        self.tabWidget.setMovable(True)
        # self.tabWidget.setTabsClosable(True)

        self.tabWidget.setTabText(0, "Osoba")
        self.tabWidget.setTabText(1, "Lotnisko")
        self.tabWidget.setTabText(2, "Samolot")

        # self.tabWidget.addTab(QWidget(), "New Tab")
        # self.tabWidget.removeTab(0)
        
        self.tabWidget.tabBarClicked.connect(self.tabChanged)

        # Default table
        self.load_data(self.tableWidget_0, osoba)

        


    def load_data(self, tab, data):
        tab.setRowCount(len(data))
        tab.setColumnCount(len(data[0]))
        for row_number, row_data in enumerate(data):
            for column, data in enumerate(row_data):
                tab.setItem(row_number, column, QTableWidgetItem(str(data)))
        # self.tableWidget.setHorizontalHeaderLabels(["id", "model", "ilosc_miejsc"])
        tab.cellClicked.connect(self.get_clicked_cell)


    def get_clicked_cell(self, row, column):
        print(f"Clicked cell: [{row}, {column}]")
        

    def tabChanged(self, index):
        print(index)

        # table_widget = [self.tableWidget_0,
        #                 self.tableWidget_1,
        #                 self.tableWidget_2,
        #                 self.tableWidget_3,
        #                 self.tableWidget_4,
        #                 self.tableWidget_5,
        #                 self.tableWidget_6,
        #                 self.tableWidget_7,
        #                 self.tableWidget_8]

        # self.load_data(table_widget[index], index)

        if index == 0:
            self.load_data(self.tableWidget_0, osoba)
        elif index == 1:
            self.load_data(self.tableWidget_1, lotnisko)
        elif index == 2:
            self.load_data(self.tableWidget_2, samolot)
        elif index == 3:
            self.load_data(self.tableWidget_3, osoba)
        elif index == 4:
            self.load_data(self.tableWidget_4, osoba)
        elif index == 5:
            self.load_data(self.tableWidget_5, osoba)


    # def tabChanged(self, index):
    #     print(index)
    #     # print(self.tabWidget.currentIndex())
    #     # page = self.tabWidget.widget(1)
    #     # table_widget = page.findChild(QTableWidget)
    #     # table_widget = page.findChild(self.tabWidget)
    #     # self.current_table = self.tabWidget.widget(index)
    #     # print(self.current_table)
    #     # self.current_table.setRowCount(3)
    #     # self.current_table.setColumnCount(3)

    # def tabChanged(self):
    #     index = self.tabWidget.currentIndex()
    #     print(index)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # if not createConnection("contacts.sqlite"):
    #     sys.exit(1)
    osoba, lotnisko, samolot = get_data()


    window = Window()
    window.show()
    sys.exit(app.exec())
    # db.close()

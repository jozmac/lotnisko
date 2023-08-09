from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys, os
from functions import get_data, drop_tables, create_tables, select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
from PyQt6 import QtGui
from booking_dialog import Booking_dialog
from flight_dialog import Flight_dialog
import psycopg2 as pg2

DB_CONFIG = {
    "database": "lotnisko",
    "host": "localhost",
    "user": "postgres",
    "password": "password",
    "port": "5432"
}

SELECT_FUNCTIONS = {
    "osoba": select_osoba,
    "lotnisko": select_lotnisko,
    "samolot": select_samolot,
    "bilet": select_bilet,
    "lot" : select_lot,
    "miejsce" : select_miejsce,
    "zajete_miejsce" : select_zajete_miejsce,
    "zatrudnienie" : select_zatrudnienie,
    "pracownik" : select_pracownik
}

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
# sekwenje - ticket_id, osoba_id - nextval('osoba_id_seq'::regclass)
# skasować niepotrzebne kolumny w lotniskach (ładowanie danych jest )
# zatrudnienie - 2 kolumny jako klucz główny
# zamienić nazwę tabeli konto na osoba
# import os
# zakładki na tabele i sygnały klikania
# dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxy), data(kalendarz)
# skrypt do stworzenia miejsc w samolotach
# usunąć wybór daty z biletów, dialog dodawania lotów QDateEdit
# getarrt() zamiast eval()
# Flight_dialog()
# db.close()
# TODO:
# comboboxy - jak załadować dane, czytanie id wybranej opcji po kliknięciu ok - słowniki (dict)
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów - czy fstring jest taki sam jak query
# usunąć tabele zatrudnienie, miejsca, lotnisko, miejsce, zajęte miejsce z głównego okna
# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwoeranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# Wczytywanie listy dostępnych miejsc
# dodać tytuły i ikony do okien
# cashowanie tabeli lotów
# sprawdzenie błędu "QSqlDatabase: QPSQL driver not loaded" na ubuntu


# QItemDelegate - tabele, comboboxy - select id
# py
# class AreaItemDelegate(QItemDelegate):
#     def paint(self, painter, option, index):
#         styleOption = QStyleOptionViewItem(option)
#         try:
#             value = index.data(Qt.DisplayRole)
#         except AttributeError:
#             value = ''
#         if value not in [None, NULL, 'NULL', '']:
#             wartosc = str(value)
#             styleOption.text = wartosc.replace('.', ',')
#             styleOption.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
#             if styleOption.state & QStyle.State_Selected:
#                 styleOption.state |= QStyle.State_Active
#             self.parent().style().drawControl(QStyle.CE_ItemViewItem,
#                                               styleOption, painter)


# Pytania:
# - 


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_gui()

        # # self.tabWidget.setMovable(True)
        # # self.tabWidget.setTabsClosable(True)

        # # self.tabWidget.addTab(QWidget(), "New Tab")
        # # self.tabWidget.removeTab(8)


    def init_gui(self):
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        # os.chdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]))), 'GUI')
        loadUi("main_window.ui", self)

        tab_labels = [
            "Osoba", "Bilet", "Zatrudnienie", "Lot", "Samolot",
            "Miejsce", "Zajete_miejsce", "Lotnisko", "Pracownik"
        ]
        for index, label in enumerate(tab_labels):
            self.tabWidget.setTabText(index, label)
        
        self.tabWidget.tabBarClicked.connect(self.tab_changed)
        # default tab
        self.load_data(self.tableWidget_0, select_osoba())
        self.tab_changed(1)

        self.pushButton_dodaj_1.clicked.connect(self.rezerwuj_bilet)
        self.pushButton_dodaj_3.clicked.connect(self.dodaj_lot)
        self.pushButton_usun_1.clicked.connect(self.usun_bilet)
        self.pushButton_usun_3.clicked.connect(self.usun_lot)


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
        # self.tab_changed(self.index)


    def get_clicked_cell(self, row, column):
        print(f"Clicked cell: [{row}, {column}]")
        return row, column


    def get_row_id(self):
        # row, column = tab.cellClicked.connect(self.get_clicked_cell)
        # selected_row = self.tableWidget_1.currentRow()
        # print(f"Clicked cell: [{row}, {column}]")
        item = self.tableWidget_1.item(row, 0)
        print(row)
        return item
        

    def tab_changed(self, index):
        self.index = index
        tab_name = self.tabWidget.tabText(index).lower()
        print(f"Selected tab: {index} - {tab_name}")

        table_widget_attr = getattr(self, f"tableWidget_{index}", None)
        select_function = SELECT_FUNCTIONS.get(tab_name)

        if table_widget_attr and select_function:
            self.load_data(table_widget_attr, select_function())


    def return_id(self, string):
        self.split_string = string.replace("(", "").replace(")", "").replace(" ", "").split(",")
        return self.split_string[0]


    def dodaj_lot(self):
        window = Flight_dialog()
        if window.exec():
            samolot, lotnisko_a, lotnisko_b, datetime = window.get_selected_options()
            print(f"Selected options:, {samolot}, {lotnisko_a}, {lotnisko_b}, {datetime}")
            
            samolot_id = self.return_id(samolot)
            lotnisko_a_id = self.return_id(lotnisko_a)
            lotnisko_b_id = self.return_id(lotnisko_b)
            

            try:
                with pg2.connect(**DB_CONFIG) as db:
                    cur = db.cursor()
                    cur.execute("INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) VALUES (%s, %s, %s, %s)",
                                (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime))
                    db.commit()
                    print("Flight added to the database.")
            except pg2.Error as e:
                print("Error while adding flight: ", e)

            self.tab_changed(self.index)


    def usun_lot(self):
        # self.get_row_id()
        # try:
        #     with pg2.connect(**DB_CONFIG) as db:
        #         cur = db.cursor()
        #         lot_id = self.tableWidget_1.item(row_number, 0).text()  # Assuming the first column is the bilet_id
        #         cur.execute("DELETE FROM lot WHERE lot_id = %s", (lot_id,))
        #         db.commit()
        #         print("Flight deleted from the database.")
        # except pg2.Error as e:
        #     print("Error while deleting flight:", e)

        self.tab_changed(self.index)

    def usun_bilet(self):
        # self.get_row_id()
        # try:
        #     with pg2.connect(**DB_CONFIG) as db:
        #         cur = db.cursor()
        #         lot_id = self.tableWidget_1.item(row_number, 0).text()  # Assuming the first column is the bilet_id
        #         cur.execute("DELETE FROM lot WHERE lot_id = %s", (lot_id,))
        #         db.commit()
        #         print("Flight deleted from the database.")
        # except pg2.Error as e:
        #     print("Error while deleting flight:", e)

        self.tab_changed(self.index)


    def rezerwuj_bilet(self):
        window = Booking_dialog()
        if window.exec():
            osoba, lot, klasa, miejsce, asystent = window.get_selected_options()
            # selected_options = window.get_selected_options()
            # osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina = selected_options
            print(f"Selected options:, {osoba}, {lot}, {klasa}, {miejsce}, {asystent}")
            
            osoba_id = self.return_id(osoba)
            lot_id = self.return_id(lot)
            miejsce_id = self.return_id(miejsce)

            try:
                with pg2.connect(**DB_CONFIG) as db:
                    cur = db.cursor()
                    cur.execute("INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) VALUES (%s, %s, %s, %s, %s)",
                                (osoba_id, lot_id, klasa, miejsce_id, asystent))
                    db.commit()
                    print("Ticket added to the database.")
            except pg2.Error as e:
                print("Error while adding ticket:", e)
            
            self.tab_changed(self.index)



def run_app():
    app = QApplication(sys.argv)

    try:
        with pg2.connect(**DB_CONFIG) as db:
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
    db.close()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

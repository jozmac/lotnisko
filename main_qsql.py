from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
import sys, os
from functions import get_data, drop_tables, create_tables, select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
from PyQt6 import QtGui
from booking_dialog import Booking_dialog
from flight_dialog import Flight_dialog
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
# sekwenje - ticket_id, osoba_id - nextval('osoba_id_seq'::regclass)
# skasować niepotrzebne kolumny w lotniskach (ładowanie danych jest )
# zatrudnienie - 2 kolumny jako klucz główny
# zamienić nazwę tabeli konto na osoba
# import os
# zakładki na tabele i sygnały klikania
# błąd "QSqlDatabase: QPSQL driver not loaded"

# dialog zamawiania biletu - skąd, dokąd, samolot, lotnisko(combo boxy), data(kalendarz)
# miejsca w samolotach
# usunąć wybór daty z biletów, dialog dodawania lotów QDateEdit
# getarrt() zamiast eval()
# Flight_dialog()
# db.close()

# TODO:
# dokończyć model/view
# comboboxy - jak załadować dane, czytanie id wybranej opcji po kliknięciu ok - słowniki (dict)
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów - czy fstring jest taki sam jak query
# usunąć tabele zatrudnienie, miejsca, lotnisko, miejsce, zajęte miejsce z głównego okna

# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwoeranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# Wczytywanie listy dostępnych miejsc
# dodać tytuły i ikony do okien
# cashowanie tabeli lotów


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

def create_connection():
    try:
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("localhost")
        db.setDatabaseName("lotnisko")
        db.setUserName("postgres")
        db.setPassword("password")
        db.setPort(5432)

        if not db.open():
            raise ConnectionError(f"Could not open database. Error: {db.lastError().text()}")
        return db
    except Exception as e:
        raise ConnectionError(f"Connection error: {e}")


# widget dict
    # self.tables = {
    #     0: self.tableView_0,
    #     1: self.tableView_1,
    #     2: self.tableView_2,
    #     3: self.tableView_3,
    #     4: self.tableView_4,
    #     5: self.tableView_5,
    #     6: self.tableView_6,
    #     7: self.tableView_7,
    #     8: self.tableView_8
    # }


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.init_gui()
        # self.db = self.create_connection()

        # get_widget_dict = 
    
    # def create_connection(self):
    #     try:
    #         db = QSqlDatabase.addDatabase("QPSQL")
    #         db.setHostName("localhost")
    #         db.setDatabaseName("lotnisko")
    #         db.setUserName("postgres")
    #         db.setPassword("password")
    #         db.setPort(5432)

    #         if not db.open():
    #             raise ConnectionError(f"Could not open database. Error: {db.lastError().text()}")
    #         return db
    #     except Exception as e:
    #         raise ConnectionError(f"Connection error: {e}")

    def init_gui(self):
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        # os.chdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]))), 'GUI')
        loadUi("main_window_tableview.ui", self)

        # Rename tabs
        tab_labels = [
            "Osoba", "Bilet", "Lot", "Samolot", "Miejsce", 
            "Zajete_miejsce", "Lotnisko", "Pracownik", "Zatrudnienie"]
        for index, label in enumerate(tab_labels):
            self.tabWidget.setTabText(index, label)
        

        self.tabWidget.tabBarClicked.connect(self.tab_changed)

        self.pushButton_dodaj_1.clicked.connect(self.dodaj_bilet)
        self.pushButton_dodaj_3.clicked.connect(self.dodaj_lot)
        self.pushButton_usun_1.clicked.connect(self.usun_bilet)
        self.pushButton_usun_3.clicked.connect(self.usun_lot)

        # set default tab
        self.tabWidget.setCurrentIndex(0)
        self.load_osoba()

        # # self.tabWidget.setMovable(True)
        # # self.tabWidget.setTabsClosable(True)



    def load_data(self, query):
        db = create_connection()
        if not db:
            return
        model = QSqlTableModel()
        model.setQuery(query, db)
        # db.close()
        # print(f"database open: {db.isOpen()}")
        return model

    def load_osoba(self):
        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        model = self.load_data(query)
        self.tableView_0.setModel(model)
        # for idx, name in enumerate(headerNames):
        #     model.setHeaderData(idx, Qt.Horizontal, name)
        while model.canFetchMore():
            model.fetchMore()
        self.tableView_0.resizeColumnsToContents()
        # self.db.close()

    def load_bilet(self):
        query = "SELECT bilet_id, osoba_id, lot_id, miejsce_id, asystent FROM bilet"
        model = self.load_data(query)
        self.tableView_1.setModel(model)

    def load_lot(self):
        query = "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        model = self.load_data(query)
        self.tableView_2.setModel(model)

    def tab_changed(self, index):
        self.index = index

        if index == 0:
            # current_table = tableView_0
            self.load_osoba()
        elif index == 1:
            self.load_bilet()
        elif index == 2:
            self.load_lot()

        # def addRecord():
        #     model.insertRow(model.rowCount())
        #     view.scrollToBottom()

        # def delRecord():
        #     model.deleteRowFromTable(view.currentIndex().row())
        #     model.select()




    # def dodaj_lot(self):
    #     window = Flight_dialog()
    #     if window.exec():
    #         samolot, lotnisko_a, lotnisko_b, datetime = window.get_selected_options()
    #         print(f"Selected options:, {samolot}, {lotnisko_a}, {lotnisko_b}, {datetime}")
            
    #         samolot_id = self.return_id(samolot)
    #         lotnisko_a_id = self.return_id(lotnisko_a)
    #         lotnisko_b_id = self.return_id(lotnisko_b)
            
            
    #         try:
    #             # execute_query(query)
    #             with pg2.connect(**DB_CONFIG) as db:
    #                 cur = db.cursor()
    #                 cur.execute("INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) VALUES (%s, %s, %s, %s)",
    #                             (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime))
    #                 db.commit()
    #                 print("Flight added to the database.")
    #         except pg2.Error as e:
    #             print("Error while adding flight: ", e)

    #         # model.setheaderdata()

    #         self.tab_changed(self.index)


    # def usun_lot(self):
    #     # self.get_row_id()
    #     # try:
    #     #     with pg2.connect(**DB_CONFIG) as db:
    #     #         cur = db.cursor()
    #     #         lot_id = self.tableWidget_1.item(row_number, 0).text()  # Assuming the first column is the bilet_id
    #     #         cur.execute("DELETE FROM lot WHERE lot_id = %s", (lot_id,))
    #     #         db.commit()
    #     #         print("Flight deleted from the database.")
    #     # except pg2.Error as e:
    #     #     print("Error while deleting flight:", e)

    #     self.tab_changed(self.index)

    # def usun_bilet(self):
    #     # self.get_row_id()
    #     # try:
    #     #     with pg2.connect(**DB_CONFIG) as db:
    #     #         cur = db.cursor()
    #     #         lot_id = self.tableWidget_1.item(row_number, 0).text()  # Assuming the first column is the bilet_id
    #     #         cur.execute("DELETE FROM lot WHERE lot_id = %s", (lot_id,))
    #     #         db.commit()
    #     #         print("Flight deleted from the database.")
    #     # except pg2.Error as e:
    #     #     print("Error while deleting flight:", e)

    #     self.tab_changed(self.index)


    # def dodaj_bilet(self):
    #     window = Booking_dialog()
    #     if window.exec():
    #         osoba, lot, klasa, miejsce, asystent = window.get_selected_options()
    #         # selected_options = window.get_selected_options()
    #         # osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina = selected_options
    #         print(f"Selected options:, {osoba}, {lot}, {klasa}, {miejsce}, {asystent}")
            
    #         osoba_id = self.return_id(osoba)
    #         lot_id = self.return_id(lot)
    #         miejsce_id = self.return_id(miejsce)

    #         try:
    #             with pg2.connect(**DB_CONFIG) as db:
    #                 cur = db.cursor()
    #                 cur.execute("INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) VALUES (%s, %s, %s, %s, %s)",
    #                             (osoba_id, lot_id, klasa, miejsce_id, asystent))
    #                 db.commit()
    #                 print("Ticket added to the database.")
    #         except pg2.Error as e:
    #             print("Error while adding ticket:", e)
            
    #         self.tab_changed(self.index)



def run_app():
    app = QApplication(sys.argv)

    # drop_tables()
    # create_tables()
    # osoba, lotnisko, samolot = get_data()

    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUiType
import sys, os

from classes.osoba_tab import OsobaTab
from classes.bilet_tab import BiletTab
from classes.lot_tab import LotTab
from classes.database_handler import DatabaseHandler

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
# FlightDialog()
# model/view
# comboboxy - jak załadować dane, czytanie id wybranej opcji po kliknięciu ok - słowniki (dict)
# personDialog
# db.close()
# edytowanie komórki po kliknięciu edytuj
# drukowanie karty pokładowej
# black formatter
# rollback -czy napewno chcesz zatwierdzić zmiany?
# cena biletu
# usunąć tabele zatrudnienie, miejsca, lotnisko, miejsce, zajęte miejsce z głównego okna
# Zmienić nazwy przycisków w pliku .ui
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwieranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# dodać tytuły i ikony do okien
# wyświetlanie i edycja id
# zaznaczanie pojedyńczego wiersza tabeli
# get_data zamiast get_selected_opitons
# join zamiast tabledelegate
# napisać query dla dodawania, usuwania i edycji (self.model.deleteRowFromTable nie działa dla QSqlQueryModel)
# linter
# funkcja sprawdzania indesku zaznaczonego wiersza
# QSqlModelQuery
# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie) - które tabele powinny być indeksowane - tylko lotnisko?
# initializeDatabase
# indexy osobno na kolumnę
# poprawne formatowanie zapytań SQL - https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting
# .addBindValue -> f-string
# ładuj jedynie dostępne miejsca z danego samolotu do comboboxa
# wydzenenie funkcji execute_query - DatabaseHandler
# Klasa Tab i klasy OsobaTab, BiletTab i LotTab
# 1 plik 1 klasa
# fast return
# QSqlQuery bindvalue
# combobox nie zwraca indexu modelu zaznaczonej opcji - jedynie int
# ładowanie danych do dialogu edycji, zmiana miejsca w samolocie
# organizacja folderu, RunDialog
# error - błędna nazwa tabeli w zapytaniu: (42601) QPSQL: Unable to create query
# Poprawne pobieranie dostępnych miejsc
# Filtrowanie lotnisk QSortFilterProxyModel
# - jak zaimportować dane do wolumenu -
# docker-compose.yml - baza danych postgres w kontenerze + dane w wolumenie
# loadUiType zamiast loadUi
# booking_dialog miejsce query - podzapytania - zamienić na WITH - https://www.postgresql.org/docs/current/queries-with.html
# lepsze wyświetlanie miejsc w samolocie (np. 14A) - QItemDelegate pozwala na jedynie zmianę tekstu wyświetlanego w wyskakującej liście
# QCompleter
# poprawne ładowanie comboboxów do edycji FlightDialog (opcje nie są wybierane poprawnie po użyciu QSortFilterProxyModel) - zmienione na QLineEdit
# Comboboxy w FlightDialog nie wyświetlają listy opcji - jedynie aktualnie wybraną. Można zmieniać scrollem (w przypadku QSortFilterProxyModel) - zmienione na QLineEdit
# self as parent
# poprawne ładowanie lineeditów do edycji FlightDialog
# sockety/fastAPI/flask/django - client/server - napisać prosty backend - client PyQt wysyła zapytanie serwera Flask
# remove flightDialog comboboxes
# pytest - QSqlQuery nie buduje zapytania w przypadku zmockowanego db_handlera
# pytest - sprawdzenie wartości w oknie edycji

# pytest - module paths - użycie zakładki do testowania w VSCode
# pytest - testy okna głównego i dialogu osoby
# kolumna z nazwami miejsc w bazie danych zamiast metody dodającej kolumnę w modelu
# nazwy kolumn - AS zamiast funkcji z Qt
# get_data bug - QSqlQueryModel(None)
# testowanie zapytań sql - Datagrip, DBeaver, pycharm
# hashowanie - dane osoba haslo - dodać kolumnę
# weryfikacja hasła przy przed drukowaniem biletu - password_dialog
# widget.setFocus()
# fake_database sqlite


# TODO:
# delete comments
# split get_data_from_column_ functions for testing
# model test display TableView

# Pytania:
# prawidłowe podświetlanie funkcji w przypadku używania dictów lub plików ui (patrz self.tab[index].load_data() lub self.comboBox_person.setModel(self._select_osoba()))
# _ przed nazwą metody (patrz _init_ui())
# jak konwertować PG na Sqlite
# database_handler - osobny dla pg i sqlite?
# czy with _ as _: jest przydatne w przypadku używania sqlite
# czy powinno się przechowywać salt w bazie danych, a jeśli tak to dlaczego ALTER TABLE osoba DROP COLUMN salt;

# Pomysły:
# klasa do debugowanie kodu - wyświetlanie pojedyńczych obiektów / tabeli z modelami w czasie wykonywania kodu


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

# OSOBA_TAB_INDEX = 0
# BILET_TAB_INDEX = 1
# LOT_TAB_INDEX = 2
OSOBA_TAB_INDEX, BILET_TAB_INDEX, LOT_TAB_INDEX = range(3)
TAB_LABELS = ["Osoba", "Bilet", "Lot"]

UI_PATH = os.path.join(os.path.dirname(__file__), "GUI", "main.ui")
FORM_CLASS, BASE_CLASS = loadUiType(UI_PATH)


class MainWindow(QWidget, FORM_CLASS):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__()
        self.db_handler = db_handler
        if not self.db_handler.con:
            return
        self._init_ui()

    def _init_ui(self):
        self.setupUi(self)
        self._set_tab_labels()
        self.setGeometry(500, 300, 900, 700)
        # self.setWindowIcon(QIcon(os.path.join(UI_PATH, "airport.png")))
        self.setWindowIcon(QIcon("GUI/airport.png"))
        self.setWindowTitle("Airport Management System")
        self._init_tabs()
        self._connect_signals()
        self.tab = {
            OSOBA_TAB_INDEX: self.osoba_tab,
            BILET_TAB_INDEX: self.bilet_tab,
            LOT_TAB_INDEX: self.lot_tab,
        }

    def _set_tab_labels(self):
        for index, label in enumerate(TAB_LABELS):
            self.tabWidget.setTabText(index, label)

    def _init_tabs(self):
        self.osoba_tab = OsobaTab(self.db_handler, self.tableView_osoba)
        self.bilet_tab = BiletTab(self.db_handler, self.tableView_bilet)
        self.lot_tab = LotTab(self.db_handler, self.tableView_lot)
        self.tabWidget.setCurrentIndex(BILET_TAB_INDEX)
        self.bilet_tab.load_data()
        self.tabWidget.setMovable(True)

    def _connect_signals(self):
        self.tabWidget.currentChanged.connect(self.tabChanged)
        button_dict = {
            self.pushButton_dodaj_osoba: self.osoba_tab.add_row,
            self.pushButton_dodaj_bilet: self.bilet_tab.add_row,
            self.pushButton_dodaj_lot: self.lot_tab.add_row,
            self.pushButton_usun_osoba: self.osoba_tab.delete_row,
            self.pushButton_usun_bilet: self.bilet_tab.delete_row,
            self.pushButton_usun_lot: self.lot_tab.delete_row,
            self.pushButton_edytuj_osoba: self.osoba_tab.edit_row,
            self.pushButton_edytuj_bilet: self.bilet_tab.edit_row,
            self.pushButton_edytuj_lot: self.lot_tab.edit_row,
            self.pushButton_info_osoba: self.osoba_tab.info_row,
            self.pushButton_info_bilet: self.bilet_tab.info_row,
            self.pushButton_info_lot: self.lot_tab.info_row,
        }
        for button, callback in button_dict.items():
            button.clicked.connect(callback)

    def tabChanged(self, index: int):
        self.index = index
        self.tab[index].load_data()

    def closeEvent(self, event):
        self.db_handler.close_connection()


def run_app():
    app = QApplication(sys.argv)
    # app.setStyle("Basic")
    # app.setStyle("Material") # Android
    # app.setStyle("iOS")
    # app.setStyle("Fusion")  # Linux
    # app.setStyle("macOS")
    # app.setStyle("Windows")

    db_handler = DatabaseHandler()
    # db_handler = DatabaseHandler(port=5435)  # Docker database
    # db_handler = DatabaseHandler("data/lotnisko.sqlite3")
    db_handler.create_connection()
    # db_handler.create_connection_sqlite()
    window = MainWindow(db_handler)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # from config import BASE_DIR, UI_FILE
    # print(UI_FILE)
    # print(BASE_DIR)
    run_app()

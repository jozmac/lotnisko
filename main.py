from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QTableWidgetItem,
    QTableView,
    QMessageBox,
    QDialog,
    QAbstractItemView,
)

# from PyQt6.QtSql import (
#     QSqlDatabase,
#     QSqlQueryModel,
#     QSqlTableModel,
#     QSqlRelationalTableModel,
#     QSqlRelation,
#     QSqlRelationalDelegate,
#     QSqlQuery,
# )
from PyQt6.uic import loadUi, loadUiType
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QDateTime, QModelIndex

# from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QPainter, QColor, QTextDocument, QIcon, QFont
import sys, os

# from dialogs.booking_dialog import BookingDialog
# from dialogs.flight_dialog import FlightDialog
# from dialogs.person_dialog import PersonDialog

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
# Klasa Tab i klasy OsobaTab, BiletTab i LotTab (Klasa Tab dziedziczy po QWidget żeby QMessageBox działały poprawnie)


# TODO:
# ładowanie danych do dialogu edycji, zmiana miejsca w samolocie
# lepsze wyświetlanie miejsc w samolocie (np. 14A)
# 1 plik 1 klasa
# QSqlQuery bindvalue
# fast return
# mockowanie dialogu
#
# pytest - przypadki brzegowe, sprawdzanie errorów przy wpisywaniu "drop table" lub niepoprawnego formatu danych
# docker compose - baza danych postgres w kontenerze + dane w wolumenie
# API - client-server -
# hashowanie


# Pytania:
# - czasami testy uruchamiają wcześniejszą wersję klasy (sprzed zapisania pliku)
# - query.exec() zwraca False mimo poprawnego wykonania zapytania (person_dialog)
# - organizacja folderu projektu
# - docker + postgres
# -


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

# FORM_CLASS, _ = loadUiType(
#     os.path.join(os.path.dirname(__file__), "main.ui")
# )

# UI_PATH = os.path.dirname(os.path.abspath(__file__))
# FORM_CLASS = loadUiType(os.path.join(UI_PATH, "main.ui"))[0]


OSOBA_TAB_INDEX = 0
BILET_TAB_INDEX = 1
LOT_TAB_INDEX = 2


class MainWindow(QWidget):
    def __init__(self, db_handler: DatabaseHandler) -> QWidget:
        super().__init__()
        self.app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.db_handler = db_handler
        if not self.db_handler.con:
            return
        self.init_ui()
        self.init_tabs()
        self.connect_signals()

    def init_ui(self):
        self.load_ui_file()
        self.set_tab_labels()
        self.setGeometry(500, 300, 900, 700)
        self.setWindowIcon(QIcon("GUI/airport.png"))
        self.setWindowTitle("Airport Management System")

    def init_tabs(self):
        self.osoba_tab = OsobaTab(self.db_handler, self.tableView_osoba)
        self.bilet_tab = BiletTab(self.db_handler, self.tableView_bilet)
        self.lot_tab = LotTab(self.db_handler, self.tableView_lot)
        self.tabWidget.setCurrentIndex(BILET_TAB_INDEX)
        self.bilet_tab.load_data()
        self.tabWidget.setMovable(True)

    def load_ui_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "main.ui")
        loadUi(ui_file, self)

    def set_tab_labels(self):
        TAB_LABELS = ["Osoba", "Bilet", "Lot"]
        for index, label in enumerate(TAB_LABELS):
            self.tabWidget.setTabText(index, label)

    def connect_signals(self):
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.pushButton_dodaj_osoba.clicked.connect(self.osoba_tab.add_row)
        self.pushButton_dodaj_bilet.clicked.connect(self.bilet_tab.add_row)
        self.pushButton_dodaj_lot.clicked.connect(self.lot_tab.add_row)
        self.pushButton_usun_osoba.clicked.connect(self.osoba_tab.delete_row)
        self.pushButton_usun_bilet.clicked.connect(self.bilet_tab.delete_row)
        self.pushButton_usun_lot.clicked.connect(self.lot_tab.delete_row)
        self.pushButton_edytuj_osoba.clicked.connect(self.osoba_tab.edit_row)
        self.pushButton_edytuj_bilet.clicked.connect(self.bilet_tab.edit_row)
        self.pushButton_edytuj_lot.clicked.connect(self.lot_tab.edit_row)
        self.pushButton_info_osoba.clicked.connect(self.osoba_tab.info_row)
        self.pushButton_info_bilet.clicked.connect(self.bilet_tab.info_row)
        self.pushButton_info_lot.clicked.connect(self.lot_tab.info_row)

    def tabChanged(self, index: int):
        self.index = index
        if index == OSOBA_TAB_INDEX:
            self.osoba_tab.load_data()
        elif index == BILET_TAB_INDEX:
            self.bilet_tab.load_data()
        elif index == LOT_TAB_INDEX:
            self.lot_tab.load_data()

    def closeEvent(self, event):
        self.db_handler.close_connection()

    # def closeEvent(self, event: QCloseEvent):
    #     if self.db_handler:
    #         self.db_handler.close_connection()
    #     event.accept()


def run_app():
    app = QApplication(sys.argv)
    # app.setStyle("Basic")
    # app.setStyle("Material") # Android
    # app.setStyle("iOS")
    # app.setStyle("Fusion")  # Linux
    # app.setStyle("macOS")
    # app.setStyle("Windows")

    db_handler = DatabaseHandler()
    db_handler.create_connection()
    window = MainWindow(db_handler)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

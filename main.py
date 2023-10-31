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
from PyQt6.QtSql import (
    QSqlDatabase,
    QSqlQueryModel,
    QSqlTableModel,
    QSqlRelationalTableModel,
    QSqlRelation,
    QSqlRelationalDelegate,
    QSqlQuery,
)
from PyQt6.uic import loadUi, loadUiType
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QDateTime, QModelIndex
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QPainter, QColor, QTextDocument, QIcon, QFont
import sys, os

from booking_dialog import BookingDialog
from flight_dialog import FlightDialog
from person_dialog import PersonDialog

from Classes.DatabaseHandler import DatabaseHandler


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

# poprawne formatowanie zapytań SQL - https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting
# .addBindValue -> f-string
# ładuj jedynie dostępne miejsca z danego samolotu do comboboxa
# indexy osobno ma kolumnę
# wydzenenie funkcji execute_query - DatabaseHandler
# Klasa Tab i klasy OsobaTab, BiletTab i LotTab
# Klasa Tab dziedziczy po QWidget żeby QMessageBox działały poprawnie

# TODO:
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów,
# docker


# Pytania:
# - czasami testy uruchamiają wcześniejszą wersję klasy (sprzed zapisania pliku)
# - query.exec() zwraca False mimo poprawnego wykonania zapytania (person_dialog)
# - organizacja folderu projektu


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
#     os.path.join(os.path.dirname(__file__), "main_window_tableview.ui")
# )

# UI_PATH = os.path.dirname(os.path.abspath(__file__))
# FORM_CLASS = loadUiType(os.path.join(UI_PATH, "main_window_tableview.ui"))[0]


OSOBA_TAB_INDEX = 0
BILET_TAB_INDEX = 1
LOT_TAB_INDEX = 2


class Tab(QWidget):
    def __init__(self, db_handler, tab_name, table, query, id_column, dialog_class):
        self.db_handler = db_handler
        self.tab_name = tab_name
        self.table = table
        self.query = query
        self.id_column = id_column
        self.dialog_class = dialog_class
        self.init_ui()
        super().__init__()

    def init_ui(self):
        self.model = QSqlQueryModel(None)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def load_data(self):
        self.model.setQuery(self.query, self.db_handler.con)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def select_row_msg(self, text="Select one of the rows."):
        msg = QMessageBox(self, text=f"{text}")
        msg.setWindowTitle("Information")
        msg.exec()

    def get_selected_row_id(self, index: QModelIndex) -> int:
        if index.isValid():
            row = index.row()
            column = self.model.record(row).indexOf(f"{self.id_column}")
            if column != -1:
                return self.model.data(
                    self.model.index(row, column), role=Qt.ItemDataRole.DisplayRole
                )

    def add_row(self):
        window = self.dialog_class(self.db_handler)
        if window.exec():
            window.insert_into_database()
            # self.table.scrollToBottom()
            self.load_data()

    def edit_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if row_id is None:
            return self.select_row_msg()
        window = self.dialog_class(self.db_handler)
        if not window.exec():
            return
        window.update_database(id)
        self.load_data()

    def delete_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if row_id is None:
            return self.select_row_msg()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare(f"DELETE FROM {self.tab_name} WHERE {self.id_column} = ?")
            query.addBindValue(row_id)
            if query.exec():
                print("Data deleted successfully.")
            else:
                print(f"Error deleting data: {query.lastError().text()}")
            self.load_data()

    def info_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if not row_id:
            return self.select_row_msg()
        print(row_id)


class OsobaTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "osoba"
        id_column = "osoba_id"
        dialog_class = PersonDialog
        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)


class BiletTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "bilet"
        id_column = "bilet_id"
        dialog_class = BookingDialog
        query = (
            "SELECT b.bilet_id, o.imie, o.nazwisko, b.lot_id, b.miejsce_id, b.asystent "
            "FROM bilet b "
            "INNER JOIN osoba o ON o.osoba_id = b.osoba_id "
        )
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

    def info_row(self):
        if not self.table.selectedIndexes():
            return self.select_row_msg("Select row to print boarding pass.")
        self.print_preview()
        msg = QMessageBox(self, text="Boarding pass printed successfully.")
        msg.setWindowTitle("Information")
        msg.exec()

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFileName("boarding_pass.pdf")
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_boarding_pass)
        preview_dialog.exec()

    def print_boarding_pass(self, printer: QPrinter):
        painter = QPainter()
        painter.begin(printer)
        painter.setPen(QColor(0, 0, 0, 255))
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Calibri")
        painter.setFont(font())
        id = self.get_selected_row_id(self.table.currentIndex(), self.id_column)
        query = QSqlQuery()
        query.prepare(
            """
            SELECT o.imie, o.nazwisko, l.datetime, m.miejsce_samolot_id, s.samolot_id, s.model, la.city, lb.city, b.asystent, b.klasa
            FROM bilet b
            INNER JOIN osoba o ON o.osoba_id = b.osoba_id
            INNER JOIN lot l ON l.lot_id = b.lot_id
            INNER JOIN samolot s ON l.samolot_id = s.samolot_id
            INNER JOIN miejsce m ON m.miejsce_id = b.miejsce_id
            INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id
            INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id
            WHERE b.bilet_id = ?;
            """
        )
        query.addBindValue(id)
        query.exec()
        query.next()
        name = f"{query.value(0)} {query.value(1)}"
        qt_datetime = query.value(2)
        datetime = qt_datetime.toString("yyyy-MM-dd HH:mm:ss")
        seat = query.value(3)
        plane = f"{query.value(4)}, {query.value(5)}"
        airport_a = f"{query.value(6)}"
        airport_b = f"{query.value(7)}"
        asystent = f"{query.value(8)}"
        klasa = f"{query.value(9)}"

        painter.drawText(100, 100, f"Passenger Name: {name}")
        painter.drawText(100, 300, f"Flight Details: {datetime}")
        painter.drawText(100, 500, f"From: {airport_a}")
        painter.drawText(100, 700, f"To: {airport_b}")
        painter.drawText(100, 900, f"Seat Number: {seat}")
        painter.drawText(100, 1100, f"Plane: {plane}")
        painter.drawText(100, 1300, f"Assistent: {asystent}")
        painter.drawText(100, 1500, f"Class: {klasa}")

        if klasa == "Economic":
            painter.drawText(100, 1900, "Price: 300$")
        else:
            painter.drawText(100, 1900, "Price: 1000$")

        painter.end()


class LotTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "lot"
        id_column = "lot_id"
        dialog_class = FlightDialog
        query = (
            "SELECT l.lot_id, s.model, l.lotnisko_a_id, la.city, l.lotnisko_b_id, lb.city, l.datetime "
            "FROM lot l "
            "INNER JOIN samolot s ON s.samolot_id = l.samolot_id "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)


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
        self.setGeometry(500, 300, 900, 700)
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))
        self.load_ui_file()
        self.set_tab_labels()

    def init_tabs(self):
        self.osoba_tab = OsobaTab(self.db_handler, self.tableView_osoba)
        self.bilet_tab = BiletTab(self.db_handler, self.tableView_bilet)
        self.lot_tab = LotTab(self.db_handler, self.tableView_lot)
        self.tabWidget.setCurrentIndex(BILET_TAB_INDEX)
        self.bilet_tab.load_data()
        self.tabWidget.setMovable(True)

    def load_ui_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "main_window_tableview.ui")
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

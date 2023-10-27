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
from PyQt6.QtGui import QPainter, QColor, QTextDocument, QIcon
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

# poprawne formatowanie zapytań SQL
# ładuj jedynie dostępne miejsca z danego samolotu do comboboxa
# indexy osobno ma kolumnę
# wydzenenie funkcji execute_query

# TODO:
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów,
# dev containers, pipfile, setup.py
# .addBindValue -> f-string

# fields = "field1, field2, field3, field4"
# table = "table"
# conditions = "condition1=1 AND condition2=2"
# sql = (f"SELECT {fields} "
#        f"FROM {table} "
#        f"WHERE {conditions};")


# Pytania:
# - czasami testy uruchamiają wcześnieją wersję klasy
# - query.exec() zwraca False mimo poprawnego wykonania zapytania (person_dialog)
# - zapytania w booking_dialog i flight_dialog nie działają (poza usuwaniem)
# Error inserting data: ERROR:  syntax error at end of input
# LINE 1: EXECUTE
#                 ^
# (42601) QPSQL: Unable to create query


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

#     OSOBA_TAB_INDEX = 0
#     BILET_TAB_INDEX = 1
#     LOT_TAB_INDEX = 2


# class MainWindow(QWidget, FORM_CLASS):
class MainWindow(QWidget):
    def __init__(self, db_handler: DatabaseHandler) -> QWidget:
        super().__init__()
        self.app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.db_handler = db_handler
        if not self.db_handler.con:
            QMessageBox.critical(self, "Warning", "Error. Could not open database.")
            self.close()
            return
        self.init_ui()
        self.connect_signals()
        self.init_tables()

    def init_ui(self):
        self.setGeometry(500, 300, 900, 700)
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))
        self.load_ui_file()
        self.set_tab_labels()

    def load_ui_file(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "main_window_tableview.ui")
        loadUi(ui_file, self)

    def set_tab_labels(self):
        TAB_LABELS = ["Osoba", "Bilet", "Lot"]
        for index, label in enumerate(TAB_LABELS):
            self.tabWidget.setTabText(index, label)

    def connect_signals(self):
        self.tabWidget.tabBarClicked.connect(self.tabChanged)
        self.pushButton_dodaj_osoba.clicked.connect(self.dodaj_osoba)
        self.pushButton_dodaj_bilet.clicked.connect(self.dodaj_bilet)
        self.pushButton_dodaj_lot.clicked.connect(self.dodaj_lot)
        self.pushButton_usun_osoba.clicked.connect(self.usun_osoba)
        self.pushButton_usun_bilet.clicked.connect(self.usun_bilet)
        self.pushButton_usun_lot.clicked.connect(self.usun_lot)
        self.pushButton_edytuj_osoba.clicked.connect(self.edytuj_osoba)
        self.pushButton_edytuj_bilet.clicked.connect(self.edytuj_bilet)
        self.pushButton_edytuj_lot.clicked.connect(self.edytuj_lot)
        self.pushButton_info_osoba.clicked.connect(self.info_osoba)
        self.pushButton_info_bilet.clicked.connect(self.info_bilet)
        self.pushButton_info_lot.clicked.connect(self.info_lot)

    def init_tables(self):
        self.tableView_osoba.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tableView_bilet.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tableView_lot.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView_osoba.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tableView_bilet.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tableView_lot.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tableView_osoba.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableView_bilet.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableView_lot.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # self.tabWidget.setCurrentIndex(0)
        # self.load_osoba()
        self.tabWidget.setCurrentIndex(1)
        self.load_bilet()

        # self.tabWidget.setMovable(True)
        # self.tabWidget.setTabsClosable(True)

    def load_osoba(self):
        # self.model = QSqlTableModel(None)
        self.model = QSqlQueryModel(None)
        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        self.model.setQuery(query, self.db_handler.con)
        self.tableView_osoba.setModel(self.model)

        # while self.model.canFetchMore():
        #     self.model.fetchMore()
        # self.tableView_osoba.resizeColumnsToContents()

        # self.sort = QSortFilterProxyModel()
        # self.sort.setSourceModel(self.model)
        # self.sort.setDynamicSortFilter(True)
        # # self.sort.sort(0, Qt.SortOrder.AscendingOrder)
        # self.sort.sort(0, Qt.SortOrder.DescendingOrder)
        # self.tableView_osoba.setModel(self.sort)

    def load_bilet(self):
        self.model = QSqlQueryModel(None)
        query = """
            SELECT b.bilet_id, o.imie, o.nazwisko, b.lot_id, b.miejsce_id, b.asystent 
            FROM bilet b
            INNER JOIN osoba o ON o.osoba_id = b.osoba_id
            """
        self.model.setQuery(query, self.db_handler.con)
        self.tableView_bilet.setModel(self.model)

    def load_lot(self):
        self.model = QSqlQueryModel(None)
        query = """
            SELECT l.lot_id, s.model, l.lotnisko_a_id, la.city, l.lotnisko_b_id, lb.city, l.datetime 
            FROM lot l
            INNER JOIN samolot s ON s.samolot_id = l.samolot_id
            INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id
            INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id
            """
        self.model.setQuery(query, self.db_handler.con)
        self.tableView_lot.setModel(self.model)

    def tabChanged(self, index: int):
        self.index = index
        if index == 0:
            self.load_osoba()
            self.tableView_osoba.resizeColumnsToContents()
        elif index == 1:
            self.load_bilet()
            self.tableView_bilet.resizeColumnsToContents()
        elif index == 2:
            self.load_lot()
            self.tableView_bilet.resizeColumnsToContents()

    def dodaj_osoba(self):
        self.window = PersonDialog(self.db_handler)
        if self.window.exec():
            self.window.insert_into_database()
            self.tableView_osoba.scrollToBottom()
            self.load_osoba()

    def dodaj_bilet(self):
        self.window = BookingDialog(self.db_handler)
        if self.window.exec():
            self.window.insert_into_database()
            self.tableView_bilet.scrollToBottom()
            self.load_bilet()

    def dodaj_lot(self):
        self.window = FlightDialog(self.db_handler)
        if self.window.exec():
            self.window.insert_into_database()
            self.tableView_lot.scrollToBottom()
            self.load_lot()

    def select_row_msg(self, text="Select one of the rows."):
        msg = QMessageBox(self, text=f"{text}")
        msg.setWindowTitle("Information")
        msg.exec()

    def get_selected_row_id(self, index: QModelIndex, id_column_name: str) -> int:
        if index.isValid():
            row = index.row()
            column = self.model.record(row).indexOf(f"{id_column_name}")
            if column != -1:
                osoba_id = self.model.data(
                    self.model.index(row, column), role=Qt.ItemDataRole.DisplayRole
                )
                return osoba_id

    def usun_osoba(self):
        osoba_id = self.get_selected_row_id(
            self.tableView_osoba.currentIndex(), "osoba_id"
        )
        if not osoba_id:
            return self.select_row_msg()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM osoba WHERE osoba_id = ?")
            query.addBindValue(osoba_id)
            if query.exec():
                print("Data deleted successfully.")
            else:
                print(f"Error deleting data: {query.lastError().text()}")
            self.load_osoba()

    def usun_bilet(self):
        bilet_id = self.get_selected_row_id(
            self.tableView_bilet.currentIndex(), "bilet_id"
        )
        if not bilet_id:
            return self.select_row_msg()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM bilet WHERE bilet_id = ?")
            query.addBindValue(bilet_id)
            if query.exec():
                print("Data deleted successfully.")
            else:
                print(f"Error deleting data: {query.lastError().text()}")
            self.load_bilet()

    def usun_lot(self):
        lot_id = self.get_selected_row_id(self.tableView_lot.currentIndex(), "lot_id")
        if not lot_id:
            return self.select_row_msg()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM lot WHERE lot_id = ?")
            query.addBindValue(lot_id)
            if query.exec():
                print("Data deleted successfully.")
            else:
                print(f"Error deleting data: {query.lastError().text()}")
            self.load_lot()

    def edytuj_osoba(self):
        osoba_id = self.get_selected_row_id(
            self.tableView_osoba.currentIndex(), "osoba_id"
        )
        if not osoba_id:
            return self.select_row_msg()
        self.window = PersonDialog(self.db_handler)
        if not self.window.exec():
            return
        self.window.update_database(osoba_id)
        self.load_osoba()

    def edytuj_bilet(self):
        bilet_id = self.get_selected_row_id(
            self.tableView_bilet.currentIndex(), "bilet_id"
        )
        if not bilet_id:
            return self.select_row_msg()
        self.window = BookingDialog(self.db_handler)
        if not self.window.exec():
            return
        self.window.update_database(bilet_id)
        self.load_bilet()

    def edytuj_lot(self):
        lot_id = self.get_selected_row_id(self.tableView_lot.currentIndex(), "lot_id")
        if not lot_id:
            return self.select_row_msg()
        self.window = FlightDialog(self.db_handler)
        if not self.window.exec():
            return
        self.window.update_database(lot_id)
        self.load_lot()

    def info_osoba(self):
        osoba_id = self.get_selected_row_id(
            self.tableView_osoba.currentIndex(), "osoba_id"
        )
        if not osoba_id:
            return self.select_row_msg()
        print(osoba_id)

    def info_bilet(self):
        if not self.tableView_bilet.selectedIndexes():
            return self.select_row_msg("Select row to print boarding pass.")

        self.print_preview()
        msg = QMessageBox(self, text="Boarding pass printed successfully.")
        msg.setWindowTitle("Information")
        msg.exec()

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFileName("boarding_pass.pdf")
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_boarding_pass)
        previewDialog.exec()

    def print_boarding_pass(self, printer: QPrinter):
        painter = QPainter()
        painter.begin(printer)
        painter.setPen(QColor(0, 0, 0, 255))
        # painter.setFont(self.font())
        bilet_id = self.get_selected_row_id(
            self.tableView_bilet.currentIndex(), "bilet_id"
        )
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
        query.addBindValue(bilet_id)
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

    def info_lot(self):
        lot_id = self.get_selected_row_id(self.tableView_osoba.currentIndex(), "lot_id")
        if not lot_id:
            return self.select_row_msg()
        print(lot_id)

    def closeEvent(self, event):
        self.db_handler.close_connection()


def run_app():
    app = QApplication(sys.argv)
    # app.setStyle("Basic")
    # app.setStyle("Material") # Android
    # app.setStyle("iOS")
    # app.setStyle("Fusion") # Linux
    # app.setStyle("macOS")
    # app.setStyle("Windows")

    db_handler = DatabaseHandler()
    db_handler.create_connection()
    # db_handler = DatabaseHandler(database_name="test_lotnisko")
    window = MainWindow(db_handler)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

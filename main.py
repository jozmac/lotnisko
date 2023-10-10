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
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QDateTime
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QPainter, QColor, QTextDocument, QIcon
import sys, os
from functions import (
    get_data,
    drop_tables,
    create_tables,
    select_osoba,
    select_lotnisko,
    select_samolot,
    select_bilet,
    select_lot,
    select_miejsce,
    select_zajete_miejsce,
    select_zatrudnienie,
    select_pracownik,
)


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
# Zmienić nazwy przycisków
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwieranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# dodać tytuły i ikony do okien
# wyświetlanie i edycja id
# zaznaczanie pojedyńczego wiersza tabeli
# get_data zamiast get_selected_opitons

# TODO:
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów - czy fstring jest taki sam jak query

# Wczytywanie listy dostępnych miejsc - zajete_miejsce

# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie) -
# join zamiast tabledelegate


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
# - formatowanie przy kopiowaniu - dodatkowe spacje
#


class MainWindow(QWidget):
    def __init__(self, db_handler):
        super().__init__()

        self.db_handler = db_handler
        if not self.db_handler.db:
            QMessageBox.critical(self, "Warning", "Error. Could not open database.")
            self.close()
            return

        self.init_gui()

        # get_widget_dict =

    def init_gui(self):
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, "GUI")
        os.chdir(gui_directory)
        # os.chdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]))), 'GUI')
        loadUi("main_window_tableview.ui", self)
        os.chdir(directory)

        self.setGeometry(500, 300, 900, 700)
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # print(dir_path)

        TAB_LABELS = ["Osoba", "Bilet", "Lot"]
        for index, label in enumerate(TAB_LABELS):
            self.tabWidget.setTabText(index, label)

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

        # Disable cell editing
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

        # # self.tabWidget.setMovable(True)
        # # self.tabWidget.setTabsClosable(True)

    # def on_data_change(self, topLeft, bottomRight):
    def on_data_change(self):
        response = QMessageBox.question(
            self,
            "Confirm Edit",
            "Are you sure you want to save this change?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if response == QMessageBox.StandardButton.Yes:
            if self.model.submitAll():
                print("Change submitted successfully.")
            else:
                print("Error submitting change:", self.model.lastError().text())
        else:
            self.model.dataChanged.disconnect(self.on_data_change)
            self.model.revertAll()  # TODO - rozbić na 2 metody
            self.model.dataChanged.connect(self.on_data_change)

    # TODO
    def load_osoba(self):
        # self.model = QSqlTableModel()
        self.model = QSqlTableModel(None, self.db_handler.db)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        # self.model = QSqlRelationalTableModel()
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("osoba")

        # self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        # query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        # self.model.setQuery(query, self.db_handler.db)
        self.tableView_osoba.setModel(self.model)
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)

        # self.tableView_osoba.setItemDelegate(QSqlRelationalDelegate(self.tableView_osoba)) # combobox

        # for idx, name in enumerate(headerNames):
        #     model.setHeaderData(idx, Qt.Horizontal, name)

        # while self.model.canFetchMore():
        #     self.model.fetchMore()
        # self.tableView_osoba.resizeColumnsToContents()

        # print(f"database open: {db.isOpen()}")

        # self.sort = QSortFilterProxyModel()
        # self.sort.setSourceModel(model)
        # self.sort.setDynamicSortFilter(True)
        # self.sort.sort(0, Qt.SortOrder.AscendingOrder)
        # self.tableView_osoba.setModel(self.sort)

    def load_bilet(self):
        self.model = QSqlRelationalTableModel(None, self.db_handler.db)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("bilet")
        self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        # query = "SELECT bilet_id, osoba_id, lot_id, miejsce_id, asystent FROM bilet"
        # self.model.setQuery(query, self.db_handler.db)
        self.tableView_bilet.setModel(self.model)
        self.tableView_bilet.setItemDelegate(
            QSqlRelationalDelegate(self.tableView_bilet)
        )  # combobox
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)
        # self.model.isDirty.connect(self.on_data_change)

    def load_lot(self):
        self.model = QSqlRelationalTableModel(None, self.db_handler.db)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("lot")
        self.model.setRelation(1, QSqlRelation("samolot", "samolot_id", "model"))

        self.tableView_lot.setModel(self.model)
        self.tableView_lot.setItemDelegate(
            QSqlRelationalDelegate(self.tableView_lot)
        )  # combobox
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)

    def tabChanged(self, index):
        self.index = index
        self.model.dataChanged.disconnect(self.on_data_change)
        if index == 0:
            self.load_osoba()
            self.tableView_osoba.resizeColumnsToContents()
        elif index == 1:
            self.load_bilet()
            self.tableView_bilet.resizeColumnsToContents()
        elif index == 2:
            self.load_lot()

    def dodaj_osoba(self):
        window = PersonDialog()
        if window.exec():
            window.insert_to_database()
            self.tableView_osoba.scrollToBottom()
            self.model.select()

    def dodaj_bilet(self):
        window = BookingDialog(self.db_handler.db)
        if window.exec():
            window.insert_to_database()
            self.tableView_bilet.scrollToBottom()
            self.model.select()

    def dodaj_lot(self):
        window = FlightDialog(self.db_handler.db)
        if window.exec():
            window.insert_to_database()
            self.tableView_lot.scrollToBottom()
            self.model.select()

    def usun_osoba(self):
        indexes = self.tableView_osoba.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to delete.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            # result = self.model.deleteRowFromTable(self.tableView_osoba.currentIndex().row())
            # # result = self.model.deleteRowFromTable(self.tableView_osoba.selectedIndexes())
            # # result = self.model.removeRows(self.tableView_osoba.selectedIndexes())
            # # result = self.model.removeRow(self.tableView_osoba.currentIndex().row())
            # print(f"result: {result}, {self.tableView_osoba.currentIndex().row()}, {self.tableView_osoba.selectedIndexes()}")
            # print(self.model.lastError().text())
            # self.model.select()

            index = self.tableView_osoba.currentIndex()
            NewIndex = self.tableView_osoba.model().index(index.row(), 0)
            osoba_id = self.tableView_osoba.model().data(NewIndex)
            query = QSqlQuery()
            query.prepare("DELETE FROM osoba WHERE osoba_id = ?")
            query.addBindValue(osoba_id)
            if query.exec():
                print(f"Data deleted successfully.")
            else:
                print(f"Error deleting data: {query.lastError().text()}")
            print(query.lastError().text())
            self.model.select()

    def usun_bilet(self):
        indexes = self.tableView_bilet.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to delete.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.deleteRowFromTable(self.tableView_bilet.currentIndex().row())
            self.model.select()

    def usun_lot(self):
        indexes = self.tableView_lot.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to delete.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.deleteRowFromTable(self.tableView_lot.currentIndex().row())
            self.model.select()

    # TODO - model queries
    def edytuj_osoba(self):
        indexes = self.tableView_osoba.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to edit.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        index = self.tableView_osoba.currentIndex()
        NewIndex = self.tableView_osoba.model().index(index.row(), 0)
        osoba_id = self.tableView_osoba.model().data(NewIndex)
        window = PersonDialog()
        if not window.exec():
            return

        window.get_data()
        query = QSqlQuery()
        query.prepare(
            "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
        )
        query.addBindValue(window.imie)
        query.addBindValue(window.nazwisko)
        query.addBindValue(window.stanowisko)
        query.addBindValue(osoba_id)
        if query.exec():
            print(f"Data edited successfully.")
        else:
            print(f"Error editing data: {query.lastError().text()}")
        print(query.lastError().text())
        self.model.select()

    def edytuj_bilet(self):
        indexes = self.tableView_bilet.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to edit.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        index = self.tableView_bilet.currentIndex()
        NewIndex = self.tableView_bilet.model().index(index.row(), 0)
        bilet_id = self.tableView_bilet.model().data(NewIndex)
        window = BookingDialog(self.db_handler.db)
        if not window.exec():
            return

        window.get_data()
        query = QSqlQuery()
        query.prepare(
            "UPDATE bilet SET osoba_id = ?, lot_id = ?, miejsce_id = ?, asystent = ?, klasa = ? WHERE bilet_id = ?"
        )
        query.addBindValue(window.person)
        query.addBindValue(window.flight)
        query.addBindValue(window.seat)
        query.addBindValue(window.assistant)
        query.addBindValue(window.flightclass)
        query.addBindValue(bilet_id)
        if query.exec():
            print(f"Data edited successfully.")
        else:
            print(f"Error editing data: {query.lastError().text()}")
        print(query.lastError().text())
        self.model.select()

    def edytuj_lot(self):
        indexes = self.tableView_lot.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to edit.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        index = self.tableView_lot.currentIndex()
        NewIndex = self.tableView_lot.model().index(index.row(), 0)
        lot_id = self.tableView_lot.model().data(NewIndex)
        window = FlightDialog(self.db_handler.db)
        window.get_data()
        if not window.exec():
            return
        # imie, nazwisko, stanowisko = window.get_selected_options()
        query = QSqlQuery()
        query.prepare(
            "UPDATE osoba SET samolot_id = ?, lotnisko_a_id = ?, lotnisko_b_id = ?, datetime = ? WHERE lot_id = ?"
        )
        query.addBindValue(window.plane)
        query.addBindValue(window.airport_a)
        query.addBindValue(window.airport_b)
        query.addBindValue(window.qt_datetime)

        if query.exec():
            print(f"Data edited successfully.")
        else:
            print(f"Error editing data: {query.lastError().text()}")
        print(query.lastError().text())
        self.model.select()

    # def edytuj_bilet(self):
    #     selected_index = self.tableView_bilet.selectionModel().currentIndex()
    #     if selected_index.isValid():
    #         self.tableView_bilet.edit(selected_index)

    # def edytuj_lot(self):
    #     selected_index = self.tableView_lot.selectionModel().currentIndex()
    #     if selected_index.isValid():
    #         self.tableView_lot.edit(selected_index)

    def info_osoba(self):
        pass

    def info_bilet(self):
        indexes = self.tableView_bilet.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select row to print boarding pass.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return

        self.print_preview()
        # print("Boarding pass printed successfully.")
        msg = QMessageBox(self, text="Boarding pass printed successfully.")
        msg.setWindowTitle("Informacja")
        msg.exec()

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFileName("boarding_pass.pdf")
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_boarding_pass)
        previewDialog.exec()

    def print_boarding_pass(self, printer):
        painter = QPainter()
        painter.begin(printer)
        painter.setPen(QColor(0, 0, 0, 255))
        # painter.setFont(self.font())
        index = self.tableView_bilet.currentIndex()
        NewIndex = self.tableView_bilet.model().index(index.row(), 0)
        bilet_id = self.tableView_bilet.model().data(NewIndex)
        # print(bilet_id)
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
            painter.drawText(100, 1700, f"Price: 300$")
        else:
            painter.drawText(100, 1900, f"Price: 1000$")

        painter.end()

    def info_lot(self):
        pass

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

    # drop_tables()
    # create_tables()
    # osoba, lotnisko, samolot = get_data()
    db_handler = DatabaseHandler()
    window = MainWindow(db_handler)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

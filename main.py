from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QTableWidgetItem,
    QTableView,
    QMessageBox,
    QDialog,
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
from PyQt6.QtGui import QPainter, QColor, QTextDocument
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


from booking_dialog import Booking_dialog
from flight_dialog import Flight_dialog
from person_dialog import Person_dialog


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
# model/view
# comboboxy - jak załadować dane, czytanie id wybranej opcji po kliknięciu ok - słowniki (dict)
# person_dialog
# db.close()
# edytowanie komórki po kliknięciu edytuj
# drukowanie karty pokładowej
# black formatter
# rollback -czy napewno chcesz zatwierdzić zmiany?

# TODO:
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów - czy fstring jest taki sam jak query
# cena biletu

# join zamiast tabledelegate / caschowanie
# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie) -
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwieranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# Wczytywanie listy dostępnych miejsc
# cashowanie tabeli lotów
# usunąć tabele zatrudnienie, miejsca, lotnisko, miejsce, zajęte miejsce z głównego okna
# dodać tytuły i ikony do okien


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
# - TODOs
# - okno dialpogowe po edycji komórki pojawia się dwa razy
# - dialog zamawiania


def create_connection():
    try:
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("localhost")
        db.setDatabaseName("lotnisko")
        db.setUserName("postgres")
        db.setPassword("password")
        db.setPort(5432)

        if not db.open():
            raise ConnectionError(
                f"Could not open database. Error: {db.lastError().text()}"
            )
        return db
    except Exception as e:
        raise ConnectionError(f"Connection error: {e}")


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.db = create_connection()
        if not self.db:
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

        # Rename tabs
        # tab_labels = [
        #     "Osoba", "Bilet", "Lot", "Samolot", "Miejsce",
        #     "Zajete_miejsce", "Lotnisko", "Pracownik", "Zatrudnienie"]
        TAB_LABELS = ["Osoba", "Bilet", "Lot"]
        for index, label in enumerate(TAB_LABELS):
            self.tabWidget.setTabText(index, label)

        self.tabWidget.tabBarClicked.connect(self.tabChanged)

        self.pushButton_dodaj_0.clicked.connect(self.dodaj_osoba)
        self.pushButton_dodaj_1.clicked.connect(self.dodaj_bilet)
        self.pushButton_dodaj_2.clicked.connect(self.dodaj_lot)
        self.pushButton_usun_0.clicked.connect(self.usun_osoba)
        self.pushButton_usun_1.clicked.connect(self.usun_bilet)
        self.pushButton_usun_2.clicked.connect(self.usun_lot)
        self.pushButton_edytuj_0.clicked.connect(self.edytuj_osoba)
        self.pushButton_edytuj_1.clicked.connect(self.edytuj_bilet)
        self.pushButton_edytuj_2.clicked.connect(self.edytuj_lot)
        self.pushButton_info_0.clicked.connect(self.info_osoba)
        self.pushButton_info_1.clicked.connect(self.info_bilet)
        self.pushButton_info_2.clicked.connect(self.info_lot)

        # set default tab
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
            # self.model.dataChanged.disconnect(self.on_data_change)
            self.model.revertAll()  # rozbić na 2 metody

    # def closeEvent(self, event):
    #     if self.model.isDirty():
    #         reply = QMessageBox.question(
    #             self,
    #             "Unsaved Changes",
    #             "There are unsaved changes. Do you want to save them?",
    #             QMessageBox.StandardButton.Save
    #             | QMessageBox.StandardButton.Discard
    #             | QMessageBox.StandardButton.Cancel,
    #             QMessageBox.StandardButton.Save,
    #         )

    #         if reply == QMessageBox.StandardButton.Save:
    #             self.saveChanges()
    #         elif reply == QMessageBox.StandardButton.Discard:
    #             pass  # Do nothing and discard changes
    #         else:
    #             event.ignore()

    # TODO
    def load_osoba(self):
        # self.model = QSqlTableModel()
        self.model = QSqlTableModel(None, self.db)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        # self.model = QSqlRelationalTableModel()
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("osoba")

        # self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        # query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        # self.model.setQuery(query, self.db)
        self.tableView_0.setModel(self.model)
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)

        # self.tableView_0.setItemDelegate(QSqlRelationalDelegate(self.tableView_0)) # combobox

        # for idx, name in enumerate(headerNames):
        #     model.setHeaderData(idx, Qt.Horizontal, name)

        # while self.model.canFetchMore():
        #     self.model.fetchMore()
        # self.tableView_0.resizeColumnsToContents()

        # print(f"database open: {db.isOpen()}")

        # sort
        # self.sort = QSortFilterProxyModel()
        # self.sort.setSourceModel(model)
        # self.sort.setDynamicSortFilter(True)
        # self.sort.sort(0, Qt.SortOrder.AscendingOrder)
        # self.tableView_0.setModel(self.sort)

    def load_bilet(self):
        self.model = QSqlRelationalTableModel(None, self.db)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("bilet")
        self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        # query = "SELECT bilet_id, osoba_id, lot_id, miejsce_id, asystent FROM bilet"
        # self.model.setQuery(query, self.db)
        self.tableView_1.setModel(self.model)
        self.tableView_1.setItemDelegate(
            QSqlRelationalDelegate(self.tableView_1)
        )  # combobox
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)  # TODO - jest wyzwalane 2x

    def load_lot(self):
        self.model = QSqlRelationalTableModel(None, self.db)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("lot")
        self.model.setRelation(1, QSqlRelation("samolot", "samolot_id", "model"))

        self.tableView_2.setModel(self.model)
        self.tableView_2.setItemDelegate(
            QSqlRelationalDelegate(self.tableView_2)
        )  # combobox
        self.model.select()
        self.model.dataChanged.connect(self.on_data_change)

    def tabChanged(self, index):
        self.index = index
        self.model.dataChanged.disconnect(self.on_data_change)
        if index == 0:
            self.load_osoba()
            self.tableView_0.resizeColumnsToContents()
        elif index == 1:
            self.load_bilet()
            self.tableView_1.resizeColumnsToContents()
        elif index == 2:
            self.load_lot()

    def dodaj_osoba(self):
        window = Person_dialog()
        if window.exec():
            window.insert_to_database()
            self.tableView_0.scrollToBottom()
            self.model.select()

    def dodaj_bilet(self):
        window = Booking_dialog(self.db)
        if window.exec():
            window.insert_to_database()
            self.tableView_1.scrollToBottom()
            self.model.select()

    def dodaj_lot(self):
        window = Flight_dialog(self.db)
        if window.exec():
            window.insert_to_database()
            self.tableView_2.scrollToBottom()
            self.model.select()

    def usun_osoba(self):
        indexes = self.tableView_0.selectedIndexes()
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
            # result = self.model.deleteRowFromTable(self.tableView_0.currentIndex().row())
            # # result = self.model.deleteRowFromTable(self.tableView_0.selectedIndexes())
            # # result = self.model.removeRows(self.tableView_0.selectedIndexes())
            # # result = self.model.removeRow(self.tableView_0.currentIndex().row())
            # print(f"result: {result}, {self.tableView_0.currentIndex().row()}, {self.tableView_0.selectedIndexes()}")
            # print(self.model.lastError().text())
            # self.model.select()

            index = self.tableView_0.currentIndex()
            NewIndex = self.tableView_0.model().index(index.row(), 0)
            osoba_id = self.tableView_0.model().data(NewIndex)
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
        indexes = self.tableView_1.selectedIndexes()
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
            self.model.deleteRowFromTable(self.tableView_1.currentIndex().row())
            self.model.select()

    def usun_lot(self):
        indexes = self.tableView_2.selectedIndexes()
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
            self.model.deleteRowFromTable(self.tableView_2.currentIndex().row())
            self.model.select()

    # TODO - model queries
    def edytuj_osoba(self):
        indexes = self.tableView_0.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text="Select the row to edit.")
            msg.setWindowTitle("Informacja")
            msg.exec()
            return
        index = self.tableView_0.currentIndex()
        NewIndex = self.tableView_0.model().index(index.row(), 0)
        osoba_id = self.tableView_0.model().data(NewIndex)
        window = Person_dialog()
        if not window.exec():
            return
        imie, nazwisko, stanowisko = window.get_selected_options()
        query = QSqlQuery()
        query.prepare(
            "UPDATE osoba SET imie = ?, nazwisko = ?, stanowisko = ? WHERE osoba_id = ?"
        )
        query.addBindValue(imie)
        query.addBindValue(nazwisko)
        query.addBindValue(stanowisko)
        query.addBindValue(osoba_id)
        if query.exec():
            print(f"Data edited successfully.")
        else:
            print(f"Error editing data: {query.lastError().text()}")
        print(query.lastError().text())
        self.model.select()

    def edytuj_bilet(self):
        selected_index = self.tableView_1.selectionModel().currentIndex()
        if selected_index.isValid():
            self.tableView_1.edit(selected_index)

    def edytuj_lot(self):
        selected_index = self.tableView_2.selectionModel().currentIndex()
        if selected_index.isValid():
            self.tableView_2.edit(selected_index)

    def info_osoba(self):
        pass

    def info_bilet(self):
        indexes = self.tableView_1.selectedIndexes()
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
        index = self.tableView_1.currentIndex()
        NewIndex = self.tableView_1.model().index(index.row(), 0)
        bilet_id = self.tableView_1.model().data(NewIndex)
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

        painter.drawText(100, 100, f"Passenger Name: {name}")
        painter.drawText(100, 300, f"Flight Details: {datetime}")
        painter.drawText(100, 500, f"From: {airport_a}")
        painter.drawText(100, 700, f"To: {airport_b}")
        painter.drawText(100, 900, f"Seat Number: {seat}")
        painter.drawText(100, 1100, f"Plane: {plane}")
        painter.end()

    def info_lot(self):
        pass

    def closeEvent(self, event):
        self.db.close()
        if self.db.isOpen():
            print("Database is still open.")
        else:
            print("Database closed.")


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

    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

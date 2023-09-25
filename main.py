from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem, QTableView, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QDateTime
import sys, os
from functions import get_data, drop_tables, create_tables, select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
# from PyQt6 import QtGui
from booking_dialog import Booking_dialog
from flight_dialog import Flight_dialog
from person_dialog import Person_dialog
# import psycopg2 as pg2

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

# TODO:
# rollback -czy napewno chcesz zatwierdzić zmiany?
# edytowanie komórki po kliknięciu edytuj
# pytest - testy klas, sprawdzanie jednego wiersza lotów, sprawdzenie selektów - czy fstring jest taki sam jak query
# cena biletu
# drukowanie karty pokładowej

# join zamiast tabledelegate / caschowanie
# indeksowanie - CREATE INDEX osoba_imie ON osoba(imie)
# rozdzielić klasy do osobnych plików, osobne foldery dla dialogów, klas, skryptów - (main_window, klasy, dialog_window, db_connection (otwieranie bazy w klasie a nie na początku kodu)) (SRP = single response principle - jedna klasa - jedna funkcja)
# dodać tytuły i ikony do okien
# Wczytywanie listy dostępnych miejsc
# usunąć tabele zatrudnienie, miejsca, lotnisko, miejsce, zajęte miejsce z głównego okna
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


class CustomRelationalTableModel(QSqlRelationalTableModel):
    # def __init__(self, parent=None, db=None):
    #     super().__init__(parent, db)
    def __init__(self):
        super().__init__()
        
    def beforeInsert(self, record):
        return self.confirmEdits()

    def beforeUpdate(self, record):
        return self.confirmEdits()

    def confirmEdits(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText("Do you want to save the changes?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)

        result = msgBox.exec()
        return result == QMessageBox.StandardButton.Yes


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
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        # os.chdir(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]))), 'GUI')
        loadUi("main_window_tableview.ui", self)

        # Rename tabs
        # tab_labels = [
        #     "Osoba", "Bilet", "Lot", "Samolot", "Miejsce", 
        #     "Zajete_miejsce", "Lotnisko", "Pracownik", "Zatrudnienie"]
        TAB_LABELS = [
            "Osoba", "Bilet", "Lot"]
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

        # self.tableView_0.model().dataChanged.connect(self.on_data_changed)
        # self.tableView_1.model().dataChanged.connect(self.on_data_changed)
        # self.tableView_2.model().dataChanged.connect(self.on_data_changed)
        # self.model.model().dataChanged.connect(self.on_data_changed)

        # set default tab
        self.tabWidget.setCurrentIndex(0)
        self.load_osoba()
        # self.tabChanged

        # # self.tabWidget.setMovable(True)
        # # self.tabWidget.setTabsClosable(True)


    def load_osoba(self):
        self.model = QSqlTableModel()
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        # self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        # self.model = QSqlRelationalTableModel()
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("osoba")
        # self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        self.model.setQuery(query, self.db)
        self.tableView_0.setModel(self.model)
        self.model.select()

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
        # self.model = QSqlRelationalTableModel()
        self.model = CustomRelationalTableModel()
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("bilet")
        self.model.setRelation(1, QSqlRelation("osoba", "osoba_id", "nazwisko"))

        query = "SELECT bilet_id, osoba_id, lot_id, miejsce_id, asystent FROM bilet"
        self.model.setQuery(query, self.db)
        self.tableView_1.setModel(self.model)
        self.tableView_1.setItemDelegate(QSqlRelationalDelegate(self.tableView_1)) # combobox
        self.model.select()

    def load_lot(self):
        # self.model = QSqlRelationalTableModel()
        self.model = CustomRelationalTableModel()
        # self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnManualSubmit)
        self.model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)

        self.model.setTable("lot")
        self.model.setRelation(1, QSqlRelation("samolot", "samolot_id", "model"))

        query = "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        self.model.setQuery(query, self.db)
        self.tableView_2.setModel(self.model)
        self.tableView_2.setItemDelegate(QSqlRelationalDelegate(self.tableView_2)) # combobox
        self.model.select()

    def tabChanged(self, index):
        self.index = index

        if index == 0:
            self.load_osoba()
            self.tableView_0.resizeColumnsToContents()
        elif index == 1:
            self.load_bilet()
            self.tableView_1.resizeColumnsToContents()
        elif index == 2:
            self.load_lot()
            self.tableView_2.resizeColumnsToContents()

    
    def dodaj_osoba(self):
        # print(f"tableName - {self.model.tableName()}")
        # self.model.insertRow(self.model.rowCount())
        # self.tableView_0.scrollToBottom()
        window = Person_dialog()
        if window.exec():
            # self.tabChanged(self.index)
            self.tableView_0.scrollToBottom()
            self.model.select()

    def dodaj_bilet(self):
        window = Booking_dialog(self.db)
        if window.exec():
            # self.tabChanged(self.index)
            self.tableView_1.scrollToBottom()
            self.model.select()
        
    def dodaj_lot(self):
        window = Flight_dialog(self.db)
        if window.exec():
            # self.tabChanged(self.index)
            self.tableView_2.scrollToBottom()
            self.model.select()
        

    def usun_osoba(self):
        # item = self.tableView_1.item(row)
        # if item is None:
        #     return
        indexes = self.tableView_0.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text='Select the row to delete.')
            msg.setWindowTitle('Informacja')
            msg.exec()
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to remove selected row?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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
            msg = QMessageBox(self, text='Select the row to delete.')
            msg.setWindowTitle('Informacja')
            msg.exec()
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to remove selected row?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.model.deleteRowFromTable(self.tableView_1.currentIndex().row())
            self.model.select()
            
    def usun_lot(self):
        indexes = self.tableView_2.selectedIndexes()
        if not indexes:
            msg = QMessageBox(self, text='Select the row to delete.')
            msg.setWindowTitle('Informacja')
            msg.exec()
            return
        reply = QMessageBox.question(self, "Remove Item", "Do you want to remove selected row?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.model.deleteRowFromTable(self.tableView_2.currentIndex().row())
            self.model.select()

    
    def on_data_changed(self, topLeft, bottomRight):
        # Slot function to show a confirmation dialog when data is edited
        response = QMessageBox.question(self, "Confirm Edit", "Are you sure you want to save this change?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.No)

        if response == QMessageBox.StandardButton.Yes:
            # Submit the changes to the database manually
            if self.model.submitAll():
                print("Change submitted successfully.")
            else:
                print("Error submitting change:", self.model.lastError().text())
        else:
            # Revert the change if the user clicks No
            self.model.revertAll()

    # TODO
    def edytuj_osoba(self):
        # UPDATE table_name
        # SET column1 = value1, column2 = value2, ...
        # WHERE condition;

        # table_sel_model = self.licence_table.selectionModel()
        # rows = table_sel_model.selectedRows()
        # if not rows:
        #     msg = QMessageBox(self, text='Nie wybrano gminy!')
        #     msg.setWindowTitle('Informacja')
        #     msg.exec_()
        #     return
        pass

    def edytuj_bilet(self):
        selected_index = self.tableView_1.selectionModel().currentIndex()
        if selected_index.isValid():
            self.tableView_1.edit(selected_index)


        # selected_index = self.tableView_1.selectionModel().currentIndex()

        # if selected_index.isValid():
        #     if not self.tableView_1.state() == QTableView.EditState.EditingState:
        #         self.tableView_1.edit(selected_index)
                
        #         if self.model.itemFromIndex(selected_index).isModified():
        #             reply = QMessageBox.question(
        #                 self,
        #                 "Save Changes",
        #                 "Do you want to save the changes you made?",
        #                 QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard,
        #                 QMessageBox.StandardButton.Save,
        #             )

        #             if reply == QMessageBox.StandardButton.Save:
        #                 # Save the changes
        #                 self.model.itemFromIndex(selected_index).setModified(False)
        #                 # You may want to implement your save logic here
        #             else:
        #                 # Discard the changes
        #                 self.model.itemFromIndex(selected_index).setModified(False)
        #                 # You may want to implement your discard logic here
                
            
    def edytuj_lot(self):
        pass

    def info_osoba(self):
        pass

    def info_bilet(self):
        pass
            
    def info_lot(self):
        pass


    def closeEvent(self, event):
        self.db.close()
        if self.db.isOpen():
            print("Database is still open.")
        else:
            print("Database closed.")

        # reply = QMessageBox.question(self, "Window Close", "Are you sure you want to close the window?",
        #                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # if reply == QMessageBox.StandardButton.Yes:
        #     event.accept()
        # else:
        #     event.reject()


    # def addRecord():
    #     model.insertRow(model.rowCount())
    #     view.scrollToBottom()

    # def delRecord():
    #     model.deleteRowFromTable(view.currentIndex().row())
    #     model.select()



    # def warn_msg(self):
    #     QMessageBox.warning(self, "Warning", "This is warning message.")

    # def info_msg(self):
    #     QMessageBox.information(self, "Information", "This is information message.")

    # def about_msg(self):
    #     QMessageBox.about(self, "About", "This is about message.")



    # def dodaj_lot(self):
    #     window = Flight_dialog(self.db)
    #     if window.exec():
    #         samolot, lotnisko_a, lotnisko_b, datetime = window.get_selected_options()
    #         print(f"Selected options: {samolot}, {lotnisko_a}, {lotnisko_b}, {datetime}")
    #         # print(f"time = {datetime.strftime('%Y-%m-%d %H:%M:%S')}; type = {type(datetime.strftime('%Y-%m-%d %H:%M:%S'))}")
    #         datetime_str = datetime.strftime('%Y-%m-%d %H:%M:%S')
    #         qt_datetime = QDateTime.fromString(datetime_str, 'yyyy-MM-dd HH:mm:ss')

    #         query = QSqlQuery()
    #         query.prepare("INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) VALUES (?, ?, ?, ?)")
    #         query.addBindValue(samolot)
    #         query.addBindValue(lotnisko_a)
    #         query.addBindValue(lotnisko_b)
    #         query.addBindValue(qt_datetime)
    #         if query.exec():
    #             print(f"Data inserted successfully.")
    #         else:
    #             print(f"Error inserting data: {query.lastError().text()}")

    #         self.tabChanged(self.index)
    #         self.tableView_2.scrollToBottom()

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

    #         self.tabChanged(self.index)


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

    #     self.tabChanged(self.index)

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

    #     self.tabChanged(self.index)


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
            
    #         self.tabChanged(self.index)



def run_app():
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    # drop_tables()
    # create_tables()
    # osoba, lotnisko, samolot = get_data()

    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()

from PyQt6.QtWidgets import QDialog, QApplication, QComboBox, QTableView, QStyledItemDelegate, QAbstractItemDelegate, QStyle
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery, QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt6.QtCore import Qt, QModelIndex, QStringListModel, QAbstractTableModel, QAbstractItemModel, QSize, QDateTime

import sys, os
# from functions import get_data, drop_tables, create_tables
from functions import select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
from datetime import datetime


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
    

class CustomSqlRelationalTableModel(QSqlRelationalTableModel):
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row_index = index.row()
            data = ""
            for column_index in range(self.columnCount()):
                value = super().data(self.index(row_index, column_index), Qt.ItemDataRole.EditRole)
                data += f" - {value}" if data else f"{value}"
            return f"{data}"
        return super().data(index, role)

# class CustomSqlRelationalTableModel(QSqlRelationalTableModel):
#     def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
#         if role == Qt.ItemDataRole.DisplayRole:
#             column_index = index.column()
#             if column_index == 0:
#                 data1 = super().data(index.siblingAtColumn(1), Qt.ItemDataRole.EditRole)
#                 data2 = super().data(index.siblingAtColumn(2), Qt.ItemDataRole.EditRole)
#                 return f"{data1} - {data2}"

#         return super().data(index, role)

class Flight_dialog(QDialog):
    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        loadUi("flight_dialog.ui", self)

        self.db = db
        # self.db = create_connection()
        # if not self.db:
        #     return

        # # Create the delegate
        # self.relational_delegate = QSqlRelationalDelegate(self.comboBox_plane)
        # # Set the delegate for comboBox_plane
        # self.comboBox_plane.setItemDelegate(self.relational_delegate)

        self.load_combo_boxes()

        self.comboBox_from.setCurrentIndex(1538)
        self.comboBox_to.setCurrentIndex(1538)

        # text = cbo.itemText(index)
        # data = cbo.itemData(index, QtCore.Qt.UserRole)
        # check_state = cbo.itemData(index, QtCore.Qt.CheckStateRole)
        # print(index, text, data, check_state)

    # cbo.currentIndexChanged[int].connect(on_current_index_changed)

        self.buttonBox.accepted.connect(self.insert_selected_data)

    def load_combo_boxes(self):
        # samolot_query = QSqlQuery("SELECT samolot_id, model, ilosc_miejsc FROM samolot", self.db)
        # lotnisko_query = QSqlQuery("SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko", self.db)

        # samolot_model = CustomItemModel(samolot_query)
        # lotnisko_model = CustomItemModel(lotnisko_query)

        # self.model = QSqlTableModel()
        # self.model = QSqlRelationalTableModel()

        self.samolot = CustomSqlRelationalTableModel()
        # self.samolot.setTable("samolot")
        # self.samolot.setRelation(0, QSqlRelation("samolot", "samolot_id", "model"))
        query = "SELECT samolot_id, model, ilosc_miejsc FROM samolot"
        self.samolot.setQuery(query, self.db)
        self.samolot.select()
        # self.comboBox_plane.setItemDelegate(QSqlRelationalDelegate(self.comboBox_plane)) # combobox

        self.lotnisko = CustomSqlRelationalTableModel()
        query = "SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko"
        self.lotnisko.setQuery(query, self.db)
        self.lotnisko.select()

        # self.relational_delegate.setModel(self.samolot)
        # self.relational_delegate.setColumn(1)  # Set the column you want to display in the combobox

        self.comboBox_plane.setModel(self.samolot)
        self.comboBox_from.setModel(self.lotnisko)
        self.comboBox_to.setModel(self.lotnisko)
        # self.comboBox_plane.setModelColumn(1)
        # self.comboBox_plane.setItemDelegate(MultiColumnItemDelegate())

    def insert_selected_data(self):
        # TODO
        selected_date = self.calendarWidget.selectedDate().toPyDate()
        selected_time = self.timeEdit.time().toPyTime()
        py_datetime = datetime.combine(selected_date, selected_time)
        datetime_str = py_datetime.strftime('%Y-%m-%d %H:%M:%S')
        qt_datetime = QDateTime.fromString(datetime_str, 'yyyy-MM-dd HH:mm:ss')

        # selected_data = self.samolot.data(self.samolot.currentIndex(), Qt.ItemDataRole.EditRole)

        # self.comboBox_plane.setModelColumn(0)
        # self.comboBox_from.setModelColumn(0)
        # self.comboBox_to.setModelColumn(0)

        query = QSqlQuery()
        query.prepare("INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) VALUES (?, ?, ?, ?)")
        # query.addBindValue(self.comboBox_plane.currentText())
        # query.addBindValue(self.comboBox_from.currentText())
        # query.addBindValue(self.comboBox_to.currentText())
        # query.addBindValue(self.comboBox_plane.currentData(0))
        # query.addBindValue(self.comboBox_from.currentData(0))
        # query.addBindValue(self.comboBox_to.currentData(0))
        # query.addBindValue(self.comboBox_plane.itemData(self.comboBox_plane.currentIndex(),Qt.ItemDataRole.DisplayRole))
        query.addBindValue(self.comboBox_plane.itemData(self.comboBox_plane.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_from.itemData(self.comboBox_from.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_to.itemData(self.comboBox_to.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(qt_datetime)
        if query.exec():
            print(f"Data inserted successfully.")
        else:
            print(f"Error inserting data: {query.lastError().text()}")



# class MultiColumnItemDelegate(QStyledItemDelegate):
#     def displayText(self, value, locale):
#         if isinstance(value, tuple):
#             return f"{value[0]} {value[1]}"  # Modify as needed for your specific columns
#         return super().displayText(value, locale)

# class CustomItemModel(QAbstractItemModel):
#     def __init__(self, query, parent=None):
#         super().__init__(parent)
#         self.query = query

#     def rowCount(self, parent=QModelIndex()):
#         return self.query.size()

#     def columnCount(self, parent=QModelIndex()):
#         return self.query.record().count()

#     def data(self, index, role):
#         if not index.isValid():
#             return None

#         if role == Qt.ItemDataRole.DisplayRole:
#             self.query.seek(index.row())
#             return self.query.value(index.column())  # Use the index column

#         return None
    
#     def index(self, row, column, parent=QModelIndex()):
#         if not self.hasIndex(row, column, parent):
#             return QModelIndex()

#         return self.createIndex(row, column)
    
#     def parent(self, index):
#         return QModelIndex()




# class Flight_dialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         directory = os.path.dirname(os.path.realpath(sys.argv[0]))
#         gui_directory = os.path.join(directory, 'GUI')
#         os.chdir(gui_directory)
#         # os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
#         loadUi("flight_dialog.ui", self)

#         self.samolot = select_samolot()
#         self.lotnisko = select_lotnisko()

#         # osoba = select_osoba()
#         # s = [''.join(str(x)) for x in osoba]
#         # self.comboBox_plane.addItems([''.join(str(x)) for x in self.samolot])
#         # self.comboBox_from.addItems([''.join(str(x)) for x in self.lotnisko])
#         # self.comboBox_to.addItems([''.join(str(x)) for x in self.lotnisko])
#         self.populate_combo_boxes()

#         self.comboBox_from.setCurrentIndex(1538)
#         self.comboBox_to.setCurrentIndex(1538)


#     def add_items_to_combo_box(self, combo_box, items):
#         combo_box.addItems([str(item) for item in items])

#     def populate_combo_boxes(self):
#         self.add_items_to_combo_box(self.comboBox_plane, self.samolot)
#         self.add_items_to_combo_box(self.comboBox_from, self.lotnisko)
#         self.add_items_to_combo_box(self.comboBox_to, self.lotnisko)

#     def get_selected_options(self):
#         self.selected_date = self.calendarWidget.selectedDate().toPyDate()
#         self.selected_time = self.timeEdit.time().toPyTime()

#         return [self.comboBox_plane.currentText(),
#                 self.comboBox_from.currentText(), 
#                 self.comboBox_to.currentText(), 
#                 datetime.combine(self.selected_date, self.selected_time)]






#     # self.insertButton.clicked.connect(self.insert_data_to_database)

#     # def insert_data_to_database(self):
#     #     selected_options = self.get_selected_options()
#     #     osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina = selected_options
#     #     self.insert_ticket_to_database(osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina)

#     # def insert_ticket_to_database(self, osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina):
#     #     try:
#     #         with pg2.connect(**DB_CONFIG) as db:
#     #             cur = db.cursor()
#     #             cur.execute("INSERT INTO bilet (osoba_id, lotnisko_a_id, lotnisko_b_id, klasa, miejsce_id, asystent, data, godzina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#     #                         (osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina))
#     #             db.commit()
#     #             print("Ticket added to the database.")
#     #     except pg2.Error as e:
#     #         print("Error while adding ticket:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Flight_dialog(create_connection())
    window.show()

    # model = QSqlTableModel()
    # query = "SELECT samolot_id, model, ilosc_miejsc FROM samolot"
    # tableView = QTableView()
    # tableView.show()
    # tableView.setModel(model)


    sys.exit(app.exec())
    # db.close()

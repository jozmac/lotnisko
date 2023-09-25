from PyQt6.QtWidgets import QDialog, QApplication, QComboBox
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlQuery, QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt6.QtCore import Qt, QModelIndex, QStringListModel, QAbstractTableModel, QAbstractItemModel, QSize, QDateTime
import sys, os
# from functions import get_data, drop_tables, create_tables
from functions import select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik

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

# class CustomSqlRelationalTableModel(QSqlRelationalTableModel):
#     def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
#         if role == Qt.ItemDataRole.DisplayRole:
#             column_index = index.column()
#             if column_index == 0:  # Customize for columns 2 and 3
#                 data1 = super().data(index.siblingAtColumn(1), Qt.ItemDataRole.EditRole)
#                 data2 = super().data(index.siblingAtColumn(2), Qt.ItemDataRole.EditRole)
#                 return f"{data1} - {data2}"

#         return super().data(index, role)
    
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


class Booking_dialog(QDialog):
    def __init__(self, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        # os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("booking_dialog.ui", self)

        self.db = db

        self.load_combo_boxes()

        self.buttonBox.accepted.connect(self.insert_selected_options)
        # self.buttonBox.rejected.connect(Dialog.reject)

    def load_combo_boxes(self):
        self.comboBox_person.setModel(self.select_osoba())
        self.comboBox_flight.setModel(self.select_lot())
        self.comboBox_seat.setModel(self.select_miejsce())

    def select_osoba(self):
        self.model = CustomSqlRelationalTableModel()
        # self.model.setTable("samolot")
        # self.model.setRelation(0, QSqlRelation("samolot", "samolot_id", "model"))
        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        self.model.setQuery(query, self.db)
        self.model.select()
        # self.comboBox_plane.setItemDelegate(QSqlRelationalDelegate(self.comboBox_plane)) # combobox
        return self.model

    def select_lot(self):
        self.model = CustomSqlRelationalTableModel()
        # self.model.setTable("lot")
        # self.model.setRelation(2, QSqlRelation("lotnisko", "lotnisko_a_id", "city"))
        # self.model.setRelation(3, QSqlRelation("lotnisko", "lotnisko_b_id", "city"))
        # self.model.select()

        query = "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        self.model.setQuery(query, self.db)
        self.model.select()
        return self.model
    
    def select_miejsce(self):
        self.model = CustomSqlRelationalTableModel()
        query = "SELECT miejsce_id, samolot_id FROM miejsce"
        self.model.setQuery(query, self.db)
        self.model.select()
        return self.model
    
    def insert_selected_options(self):
        # self.comboBox_person.setModelColumn(0)
        # self.comboBox_flight.setModelColumn(0)
        # # self.comboBox_class.setModelColumn(0)
        # self.comboBox_seat.setModelColumn(0)
        # # self.comboBox_assistant.setModelColumn(0)

        query = QSqlQuery()
        query.prepare("INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) VALUES (?, ?, ?, ?, ?)")
        # query.addBindValue(self.comboBox_person.currentText())
        # query.addBindValue(self.comboBox_flight.currentText())
        # query.addBindValue(self.comboBox_class.currentText())
        # query.addBindValue(self.comboBox_seat.currentText())
        # query.addBindValue(self.comboBox_assistant.currentText())
        query.addBindValue(self.comboBox_person.itemData(self.comboBox_person.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_flight.itemData(self.comboBox_flight.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_class.itemData(self.comboBox_class.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_seat.itemData(self.comboBox_seat.currentIndex(),Qt.ItemDataRole.EditRole))
        query.addBindValue(self.comboBox_assistant.itemData(self.comboBox_assistant.currentIndex(),Qt.ItemDataRole.EditRole))
        if query.exec():
            print(f"Data inserted successfully.")
        else:
            print(f"Error inserting data: {query.lastError().text()}")


    # def load_combo_boxes(self):
    #     # samolot_query = QSqlQuery("SELECT samolot_id, model, ilosc_miejsc FROM samolot", self.db)
    #     # lotnisko_query = QSqlQuery("SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko", self.db)

    #     # samolot_model = CustomItemModel(samolot_query)
    #     # lotnisko_model = CustomItemModel(lotnisko_query)

    #     # self.comboBox_plane.setModel(samolot_model)
    #     # self.comboBox_from.setModel(lotnisko_model)
    #     # self.comboBox_to.setModel(lotnisko_model)

    #     # self.model = QSqlTableModel()
    #     # self.model = QSqlRelationalTableModel()

    #     # Configure the delegate to work with the samolot model
    #     # self.relational_delegate.setModel(self.samolot)
    #     # self.relational_delegate.setColumn(1)  # Set the column you want to display in the combobox


    #     self.comboBox_person.setModel(self.select_osoba())
    #     # self.comboBox_person.setModelColumn(1)
    #     self.comboBox_flight.setModel(self.select_lot())
    #     # self.comboBox_flight.setModelColumn(1)
    #     self.comboBox_seat.setModel(self.select_miejsce())
    #     # self.comboBox_seat.setModelColumn(1)

    #     # self.comboBox_person.setModel(self.select("SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"))
    #     # self.comboBox_flight.setModel(self.select("SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"))
    #     # self.comboBox_seat.setModel(self.select("SELECT miejsce_id, samolot_id FROM miejsce"))


    # # def select(self, query):
    # #     self.model = CustomSqlRelationalTableModel()
    # #     self.model.setQuery(query, self.db)
    # #     self.model.select()
    # #     return self.model


# class Booking_dialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         directory = os.path.dirname(os.path.realpath(sys.argv[0]))
#         gui_directory = os.path.join(directory, 'GUI')
#         os.chdir(gui_directory)
#         # os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
#         loadUi("booking_dialog.ui", self)

#         # osoba = select_osoba()
#         # s = [''.join(str(x)) for x in osoba]
#         self.comboBox_person.addItems([''.join(str(x)) for x in select_osoba()])
#         self.comboBox_flight.addItems([''.join(str(x)) for x in select_lot()])
#         self.comboBox_seat.addItems([''.join(str(x)) for x in select_miejsce()])



#     def get_selected_options(self):
#         return [self.comboBox_person.currentText(), 
#                 self.comboBox_flight.currentText(), 
#                 self.comboBox_class.currentText(), 
#                 self.comboBox_seat.currentText(), 
#                 self.comboBox_assistant.currentText(),]
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Booking_dialog(create_connection())
    window.show()
    sys.exit(app.exec())

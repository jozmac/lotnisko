from PyQt6.QtWidgets import QDialog, QApplication, QComboBox
from PyQt6.uic import loadUi
from PyQt6.QtSql import (
    QSqlQuery,
    QSqlDatabase,
    QSqlQueryModel,
    QSqlTableModel,
    QSqlRelationalTableModel,
    QSqlRelation,
    QSqlRelationalDelegate,
)
from PyQt6.QtCore import (
    Qt,
    QModelIndex,
    QStringListModel,
    QAbstractTableModel,
    QAbstractItemModel,
    QSize,
    QDateTime,
)

from PyQt6.QtGui import QIcon

import sys, os

from Classes.DatabaseHandler import DatabaseHandler


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
                value = super().data(
                    self.index(row_index, column_index), Qt.ItemDataRole.EditRole
                )
                data += f" - {value}" if data else f"{value}"
            return f"{data}"
        return super().data(index, role)


# class CustomSqlQueryModel(QSqlQueryModel):
#     def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
#         if role == Qt.DisplayRole:
#             row_index = index.row()
#             data = ""
#             for column_index in range(self.columnCount()):
#                 value = super().data(
#                     self.index(row_index, column_index), Qt.ItemDataRole.EditRole
#                 )
#                 data += f" - {value}" if data else str(value)
#             return data
#         return super().data(index, role)


class BookingDialog(QDialog):
    def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.init_gui()

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "booking_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))
        self.load_combo_boxes()
        self.comboBox_flight.currentIndexChanged.connect(self.select_miejsce)

        # self.buttonBox.accepted.connect(self.insert_to_database)
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
        self.model.setQuery(query, self.db_handler.con)
        self.model.select()
        # self.comboBox_plane.setItemDelegate(QSqlRelationalDelegate(self.comboBox_plane)) # combobox
        return self.model

    def select_lot(self):
        self.model = CustomSqlRelationalTableModel()
        # self.model.setTable("lot")
        # self.model.setRelation(2, QSqlRelation("lotnisko", "lotnisko_a_id", "city"))
        # self.model.setRelation(3, QSqlRelation("lotnisko", "lotnisko_b_id", "city"))

        query = (
            "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        )
        self.model.setQuery(query, self.db_handler.con)
        self.model.select()
        return self.model

    def select_miejsce(self):
        self.get_data()

        self.model = QSqlQueryModel(None)

        query = (
            f"SELECT m.miejsce_id "
            f"FROM miejsce m "
            f"LEFT JOIN bilet b ON m.miejsce_id = b.miejsce_id "
            f"WHERE m.samolot_id = (SELECT l.samolot_id FROM lot l WHERE lot_id = {self.flight}) "
            f"AND b.miejsce_id IS NULL "
        )
        self.model.setQuery(query, self.db_handler.con)

        self.comboBox_seat.setModel(self.model)
        return self.model

    def get_data(self):
        self.person = self.comboBox_person.itemData(
            self.comboBox_person.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.flight = self.comboBox_flight.itemData(
            self.comboBox_flight.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.flightclass = self.comboBox_class.itemData(
            self.comboBox_class.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.seat = self.comboBox_seat.itemData(
            self.comboBox_seat.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.assistant = self.comboBox_assistant.itemData(
            self.comboBox_assistant.currentIndex(), Qt.ItemDataRole.EditRole
        )
        # print(
        #     f"{type(self.person)} - {type(self.flight)} - {type(self.flightclass)} - {type(self.seat)} - {type(self.assistant)}"
        # )

    def insert_into_database(self):
        self.get_data()
        self.query = (
            f"INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) "
            f"VALUES ({self.person}, {self.flight}, {self.flightclass}, {self.seat}, {self.assistant})"
        )
        self.db_handler.execute_query(self.query)

    def update_database(self, id: int):
        self.get_data()
        self.query = (
            f"UPDATE bilet SET "
            f"osoba_id = {self.person}, "
            f"lot_id = {self.flight}, "
            f"miejsce_id = {self.seat}, "
            f"asystent = {self.assistant}, "
            f"klasa = {self.flightclass}, "
            f"WHERE bilet_id = {id}"
        )
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_handler = DatabaseHandler()
    db_handler.create_connection()
    window = BookingDialog(db_handler)
    window.show()
    sys.exit(app.exec())

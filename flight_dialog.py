from PyQt6.QtWidgets import (
    QDialog,
    QApplication,
    QComboBox,
    QTableView,
    QStyledItemDelegate,
    QAbstractItemDelegate,
    QStyle,
)
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

from datetime import datetime


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


# class CustomSqlRelationalTableModel(QSqlRelationalTableModel):
#     def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
#         if role == Qt.ItemDataRole.DisplayRole:
#             column_index = index.column()
#             if column_index == 0:
#                 data1 = super().data(index.siblingAtColumn(1), Qt.ItemDataRole.EditRole)
#                 data2 = super().data(index.siblingAtColumn(2), Qt.ItemDataRole.EditRole)
#                 return f"{data1} - {data2}"

#         return super().data(index, role)


class FlightDialog(QDialog):
    def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.init_gui()

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(directory, "GUI", "flight_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("images/airport.png"))

        self.load_combo_boxes()

        self.comboBox_from.setCurrentIndex(1538)
        self.comboBox_to.setCurrentIndex(1538)

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
        self.samolot.setQuery(query, self.db_handler.con)
        self.samolot.select()
        # self.comboBox_plane.setItemDelegate(QSqlRelationalDelegate(self.comboBox_plane)) # combobox

        self.lotnisko = CustomSqlRelationalTableModel()
        query = "SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko"
        self.lotnisko.setQuery(query, self.db_handler.con)
        self.lotnisko.select()

        # self.relational_delegate.setModel(self.samolot)
        # self.relational_delegate.setColumn(1)  # Set the column you want to display in the combobox

        self.comboBox_plane.setModel(self.samolot)
        self.comboBox_from.setModel(self.lotnisko)
        self.comboBox_to.setModel(self.lotnisko)
        # self.comboBox_plane.setModelColumn(1)
        # self.comboBox_plane.setItemDelegate(MultiColumnItemDelegate())

    def get_data(self):
        selected_date = self.calendarWidget.selectedDate().toPyDate()
        selected_time = self.timeEdit.time().toPyTime()
        py_datetime = datetime.combine(selected_date, selected_time)
        datetime_str = py_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.qt_datetime = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss")

        self.plane = self.comboBox_plane.itemData(
            self.comboBox_plane.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.airport_a = self.comboBox_from.itemData(
            self.comboBox_from.currentIndex(), Qt.ItemDataRole.EditRole
        )
        self.airport_b = self.comboBox_to.itemData(
            self.comboBox_to.currentIndex(), Qt.ItemDataRole.EditRole
        )

    def insert_into_database(self):
        self.get_data()
        self.query = (
            f"INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) "
            f"VALUES ({self.plane}, {self.airport_a}, {self.airport_b}, {self.qt_datetime})"
        )
        self.db_handler.execute_query(self.query)

    def update_database(self, id: int):
        self.get_data()
        self.query = (
            f"UPDATE osoba SET "
            f"samolot_id = {self.plane}, "
            f"lotnisko_a_id = {self.airport_a}, "
            f"lotnisko_b_id = {self.airport_b}, "
            f"datetime = {self.qt_datetime} "
            f"WHERE lot_id = {id}"
        )
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_handler = DatabaseHandler()
    db_handler.create_connection()
    window = FlightDialog(db_handler)
    window.show()

    sys.exit(app.exec())

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
    QSortFilterProxyModel,
)

from PyQt6.QtGui import QIcon

import sys, os

from datetime import datetime


class FlightDialog(QDialog):
    def __init__(self, db_handler, row_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.row_id = row_id
        self.init_gui()
        if self.row_id:
            self.set_edit_values()
        self.set_combo_boxes_model_column()

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(directory, "..")
        ui_file = os.path.join(directory, "GUI", "flight_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))

        self.load_combo_boxes()

        self.comboBox_from.setCurrentIndex(1538)
        self.comboBox_to.setCurrentIndex(1538)

    def set_combo_boxes_model_column(self):
        self.comboBox_plane.setModelColumn(1)
        self.comboBox_from.setModelColumn(1)
        self.comboBox_to.setModelColumn(1)

    def load_combo_boxes(self):
        self.model_samolot = QSqlQueryModel()
        query = (
            "SELECT samolot_id AS samolot_id, "
            "samolot_id || ' - ' || model || ' - ' || ilosc_miejsc FROM samolot"
        )

        self.model_samolot.setQuery(query, self.db_handler.con)

        self.model_lotnisko = QSqlQueryModel()
        # query = "SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko"
        query = (
            "SELECT lotnisko_id AS lotnisko_id, "
            "lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country FROM lotnisko"
        )
        self.model_lotnisko.setQuery(query, self.db_handler.con)

        self.comboBox_plane.setModel(self.model_samolot)
        # self.comboBox_from.setModel(self.model_lotnisko)
        # self.comboBox_to.setModel(self.model_lotnisko)

        # self.lineEdit_from.textChanged.connect(
        #     lambda: self.filter_combobox_from(self.lineEdit_from.text())
        # )
        self.lineEdit_from.textChanged.connect(self.filter_combobox_from)
        self.lineEdit_to.textChanged.connect(self.filter_combobox_to)

        self.proxy_model_from = QSortFilterProxyModel()
        self.proxy_model_from.setSourceModel(self.model_lotnisko)
        self.proxy_model_from.setFilterKeyColumn(1)

        self.proxy_model_to = QSortFilterProxyModel()
        self.proxy_model_to.setSourceModel(self.model_lotnisko)
        self.proxy_model_to.setFilterKeyColumn(1)

    def filter_combobox_from(self, text):
        # text = self.lineEdit_from.text()

        # self.proxy_model_from.setDynamicSortFilter(True)

        # Set the filter on the proxy model based on the text entered in the line edit
        # self.proxy_model_from.invalidate()
        # self.proxy_model_from.setFilterFixedString(const QString &pattern)
        # self.proxy_model_from.setFilterRegularExpression(const QString &pattern)
        # self.proxy_model_from.setFilterRegularExpression(const QRegularExpression &regularExpression)
        # self.proxy_model_from.setFilterWildcard(const QString &pattern)
        # self.proxy_model_from.setFilterWildcard(f"*{text}*")
        # self.proxy_model_from.setFilterWildcard(text)
        self.proxy_model_from.setFilterFixedString(text)

        # self.proxy_model_from.setAutoAcceptChildRows(bool accept)
        # self.proxy_model_from.setDynamicSortFilter(bool enable)
        self.proxy_model_from.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        # self.proxy_model_from.setFilterKeyColumn(1)
        # self.proxy_model_from.setFilterRole(int role)
        # self.proxy_model_from.setRecursiveFilteringEnabled(True)
        # self.proxy_model_from.setSortCaseSensitivity(Qt::CaseSensitivity cs)
        # self.proxy_model_from.setSortLocaleAware(bool on)
        # self.proxy_model_from.setSortRole(int role)
        # Set the current index to the first item in the filtered list
        # self.comboBox_from.setCurrentIndex(0)

        # self.proxy_model_from.sort(0, Qt.SortOrder.AscendingOrder)
        self.comboBox_from.setModel(self.proxy_model_from)

    def filter_combobox_to(self, text):
        self.proxy_model_from.setFilterFixedString(text)
        self.proxy_model_from.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        # self.proxy_model_from.setFilterWildcard(f"*{text}*")
        # Set the current index to the first item in the filtered list
        # self.comboBox_to.setCurrentIndex(0)

        self.comboBox_to.setModel(self.proxy_model_to)

    def get_data(self):
        # selected_date = self.calendarWidget.selectedDate().toPyDate()
        # selected_time = self.timeEdit.time().toPyTime()
        # py_datetime = datetime.combine(selected_date, selected_time)
        # datetime_str = py_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # self.qt_datetime = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss")

        selected_date = self.calendarWidget.selectedDate()
        selected_time = self.timeEdit.time()
        self.qt_datetime = QDateTime()
        self.qt_datetime.setDate(selected_date)
        self.qt_datetime.setTime(selected_time)

        # self.plane = self.comboBox_plane.itemData(
        #     self.comboBox_plane.currentIndex(), Qt.ItemDataRole.EditRole
        # )
        # self.airport_a = self.comboBox_from.itemData(
        #     self.comboBox_from.currentIndex(), Qt.ItemDataRole.EditRole
        # )
        # self.airport_b = self.comboBox_to.itemData(
        #     self.comboBox_to.currentIndex(), Qt.ItemDataRole.EditRole
        # )

        self.plane = self.model_samolot.record(
            self.comboBox_plane.currentIndex()
        ).value("samolot_id")
        self.airport_a = self.model_lotnisko.record(
            self.comboBox_from.currentIndex()
        ).value("lotnisko_id")
        self.airport_b = self.model_lotnisko.record(
            self.comboBox_to.currentIndex()
        ).value("lotnisko_id")

        print(
            f"{self.plane} - {self.airport_a} - {self.airport_b} - {self.qt_datetime} - {self.row_id}"
        )
        print(
            f"{type(self.plane)} - {type(self.airport_a)} - {type(self.airport_b)} - {type(self.qt_datetime)} - {type(self.row_id)}"
        )

    def insert_into_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "INSERT INTO lot (samolot_id, lotnisko_a_id, lotnisko_b_id, datetime) VALUES (?, ?, ?, ?)"
        )
        self.query.addBindValue(self.plane)
        self.query.addBindValue(self.airport_a)
        self.query.addBindValue(self.airport_b)
        self.query.addBindValue(self.qt_datetime)
        self.db_handler.execute_query(self.query)

    def set_edit_values(self):
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "SELECT samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot WHERE lot_id = ?"
        )
        self.query.addBindValue(self.row_id)
        self.query.exec()
        self.query.next()
        self.comboBox_plane.setCurrentIndex(
            self.comboBox_plane.findData(self.query.value(0), 0)
        )
        self.comboBox_from.setCurrentIndex(
            self.comboBox_from.findData(self.query.value(1), 0)
        )
        self.comboBox_to.setCurrentIndex(
            self.comboBox_to.findData(self.query.value(2), 0)
        )
        datetime = self.query.value(3)
        date = datetime.date()
        time = datetime.time()
        self.calendarWidget.setSelectedDate(date)
        self.timeEdit.setTime(time)

    def update_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "UPDATE lot SET samolot_id = ?, lotnisko_a_id = ?, lotnisko_b_id = ?, datetime = ? WHERE lot_id = ?"
        )
        self.query.addBindValue(self.plane)
        self.query.addBindValue(self.airport_a)
        self.query.addBindValue(self.airport_b)
        self.query.addBindValue(self.qt_datetime)
        self.query.addBindValue(self.row_id)
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    from run_test_dialog import RunTestDialog

    test_window = RunTestDialog(FlightDialog, row_id=0)

from PyQt6.QtWidgets import QDialog, QApplication, QComboBox, QStyledItemDelegate
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


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def displayText(self, value, locale):
        # index = value.index(self.currentIndex)
        # return index.siblingAtColumn(1).data()
        index: QModelIndex = self.parent.currentIndex()
        id: int = self.model_osoba.data(index.siblingAtColumn(0), 0)
        return id


class BookingDialog(QDialog):
    def __init__(self, db_handler, row_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.row_id = row_id
        self.init_gui()
        if row_id:
            self.set_edit_values()
        self.set_combo_boxes_model_column()
        self.comboBox_flight.currentIndexChanged.connect(self.select_miejsce)

    def init_gui(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(directory, "..")
        ui_file = os.path.join(directory, "GUI", "booking_dialog.ui")
        loadUi(ui_file, self)

        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))
        self.load_combo_boxes()
        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)

    def load_combo_boxes(self):
        # delegate = ComboBoxDelegate()
        # self.comboBox_person.setItemDelegate(delegate)
        self.comboBox_person.setModel(self.select_osoba())
        self.comboBox_flight.setModel(self.select_lot())
        self.comboBox_seat.setModel(self.select_miejsce())

    def set_combo_boxes_model_column(self):
        self.comboBox_person.setModelColumn(1)
        self.comboBox_flight.setModelColumn(1)

    def select_osoba(self):
        self.model_osoba = QSqlQueryModel()
        query = (
            "SELECT osoba_id AS osoba_id, "
            "osoba_id || ' - ' || imie || ' ' || nazwisko AS osoba_data "
            "FROM osoba"
        )
        self.model_osoba.setQuery(query, self.db_handler.con)
        return self.model_osoba

    def select_lot(self):
        self.model_lot = QSqlQueryModel()
        query = (
            "SELECT l.lot_id AS lot_id, "
            "l.lot_id || ' - ' || la.city || ' - ' || lb.city || ' - ' || l.datetime AS lot_data "
            "FROM bilet b "
            "INNER JOIN lot l ON l.lot_id = b.lot_id "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        # query = (
        #     "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        # )
        self.model_lot.setQuery(query, self.db_handler.con)
        return self.model_lot

    def select_miejsce(self):
        # self.get_data()
        self.flight = self.model_lot.record(self.comboBox_flight.currentIndex()).value(
            "lot_id"
        )
        print(f"self.flight - {self.flight}")
        print(f"self.row_id - {self.row_id}")
        self.model_miejsce = QSqlQueryModel(None)
        # query = (
        #     f"SELECT m.miejsce_samolot_id "
        #     f"FROM miejsce m "
        #     f"LEFT JOIN bilet b ON m.miejsce_id = b.miejsce_id "
        #     f"WHERE m.samolot_id = (SELECT l.samolot_id FROM lot l WHERE lot_id = {self.flight}) "
        #     f"AND b.miejsce_id IS NULL"
        # )
        query = (
            f"SELECT m.miejsce_samolot_id "
            f"FROM ( "
            f"    SELECT * "
            f"    FROM miejsce m "
            f"    WHERE m.samolot_id = (SELECT l.samolot_id FROM lot l WHERE l.lot_id = {self.flight}) "
            f") AS m "
            f"LEFT JOIN (SELECT * FROM bilet b WHERE b.lot_id = {self.flight}) AS b ON m.miejsce_samolot_id = b.miejsce_id "
            f"WHERE b.miejsce_id IS NULL "
            f"OR b.bilet_id = {self.row_id}"
        )
        self.model_miejsce.setQuery(query, self.db_handler.con)
        self.comboBox_seat.setModel(self.model_miejsce)
        return self.model_miejsce

    def get_data(self):
        self.flightclass = self.comboBox_class.itemData(
            self.comboBox_class.currentIndex(),
            Qt.ItemDataRole.EditRole,
        )
        self.assistant = self.comboBox_assistant.itemData(
            self.comboBox_assistant.currentIndex(),
            Qt.ItemDataRole.EditRole,
        )

        self.person = self.model_osoba.record(
            self.comboBox_person.currentIndex()
        ).value("osoba_id")
        self.flight = self.model_lot.record(self.comboBox_flight.currentIndex()).value(
            "lot_id"
        )
        self.seat = self.model_miejsce.record(self.comboBox_seat.currentIndex()).value(
            "miejsce_samolot_id"
        )

        # print("=====")
        # print(
        #     f"{self.person} - {self.flight} - {self.flightclass} - {self.seat} - {self.assistant}"
        # )
        # print(
        #     f"{type(self.person)} - {type(self.flight)} - {type(self.flightclass)} - {type(self.seat)} - {type(self.assistant)}"
        # )
        # print("=====")

        # 65 - 4 - Economic - 1741 - No
        # <class 'int'> - <class 'int'> - <class 'str'> - <class 'int'> - <class 'str'>

    def insert_into_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) VALUES (?, ?, ?, ?, ?)"
        )
        self.query.addBindValue(self.person)
        self.query.addBindValue(self.flight)
        self.query.addBindValue(self.flightclass)
        self.query.addBindValue(self.seat)
        self.query.addBindValue(self.assistant)
        self.db_handler.execute_query(self.query)

    def set_edit_values(self):
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "SELECT osoba_id, lot_id, klasa, miejsce_id, asystent FROM bilet WHERE bilet_id = ?"
        )
        self.query.addBindValue(self.row_id)
        self.query.exec()
        self.query.next()
        # index = self.comboBox_person.findData(
        #     self.query.value(0), Qt.ItemDataRole.DisplayRole
        # )

        self.comboBox_person.setCurrentIndex(
            self.comboBox_person.findData(self.query.value(0), 0)
        )
        self.comboBox_flight.setCurrentIndex(
            self.comboBox_flight.findData(self.query.value(1), 0)
        )
        self.comboBox_class.setCurrentIndex(
            self.comboBox_class.findData(self.query.value(2), 0)
        )
        self.comboBox_seat.setCurrentIndex(
            self.comboBox_seat.findData(self.query.value(3), 0)
        )
        # self.seat = self.comboBox_seat.itemData(
        #     self.comboBox_seat.currentIndex(), Qt.ItemDataRole.EditRole
        # )

        print(f"seat_id - {self.query.value(3)}, type - {type(self.query.value(3))}")
        print(
            f"{type(self.query.value(1))}, {type(self.query.value(2))}, {type(self.query.value(3))}, {type(self.query.value(4))}"
        )

        assistant_yes_no = "Yes" if self.query.value(4) else "No"
        self.comboBox_assistant.setCurrentIndex(
            self.comboBox_assistant.findData(assistant_yes_no, 0)
        )

    def update_database(self):
        self.get_data()
        self.query = QSqlQuery(None, self.db_handler.con)
        self.query.prepare(
            "UPDATE bilet SET osoba_id = ?, lot_id = ?, miejsce_id = ?, asystent = ?, klasa = ? WHERE bilet_id = ?"
        )
        self.query.addBindValue(self.person)
        self.query.addBindValue(self.flight)
        self.query.addBindValue(self.seat)
        self.query.addBindValue(self.assistant)
        self.query.addBindValue(self.flightclass)
        self.query.addBindValue(self.row_id)
        self.db_handler.execute_query(self.query)


if __name__ == "__main__":
    from run_test_dialog import RunTestDialog

    test_window = RunTestDialog(BookingDialog, row_id=0)

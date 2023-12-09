from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QDialog, QStyledItemDelegate, QItemDelegate, QApplication
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtSql import QSqlQuery, QSqlQueryModel
from PyQt6.uic import loadUiType
import os

import pandas as pd

# def display_model(model):
#     from PyQt6.QtWidgets import QTableView
#     import sys

#     # app = QApplication(sys.argv)
#     table_view = QTableView()
#     table_view.setModel(model)
#     table_view.show()
#     # table_view.exec()
#     # sys.exit(app.exec())


class DisplayModel(QDialog):
    def __init__(self, model):
        super().__init__()

        from PyQt6.QtWidgets import QTableView, QVBoxLayout

        self.setWindowTitle("Display Model")
        table_view = QTableView()
        table_view.setModel(model)
        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.exec()


class DisplayWidgets(QDialog):
    def __init__(self, *widgets):
        super().__init__()

        from PyQt6.QtWidgets import QVBoxLayout

        layout = QVBoxLayout(self)

        for widget in widgets:
            layout.addWidget(widget)

        self.exec()


def qtmodel_to_dataframe(qt_model):
    """
    Convert a PyQt model to a Pandas DataFrame.

    Parameters:
    - qt_model: The PyQt model to be converted.

    Returns:
    - pd.DataFrame: The Pandas DataFrame containing the data from the PyQt model.
    """
    import pandas as pd

    rows = qt_model.rowCount()
    columns = qt_model.columnCount()

    headers = [
        qt_model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        for col in range(columns)
    ]

    df = pd.DataFrame(columns=headers)

    for row in range(rows):
        data = [qt_model.data(qt_model.index(row, col)) for col in range(columns)]
        df.loc[row] = data

    return df


def dataframe_to_qtmodel(dataframe):
    """
    Convert a Pandas DataFrame to a PyQt model.

    Parameters:
    - dataframe: The Pandas DataFrame to be converted.

    Returns:
    - QStandardItemModel: The PyQt QStandardItemModel containing the data from the DataFrame.
    """
    from PyQt6.QtGui import QStandardItem, QStandardItemModel

    model = QStandardItemModel()

    model.setHorizontalHeaderLabels(dataframe.columns)

    for row in range(dataframe.shape[0]):
        items = [
            QStandardItem(str(dataframe.iloc[row, col]))
            for col in range(dataframe.shape[1])
        ]
        model.appendRow(items)

    return model


def print_qtmodel(qtmodel):
    print(qtmodel_to_dataframe(qtmodel))


# class SeatModel(QSqlQueryModel):
#     def __init__(self, parent=None, seat_columns_count=6, *args, **kwargs):
#         self.seat_columns_count = seat_columns_count
#         super().__init__(parent, *args, **kwargs)

#     def columnCount(self, parent=None):
#         return 2

#     def data(self, index, role=Qt.ItemDataRole.DisplayRole):
#         if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
#             if index.column() == 1:
#                 seat_id = self.data(self.index(index.row(), 0), role)
#                 row_number = int(seat_id / self.seat_columns_count) + 1
#                 seat_letter = chr((seat_id - 1) % self.seat_columns_count + 65)
#                 seat_name = f"{seat_id} - {row_number}{seat_letter}"
#                 return seat_name
#             else:
#                 return super().data(index, role)
#         return None


UI_PATH = os.path.join(os.path.dirname(__file__), "..", "GUI", "booking_dialog.ui")
FORM_CLASS, BASE_CLASS = loadUiType(UI_PATH)


class BookingDialog(QDialog, FORM_CLASS):
    def __init__(self, db_handler, row_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.row_id = row_id
        self._init_ui()

    def _init_ui(self):
        self.setupUi(self)
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))
        self._load_combo_boxes()
        if self.row_id:
            self._set_edit_values()
        self._set_combo_boxes_model_column()
        self.comboBox_flight.currentIndexChanged.connect(self._select_miejsce)
        # self.buttonBox.accepted.connect(self.insert_to_database)
        # self.buttonBox.rejected.connect(Dialog.reject)

    def _load_combo_boxes(self):
        self.comboBox_person.setModel(self._select_osoba())
        self.comboBox_flight.setModel(self._select_lot())
        # self.comboBox_seat.setModel(self._select_miejsce())
        self._select_miejsce()
        # DisplayModel(self.model_osoba)
        # DisplayModel(self.model_lot)
        # DisplayModel(self.model_miejsce)
        df = qtmodel_to_dataframe(self.model_osoba)
        # data = {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
        data = df
        df = pd.DataFrame(data)
        qt_model = dataframe_to_qtmodel(df)
        DisplayModel(qt_model)

        # from PyQt6.QtWidgets import QTableView

        # table_view1 = QTableView()
        # table_view1.setModel(self.model_osoba)
        # table_view2 = QTableView()
        # table_view2.setModel(qt_model)
        # DisplayWidgets(table_view1, table_view2)
        print_qtmodel(qt_model)

    def _set_combo_boxes_model_column(self):
        self.comboBox_person.setModelColumn(1)
        self.comboBox_flight.setModelColumn(1)
        self.comboBox_seat.setModelColumn(1)

    def _select_osoba(self):
        self.model_osoba = QSqlQueryModel()
        query = (
            "SELECT osoba_id, "
            "osoba_id || ' - ' || imie || ' ' || nazwisko AS osoba_data "
            "FROM osoba"
        )
        # query = (
        #     "SELECT osoba_id || ' - ' || imie || ' ' || nazwisko AS osoba_data, "
        #     "osoba_id "
        #     "FROM osoba"
        # )
        self.model_osoba.setQuery(query, self.db_handler.con)
        return self.model_osoba

    def _select_lot(self):
        self.model_lot = QSqlQueryModel()
        query = (
            "SELECT l.lot_id, "
            "l.lot_id || ' - ' || la.city || ' - ' || lb.city || ' - ' || l.datetime AS lot_data "
            "FROM lot l "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        # query = (
        #     "SELECT l.lot_id || ' - ' || la.city || ' - ' || lb.city || ' - ' || l.datetime AS lot_data, "
        #     # "SELECT l.lot_id || ' - ' || l.lotnisko_a_id || ' - ' || l.lotnisko_b_id || ' - ' || l.datetime AS lot_data, "
        #     "l.lot_id "
        #     "FROM lot l "
        #     "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
        #     "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        # )
        # query = (
        #     "SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot"
        # )
        self.model_lot.setQuery(query, self.db_handler.con)
        return self.model_lot

    def _select_miejsce(self):
        self.flight = self.model_lot.record(self.comboBox_flight.currentIndex()).value(
            "lot_id"
        )

        # self.flight = self.model_lot.record(
        #     self.model_lot.match(
        #         self.model_lot.index(0, 0),
        #         Qt.ItemDataRole.DisplayRole,
        #         self.comboBox_flight.currentText(),
        #         1,
        #         Qt.MatchFlag.MatchContains,
        #     )[0].row()
        # ).value("lot_id")

        print(
            f"_select_miejsce: self.comboBox_flight.currentText() == {self.comboBox_flight.currentText()}"
        )
        print(f"_select_miejsce: self.flight == {self.flight}")

        # print(f"self.flight - {self.flight}")
        # print(f"self.row_id - {self.row_id}")

        self.model_miejsce = QSqlQueryModel()

        query = (
            "WITH lot_samolot_id AS ("
            "    SELECT l.samolot_id "
            "    FROM lot l "
            f"    WHERE l.lot_id = {self.flight}"
            "), "
            "lot_samolot_miejsce AS ("
            "    SELECT * "
            "    FROM miejsce m "
            "    WHERE m.samolot_id = (SELECT samolot_id FROM lot_samolot_id) "
            ") "
            "SELECT m.miejsce_samolot_id, m.miejsce_samolot_name "
            "FROM lot_samolot_miejsce m "
            "LEFT JOIN ("
            "    SELECT * "
            "    FROM bilet b "
            f"    WHERE b.lot_id = {self.flight} "
            ") AS b ON m.miejsce_samolot_id = b.miejsce_id "
            "WHERE b.miejsce_id IS NULL "
            f"OR b.bilet_id = {self.row_id}"
        )

        print(
            f"_select_miejsce: miejsce_samolot_id query values: row_id: {self.row_id}, flight_id: {self.flight}"
        )

        self.model_miejsce.setQuery(query, self.db_handler.con)
        self.comboBox_seat.setModel(self.model_miejsce)
        return self.model_miejsce

    def _set_edit_values(self):
        self.query = QSqlQuery()
        self.query.prepare(
            "SELECT osoba_id, lot_id, klasa, miejsce_id, asystent FROM bilet WHERE bilet_id = ?"
        )
        self.query.addBindValue(self.row_id)
        self.query.exec()
        self.query.next()

        # data = {
        #     "osoba_id": self.query.value(0),
        #     "lot_id": self.query.value(1),
        #     "klasa": self.query.value(2),
        #     "miejsce_id": self.query.value(3),
        #     "asystent": self.query.value(4),
        # }
        # print(f"_set_edit_values: {data}")

        # index = self.comboBox_person.findData(
        #     self.query.value(0), Qt.ItemDataRole.DisplayRole
        # )

        self.comboBox_person.setCurrentIndex(
            self.comboBox_person.findData(
                self.query.value(0),
                Qt.ItemDataRole.DisplayRole,
                Qt.MatchFlag.MatchExactly,
            )
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

        # print(f"________________ {self.comboBox_seat.findData(self.query.value(3), 0)}")

        # osoba_data = self.model_osoba.record(
        #     self.model_osoba.match(
        #         self.model_osoba.index(0, 1),
        #         Qt.ItemDataRole.DisplayRole,
        #         self.query.value(0),
        #         1,
        #         Qt.MatchFlag.MatchContains,
        #     )[0].row()
        # ).value("osoba_data")

        # lot_data = self.model_lot.record(
        #     self.model_lot.match(
        #         self.model_lot.index(0, 1),
        #         Qt.ItemDataRole.DisplayRole,
        #         self.query.value(1),
        #         1,
        #         Qt.MatchFlag.MatchContains,
        #     )[0].row()
        # ).value("lot_data")

        # miejsce_data = self.model_miejsce.record(
        #     self.model_miejsce.match(
        #         self.model_miejsce.index(0, 1),
        #         Qt.ItemDataRole.DisplayRole,
        #         self.query.value(3),
        #         1,
        #         Qt.MatchFlag.MatchContains,
        #     )[0].row()
        # ).value("miejsce_data")

        # self.comboBox_person.setCurrentIndex(
        #     self.comboBox_person.findData(osoba_data, 0)
        # )
        # self.comboBox_flight.setCurrentIndex(self.comboBox_flight.findData(lot_data, 0))
        # self.comboBox_seat.setCurrentIndex(self.comboBox_seat.findData(miejsce_data, 0))

        # self.seat = self.comboBox_seat.itemData(
        #     self.comboBox_seat.currentIndex(), Qt.ItemDataRole.EditRole
        # )

        # print(f"seat_id - {self.query.value(3)}, type - {type(self.query.value(3))}")
        # print(
        #     f"{type(self.query.value(1))}, {type(self.query.value(2))}, {type(self.query.value(3))}, {type(self.query.value(4))}"
        # )

        assistant_yes_no = "Yes" if self.query.value(4) else "No"
        self.comboBox_assistant.setCurrentIndex(
            self.comboBox_assistant.findData(assistant_yes_no, 0)
        )

    # def match_data_in_model(self, model, match_column: int, data, return_value_column: str):
    #     return model.record(
    #         model.match(
    #             model.index(0, match_column),
    #             Qt.ItemDataRole.DisplayRole,
    #             data,
    #             1,
    #             Qt.MatchFlag.MatchContains,
    #         )[0].row()
    #     ).value(f"{return_value_column}")

    def _get_data(self):
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

        # data = {
        #     "osoba_id": self.person,
        #     "lot_id": self.flight,
        #     "miejsce_samolot_id": self.seat,
        #     "flightclass": self.flightclass,
        #     "assistant": self.assistant,
        # }
        # print(f"_get_data: {data}")

        # model_miejsce_current_index = self.comboBox_seat.currentIndex()
        # model_miejsce_record = self.model_miejsce.record(
        #     self.comboBox_seat.currentIndex()
        # )
        # print(model_miejsce_record)
        # print(model_miejsce_current_index)

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
        self._get_data()
        # self.query = QSqlQuery(None, self.db_handler.con)
        self.query = QSqlQuery()
        self.query.prepare(
            "INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) VALUES (?, ?, ?, ?, ?)"
        )
        self.query.addBindValue(self.person)
        self.query.addBindValue(self.flight)
        self.query.addBindValue(self.flightclass)
        self.query.addBindValue(self.seat)
        self.query.addBindValue(self.assistant)
        self.db_handler.execute_query(self.query)

    def update_database(self):
        self._get_data()
        # self.query = QSqlQuery(None, self.db_handler.con)
        self.query = QSqlQuery()
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

    # def display_model(self, model):
    #     from PyQt6.QtWidgets import QTableView

    #     table_view = QTableView()
    #     table_view.show()
    #     table_view.setModel(model)


if __name__ == "__main__":
    from run_test_dialog import RunTestDialog

    test_window = RunTestDialog(BookingDialog, row_id=15)
    # test_window.display_model(test_window.model_miejsce)
    # test_window.display_model(test_window.model_lot)
    # test_window.display_model(test_window.model_lot)

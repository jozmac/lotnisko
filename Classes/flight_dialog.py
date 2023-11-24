from PyQt6.QtCore import Qt, QDateTime, QSortFilterProxyModel
from PyQt6.QtWidgets import QDialog, QCompleter
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlQuery, QSqlQueryModel
from PyQt6.uic import loadUiType
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "GUI", "flight_dialog.ui")
FORM_CLASS, BASE_CLASS = loadUiType(UI_PATH)


class FlightDialog(QDialog, FORM_CLASS):
    def __init__(self, db_handler, row_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.db_handler = db_handler
        self.row_id = row_id
        self.init_gui()
        if self.row_id:
            self.set_edit_values()
        self.set_combo_boxes_model_column()

    def init_gui(self):
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))

        self.load_combo_boxes()

        # self.comboBox_from.setCurrentIndex(1538)
        # self.comboBox_to.setCurrentIndex(1538)

    def set_combo_boxes_model_column(self):
        self.comboBox_plane.setModelColumn(1)
        # self.comboBox_from.setModelColumn(1)
        # self.comboBox_to.setModelColumn(1)

    def load_combo_boxes(self):
        self.model_samolot = QSqlQueryModel()
        query = (
            "SELECT samolot_id AS samolot_id, "
            "samolot_id || ' - ' || model || ' - ' || ilosc_miejsc FROM samolot"
        )

        self.model_samolot.setQuery(query, self.db_handler.con)

        self.model_lotnisko = QSqlQueryModel()
        # query = "SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko"
        # query = (
        #     "SELECT lotnisko_id AS lotnisko_id, "
        #     "lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country AS lotnisko_data FROM lotnisko"
        # )
        # query = "SELECT lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country AS lotnisko_data FROM lotnisko"
        query = "SELECT lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country AS lotnisko_data, lotnisko_id FROM lotnisko"

        self.model_lotnisko.setQuery(query, self.db_handler.con)

        # self.model_lotnisko_from = QSqlQueryModel()
        # query = "SELECT lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country AS lotnisko_data FROM lotnisko"
        # self.model_lotnisko_from.setQuery(query, self.db_handler.con)

        # self.model_lotnisko_to = QSqlQueryModel()
        # query = "SELECT lotnisko_id || ' - ' || icao_code || ' - ' || name || ' - ' || city || ' - ' || country AS lotnisko_data FROM lotnisko"
        # self.model_lotnisko_from.setQuery(query, self.db_handler.con)

        self.comboBox_plane.setModel(self.model_samolot)
        # self.comboBox_from.setModel(self.model_lotnisko)
        # self.comboBox_to.setModel(self.model_lotnisko)

        # self.lineEdit_from.textChanged.connect(
        #     lambda: self.filter_combobox_from(self.lineEdit_from.text())
        # )

        # self.lineEdit_from.textChanged.connect(self.filter_combobox_from)
        # self.lineEdit_to.textChanged.connect(self.filter_combobox_to)

        # column_index = self.model_lotnisko.record().indexOf("lotnisko_data")
        # words = [
        #     self.model_lotnisko.record(i).value(column_index)
        #     for i in range(self.model_lotnisko.rowCount())
        # ]
        # completer = QCompleter(words, self)
        self.completer_from = QCompleter(self.model_lotnisko, self)
        self.completer_from.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer_from.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_to = QCompleter(self.model_lotnisko, self)
        self.completer_to.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer_to.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.lineEdit_from.setCompleter(self.completer_from)
        self.lineEdit_to.setCompleter(self.completer_to)

        # self.proxy_model_from = QSortFilterProxyModel()
        # self.proxy_model_from.setSourceModel(self.model_lotnisko)
        # self.proxy_model_from.setFilterKeyColumn(1)

        # self.proxy_model_to = QSortFilterProxyModel()
        # self.proxy_model_to.setSourceModel(self.model_lotnisko)
        # self.proxy_model_to.setFilterKeyColumn(1)

    # def filter_combobox_from(self, text):
    #     # text = self.lineEdit_from.text()

    #     # self.proxy_model_from.setDynamicSortFilter(True)

    #     # Set the filter on the proxy model based on the text entered in the line edit
    #     # self.proxy_model_from.invalidate()
    #     # self.proxy_model_from.setFilterFixedString(const QString &pattern)
    #     # self.proxy_model_from.setFilterRegularExpression(const QString &pattern)
    #     # self.proxy_model_from.setFilterRegularExpression(const QRegularExpression &regularExpression)
    #     # self.proxy_model_from.setFilterWildcard(const QString &pattern)
    #     # self.proxy_model_from.setFilterWildcard(f"*{text}*")
    #     # self.proxy_model_from.setFilterWildcard(text)
    #     self.proxy_model_from.setFilterFixedString(text)

    #     # self.proxy_model_from.setAutoAcceptChildRows(bool accept)
    #     # self.proxy_model_from.setDynamicSortFilter(bool enable)
    #     self.proxy_model_from.setFilterCaseSensitivity(
    #         Qt.CaseSensitivity.CaseInsensitive
    #     )
    #     # self.proxy_model_from.setFilterKeyColumn(1)
    #     # self.proxy_model_from.setFilterRole(int role)
    #     # self.proxy_model_from.setRecursiveFilteringEnabled(True)
    #     # self.proxy_model_from.setSortCaseSensitivity(Qt::CaseSensitivity cs)
    #     # self.proxy_model_from.setSortLocaleAware(bool on)
    #     # self.proxy_model_from.setSortRole(int role)
    #     # Set the current index to the first item in the filtered list
    #     # self.comboBox_from.setCurrentIndex(0)

    #     # self.proxy_model_from.sort(0, Qt.SortOrder.AscendingOrder)
    #     self.comboBox_from.setModel(self.proxy_model_from)

    # def filter_combobox_to(self, text):
    #     self.proxy_model_from.setFilterFixedString(text)
    #     self.proxy_model_from.setFilterCaseSensitivity(
    #         Qt.CaseSensitivity.CaseInsensitive
    #     )
    #     # self.proxy_model_from.setFilterWildcard(f"*{text}*")
    #     # Set the current index to the first item in the filtered list
    #     # self.comboBox_to.setCurrentIndex(0)

    #     self.comboBox_to.setModel(self.proxy_model_to)

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
        # self.airport_a = self.model_lotnisko.record(
        #     self.comboBox_from.currentIndex()
        # ).value("lotnisko_id")
        # self.airport_b = self.model_lotnisko.record(
        #     self.comboBox_to.currentIndex()
        # ).value("lotnisko_id")

        self.airport_a = self.model_lotnisko.record(
            self.completer_from.currentIndex()
        ).value("lotnisko_id")
        self.airport_b = self.model_lotnisko.record(
            self.completer_to.currentIndex()
        ).value("lotnisko_id")

        # print(
        #     f"{self.plane} - {self.airport_a} - {self.airport_b} - {self.qt_datetime} - {self.row_id}"
        # )
        # print(
        #     f"{type(self.plane)} - {type(self.airport_a)} - {type(self.airport_b)} - {type(self.qt_datetime)} - {type(self.row_id)}"
        # )

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
        # self.comboBox_from.setCurrentIndex(
        #     self.comboBox_from.findData(self.query.value(1), 0)
        # )
        # self.comboBox_to.setCurrentIndex(
        #     self.comboBox_to.findData(self.query.value(2), 0)
        # )

        lotnisko_data_from = self.model_lotnisko.record(
            self.model_lotnisko.match(
                self.model_lotnisko.index(0, 1),
                Qt.ItemDataRole.DisplayRole,
                self.query.value(1),
                1,
                Qt.MatchFlag.MatchContains,
            )[0].row()
        ).value("lotnisko_data")

        lotnisko_data_to = self.model_lotnisko.record(
            self.model_lotnisko.match(
                self.model_lotnisko.index(0, 1),
                Qt.ItemDataRole.DisplayRole,
                self.query.value(2),
                1,
                Qt.MatchFlag.MatchContains,
            )[0].row()
        ).value("lotnisko_data")

        # variant = self.model_lotnisko.match(
        #     self.model_lotnisko.index(0, 1),
        #     Qt.ItemDataRole.DisplayRole,
        #     self.query.value(1),
        #     1,
        #     Qt.MatchFlag.MatchContains,
        # )
        # print(variant[0])
        # print(variant[0].row())
        # print(variant[0].column())

        self.lineEdit_from.setText(str(lotnisko_data_from))
        self.lineEdit_to.setText(str(lotnisko_data_to))

        # self.lineEdit_from.setText(str(self.query.value(1)))
        # self.lineEdit_to.setText(str(self.query.value(2)))

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

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QTableView,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QVariant, QAbstractTableModel

# from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
# from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import requests


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return QVariant()

    # def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
    #     if role == Qt.ItemDataRole.DisplayRole:
    #         if orientation == Qt.Orientation.Horizontal:
    #             return str(self._data.columns[section])
    #         elif orientation == Qt.Orientation.Vertical:
    #             return str(self._data.index[section])
    #     return QVariant()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.hbox_layout = QHBoxLayout()

        self.line_edit = QLineEdit(self)
        self.line_edit.setText("osoba")
        self.hbox_layout.addWidget(self.line_edit)

        self.button = QPushButton("Get Data", self)
        self.button.clicked.connect(self.get_data)
        self.hbox_layout.addWidget(self.button)
        self.layout.addLayout(self.hbox_layout)

        self.table_view = QTableView(self)
        self.layout.addWidget(self.table_view)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

    def get_data(self):
        url = f"http://127.0.0.1:5000/api/data/{self.line_edit.text()}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()  # list of lists (list of rows)
            self.display_data(data)
            self.label.setText(
                f"Status code: {response.status_code} - {self.get_status_info(response.status_code)}"
            )

        except requests.RequestException as e:
            self.label.setText(str(e))

    def get_status_info(self, status_code):
        if 100 <= status_code < 200:
            return "Informational response"
        elif 200 <= status_code < 300:
            return "Successful response"
        elif 300 <= status_code < 400:
            return "Redirection message"
        elif 400 <= status_code < 500:
            return "Client error response"
        elif 500 <= status_code < 600:
            return "Server error response"
        else:
            return "Unknown status code"

    def display_data(self, data):
        # model = QStandardItemModel(len(data), len(data[0]), self)
        # for row_idx, row in enumerate(data):
        #     for col_idx, value in enumerate(row):
        #         item = QStandardItem(str(value))
        #         model.setItem(row_idx, col_idx, item)
        model = CustomTableModel(data)
        self.table_view.setModel(model)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.setGeometry(100, 100, 400, 200)
    window.setWindowTitle("PyQt6 Client")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    # self.central_widget = QWidget(self)
    # self.setCentralWidget(self.central_widget)

    # self.layout = QVBoxLayout(self.central_widget)

    # self.label = QLabel(self)
    # self.layout.addWidget(self.label)

    # self.table_view = QTableView(self)
    # self.layout.addWidget(self.table_view)

    # self.button = QPushButton("Get Data", self)
    # self.button.clicked.connect(self.get_data)
    # self.layout.addWidget(self.button)

    # self.manager = QNetworkAccessManager(self)
    # self.manager.finished.connect(self.handle_response)

    # def get_data(self):
    #     url = QUrl("http://127.0.0.1:5000/api/data")
    #     request = QNetworkRequest(url)
    #     self.manager.get(request)

    # def handle_response(self, reply):
    #     if reply.error() == QNetworkReply.NetworkError.NoError:
    #         data = reply.readAll().data().decode("utf-8")
    #         # data = reply.json()
    #         # self.table_view.setModel(data)
    #         # self.label.setText(data)

    #         model = QStandardItemModel(len(data), len(data[0]), self)

    #         for row_idx, row in enumerate(data):
    #             for col_idx, value in enumerate(row):
    #                 item = QStandardItem(str(value))
    #                 model.setItem(row_idx, col_idx, item)

    #         self.table_view.setModel(model)

    #     else:
    #         self.label.setText("Error: {}".format(reply.errorString()))

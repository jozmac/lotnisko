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
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
import requests  # HTTP library


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
            self.label.setText(f"Status: {self.get_status_info(response.status_code)}")

        except requests.RequestException as e:
            self.label.setText(str(e))

    def get_status_info(self, status_code):
        status_ranges = {
            (100, 200): "Informational response",
            (200, 300): "Successful response",
            (300, 400): "Redirection message",
            (400, 500): "Client error response",
            (500, 600): "Server error response",
        }

        for code_range, info in status_ranges.items():
            if code_range[0] <= status_code < code_range[1]:
                return info

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

from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import sys

from functions import get_data, drop_tables, create_tables

# drop_tables()
# create_tables()
osoba, lotnisko, samolot = get_data()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("C:\PycharmProjects\lotnisko\lotnisko_combo.ui", self)

        # self.pushButton_pasazerowie.clicked.connect(lambda: self.load_data(osoba))
        # self.pushButton_lotnisko.clicked.connect(lambda: self.load_data(lotnisko))
        # self.pushButton_loty.clicked.connect(lambda: self.load_data(samolot))

        self.tableWidget.cellClicked.connect(self.get_clicked_cell)

    def load_data(self, table_name):
        self.table_name = table_name
        self.tableWidget.setRowCount(len(table_name))
        self.tableWidget.setColumnCount(len(table_name[0]))
        for row_number, row_data in enumerate(table_name):
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column, QTableWidgetItem(str(data)))
        self.tableWidget.setHorizontalHeaderLabels(["id", "model", "ilosc_miejsc"])

    def get_clicked_cell(self, row, column):
        print(f"Clicked cell: [{row}, {column}] {self.table_name[0][0]}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

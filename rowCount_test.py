import sys

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    tableView = QTableView()

    model = QStandardItemModel()
    model.setItem(0, 0, QStandardItem("Row 1, Column 1"))
    model.setItem(0, 1, QStandardItem("Row 1, Column 2"))
    model.setItem(1, 0, QStandardItem("Row 2, Column 1"))
    model.setItem(1, 1, QStandardItem("Row 2, Column 2"))

    tableView.setModel(model)
    window.setCentralWidget(tableView)

    window.show()

    row_count = tableView.model().rowCount()
    print("Number of rows in TableView:", row_count)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

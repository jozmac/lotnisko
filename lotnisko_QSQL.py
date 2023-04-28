from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.uic import loadUi
# from PyQt6.QtCore import QCoreApplication
from PyQt6 import QtCore
import psycopg2 as pg2
import sys

# import PyQt6
# print(PyQt6.__file__)
# _translate = QtCore.QCoreApplication.translate


# try:
#     mydb = pg2.connect(
#         database="lotnisko",
#         host="localhost",
#         user='postgres',
#         password='password',
#         port='5432'
#     )
#     print(mydb)
#     cursor = mydb.cursor()
# except pg2.Error as e:
#     # self.label_result.setText("Error")
#     print(e)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("lotnisko1.ui", self)

        self.model1 = QSqlTableModel()
        self.model1.setTable('samolot')
        self.model1.select()

        self.model2 = QSqlTableModel()
        self.model2.setTable('lotnisko')
        self.model2.select()

        self.model3 = QSqlTableModel()
        self.model3.setTable('osoba')
        self.model3.select()

        self.tableView = QTableView()
        # self.view = QTableView()

        # Set the initial model for the table view
        # self.tableView.setModel(self.model1)

        # Set up the button connections
        self.pushButton_loty.clicked.connect(lambda: self.tableView.setModel(self.model1))
        self.pushButton_lotnisko.clicked.connect(lambda: self.tableView.setModel(self.model2))
        self.pushButton_pasazerowie.clicked.connect(lambda: self.tableView.setModel(self.model3))


def createConnection():
    # https: // wiki.qt.io/How_to_load_a_sql_driver_correctly
    db = QSqlDatabase.addDatabase("QPSQL")
    # print("Available drivers", db.drivers())
    db.setHostName("localhost")
    db.setDatabaseName("lotnisko")
    db.setUserName("postgres")
    db.setPassword("password")

    # db.open()
    # db.setPort(5432)
    if not db.open():
        print("Database Error: %s" % db.lastError().databaseText())
        sys.exit(1)
        return False
    return True

if __name__ == "__main__":
    if createConnection():
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec())

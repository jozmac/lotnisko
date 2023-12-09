# class HelloContextManager:
#     def __enter__(self):
#         print("Entering the context...")
#         return "Hello, World!"

#     def __exit__(self, exc_type, exc_value, exc_tb):
#         print("Leaving the context...")
#         print(exc_type, exc_value, exc_tb, sep="\n")


# with HelloContextManager() as hello:
#     print(hello)


import pytest
from pytest import MonkeyPatch

from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
import sys, os

import main
from main import MainWindow
from classes.booking_dialog import BookingDialog
from classes.flight_dialog import FlightDialog
from classes.person_dialog import PersonDialog
from classes.initialize_database import InitializeDatabase
from classes.database_handler import DatabaseHandler


class AppContextmManager:
    def __enter__(self):
        print("Creating the widget...")
        self.application = QApplication(sys.argv)
        self.db_handler = DatabaseHandler(database_name="lotnisko")
        self.db_handler.create_connection_sqlite()
        self.widget = MainWindow(self.db_handler)
        self.widget.show()

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Closing the widget...")
        self.widget.close()
        # sys.exit(self.application.exec())


with AppContextmManager() as app:
    print("Test run.")

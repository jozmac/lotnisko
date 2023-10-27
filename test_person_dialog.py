import sys
import pytest
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from unittest.mock import Mock, patch

from person_dialog import PersonDialog
from Classes.DatabaseHandler import DatabaseHandler


def test_insert_into_database():
    db_handler = Mock()
    application = QApplication(sys.argv)
    window = PersonDialog(db_handler)

    window.lineEdit_imie.setText("Jan")
    window.lineEdit_nazwisko.setText("Kowalski")
    window.lineEdit_stanowisko.setText("Pilot")

    window.insert_into_database()

    assert window.query == (
        "INSERT INTO osoba (imie, nazwisko, stanowisko) "
        "VALUES ('Jan', 'Kowalski', 'Pilot');"
    )


def test_update_database():
    db_handler = Mock()
    application = QApplication(sys.argv)
    window = PersonDialog(db_handler)

    window.lineEdit_imie.setText("Jan")
    window.lineEdit_nazwisko.setText("Kowalski")
    window.lineEdit_stanowisko.setText("Pilot")

    window.update_database(1)

    assert window.query == (
        "UPDATE osoba SET "
        "imie = 'Jan', "
        "nazwisko = 'Kowalski', "
        "stanowisko = 'Pilot' "
        "WHERE osoba_id = '1';"
    )


# app = QApplication(sys.argv)
# db_handler = Mock()
# # db_handler = DatabaseHandler()
# # db_handler.create_connection()
# window = PersonDialog(db_handler)

# window.lineEdit_imie.setText("John")
# window.lineEdit_nazwisko.setText("Doe")
# # window.lineEdit_stanowisko.setText("Manager")
# window.lineEdit_stanowisko.setText("Pilot2")

# window.insert_into_database()
# # window.db_handler.execute_query(window.query)

# print(window.query)

# window.show()
# sys.exit(app.exec())


# @pytest.fixture
# def app():
#     # application = QApplication(sys.argv)
#     db_handler = Mock()
#     db_handler.create_connection()
#     widget = PersonDialog(db_handler)
#     return widget
#     # yield widget
#     # widget.close()
#     # sys.exit(application.exec())


# # # @pytest.fixture
# # def test_database_connection(app):
# #     assert app.db_handler.db.isOpen()


# def test_test():
#     print("testing...")
#     assert True


# You can similarly create a test case for `update_database`.

if __name__ == "__main__":
    # sys.argv.append("--qt=qt6")
    sys.exit(pytest.main(["-vv", __file__]))

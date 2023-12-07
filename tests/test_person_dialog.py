import sys, os
import pytest

from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlQuery

from unittest.mock import Mock, patch

from classes.person_dialog import PersonDialog
from classes.database_handler import DatabaseHandler
from classes.initialize_database import InitializeDatabase

# import sqlite3


class FakeDatabaseHandler(DatabaseHandler):
    def execute_query(self, query):
        print("pass query execution")
        pass


# python -m tests.test_person_dialog


# class HelloContextManager:
#     def __enter__(self):
#         print("Entering the context...")
#         return "Hello, World!"

#     def __exit__(self, exc_type, exc_value, exc_tb):
#         print("Leaving the context...")
#         print(exc_type, exc_value, exc_tb, sep="\n")


# with HelloContextManager() as hello:
#     print(hello)


# class DbConn:
#     def __enter__(self):
#         # print("Creating database connection...")
#         self.db_handler = FakeDatabaseHandler()
#         self.db_handler.create_connection_sqlite()
#         return self.db_handler

#     def __exit__(self, exc_type, exc_value, exc_tb):
#         # print("Closing database connection...")
#         print(exc_type, exc_value, exc_tb, sep="\n")
#         self.db_handler.close_connection()


@pytest.fixture
def window():
    # db_handler = Mock()
    # dbinit = InitializeDatabase()
    # dbinit.initialize_sqlite()
    db_handler = DatabaseHandler("data/lotnisko.sqlite3")
    # db_handler = FakeDatabaseHandler()
    # db_handler.create_connection()
    db_handler.create_connection_sqlite()
    application = QApplication(sys.argv)
    person_dialog = PersonDialog(db_handler, row_id=11)
    # person_dialog.show()
    yield person_dialog
    person_dialog.close()
    # sys.exit(application.exec())


def test_row_id(window):
    assert window.row_id == 11


# @patch("classes.database_handler.DatabaseHandler.execute_query")
# def test_get_data(window):
#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")
#     window.insert_into_database()
#     assert window.query.boundValues() == ["Jan", "Kowalski", "Pilot"]
#     # window._get_data()
#     # assert [window.imie, window.nazwisko, window.stanowisko] == [
#     #     "Jan",
#     #     "Kowalski",
#     #     "Pilot",
#     # ]


def test_set_edit_values(window):
    window.query = QSqlQuery()
    window.query.prepare(
        "SELECT imie, nazwisko, stanowisko FROM osoba WHERE osoba_id = ?"
    )
    window.query.addBindValue(window.row_id)
    window.query.exec()
    window.query.next()
    # window.lineEdit_imie.setText(window.query.value(0))
    # window.lineEdit_nazwisko.setText(window.query.value(1))
    # window.lineEdit_stanowisko.setText(window.query.value(2))
    person_sql = [window.query.value(0), window.query.value(1), window.query.value(2)]

    window._set_edit_values()
    window._get_data()
    person_window = [window.imie, window.nazwisko, window.stanowisko]

    assert person_window == person_sql


def test_insert_into_database(window):
    person = ["test_imie", "test_nazwisko", "test_stanowisko"]
    window.lineEdit_imie.setText(person[0])
    window.lineEdit_nazwisko.setText(person[1])
    window.lineEdit_stanowisko.setText(person[2])

    window.insert_into_database()

    window.query = QSqlQuery()
    window.query.prepare(
        "SELECT imie, nazwisko, stanowisko FROM osoba WHERE imie = ? AND nazwisko = ? AND stanowisko = ?"
    )
    window.query.addBindValue(person[0])
    window.query.addBindValue(person[1])
    window.query.addBindValue(person[2])
    window.query.exec()
    window.query.next()
    person_sql = [window.query.value(0), window.query.value(1), window.query.value(2)]
    # assert window.query.boundValues() == person
    assert person == person_sql


def test_update_database(window):
    person = ["test_imie", "test_nazwisko", "test_stanowisko"]
    window.lineEdit_imie.setText(person[0])
    window.lineEdit_nazwisko.setText(person[1])
    window.lineEdit_stanowisko.setText(person[2])
    # window._get_data()
    # person_dialog = [window.imie, window.nazwisko, window.stanowisko]
    window.update_database()

    window.query = QSqlQuery()
    window.query.prepare(
        "SELECT imie, nazwisko, stanowisko FROM osoba WHERE osoba_id = ?"
    )
    window.query.addBindValue(window.row_id)
    window.query.exec()
    window.query.next()
    person_sql = [window.query.value(0), window.query.value(1), window.query.value(2)]
    # print(person)
    # print(person_sql)
    assert person == person_sql


# class TestMyFunc:
#     """Group of tests for my_func."""

#     @pytest.mark.skip(reason="test shell")
#     def test_my_func(self):
#         """Test for my_func."""
#         pass


# def test_update_database(window):
#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")
# window.update_database()
# assert window.query.boundValues() == ["Jan", "Kowalski", "Pilot", "1"]
# assert window.query.boundValues() == ["Jan", "Kowalski", "Pilot", 0]


# def insert_into_database_query(window, imie, nazwisko, stanowisko):
#     window.lineEdit_imie.setText(imie)
#     window.lineEdit_nazwisko.setText(nazwisko)
#     window.lineEdit_stanowisko.setText(stanowisko)

#     window.insert_into_database()

#     assert window.query == (
#         "INSERT INTO osoba (imie, nazwisko, stanowisko) "
#         f"VALUES ('{imie}', '{nazwisko}', '{stanowisko}');"
#     )


# def update_database_query(window, imie, nazwisko, stanowisko):
#     window.lineEdit_imie.setText(imie)
#     window.lineEdit_nazwisko.setText(nazwisko)
#     window.lineEdit_stanowisko.setText(stanowisko)

#     window.update_database()

#     assert window.query == (
#         "INSERT INTO osoba (imie, nazwisko, stanowisko) "
#         f"VALUES ('{imie}', '{nazwisko}', '{stanowisko}');"
#     )


# def test_insert_into_database_query(window):
#     insert_into_database_query(window, "Jan", "Kowalski", "Pilot")
#     insert_into_database_query(window, "Jan4", "Kowalski2", "Pilot")
#     insert_into_database_query(window, "Jand", "Kowalski3", "Pilot")
#     insert_into_database_query(window, "", "Kowalski", "Pilot")


# def test_update_database_query(window):
#     update_database_query(window, "Jan", "Kowalski", "Pilot")
#     update_database_query(window, "Jan4", "Kowalski2", "Pilot")
#     update_database_query(window, "Jand", "Kowalski3", "Pilot")
#     update_database_query(window, "", "Kowalski", "Pilot")


# # @mock.patch("person_dialog.get_data", self.imie="Jan")
# def test_insert_into_database_query(window):

#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")

#     window.insert_into_database()

#     assert window.query == (
#         "INSERT INTO osoba (imie, nazwisko, stanowisko) "
#         "VALUES ('Jan', 'Kowalski', 'Pilot');"
#     )

# def test_update_database(window):
#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")

#     window.update_database(1)

#     assert window.query == (
#         "UPDATE osoba SET "
#         "imie = 'Jan', "
#         "nazwisko = 'Kowalski', "
#         "stanowisko = 'Pilot' "
#         "WHERE osoba_id = '1';"
#     )

# def test_insert_into_database():
#     db_handler = Mock()
#     application = QApplication(sys.argv)
#     window = PersonDialog(db_handler)

#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")

#     window.insert_into_database()

#     assert window.query == (
#         "INSERT INTO osoba (imie, nazwisko, stanowisko) "
#         "VALUES ('Jan', 'Kowalski', 'Pilot');"
#     )


# def test_update_database():
#     db_handler = Mock()
#     application = QApplication(sys.argv)
#     window = PersonDialog(db_handler)

#     window.lineEdit_imie.setText("Jan")
#     window.lineEdit_nazwisko.setText("Kowalski")
#     window.lineEdit_stanowisko.setText("Pilot")

#     window.update_database(1)

#     assert window.query == (
#         "UPDATE osoba SET "
#         "imie = 'Jan', "
#         "nazwisko = 'Kowalski', "
#         "stanowisko = 'Pilot' "
#         "WHERE osoba_id = '1';"
#     )


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


# sys.path.insert(1, "../")
# sys.path.append("../")
# sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
# os.chdir(os.path.join(os.path.dirname(__file__), ".."))
# print(os.path.join(os.path.dirname(__file__), ".."))
# print(os.getcwd())

# sys.path.insert(0, "C:\\PycharmProjects\\lotnisko\\classes")
# from person_dialog import PersonDialog
# from database_handler import DatabaseHandler

# sys.path.insert(0, "C:\\PycharmProjects\\lotnisko")

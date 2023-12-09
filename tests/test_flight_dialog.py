import sys, os
import pytest

from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlQuery

from unittest.mock import Mock, patch

from classes.flight_dialog import FlightDialog
from classes.database_handler import DatabaseHandler
from classes.initialize_database import InitializeDatabase


class FakeDatabaseHandler(DatabaseHandler):
    def execute_query(self, query):
        print("pass query execution")
        self.con.rollback()


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
    flight_dialog = FlightDialog(db_handler, row_id=15)
    # flight_dialog.show()
    yield flight_dialog
    flight_dialog.close()


def test_row_id(window):
    assert window.row_id == 15


def test_set_edit_values(window):
    window.query = QSqlQuery()
    window.query.prepare(
        "SELECT samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot WHERE lot_id = ?"
    )
    window.query.addBindValue(window.row_id)
    window.query.exec()
    window.query.next()
    flight_sql = [
        window.query.value(0),
        window.query.value(1),
        window.query.value(2),
        window.query.value(3),
    ]

    window._set_edit_values()
    window._get_data()
    flight_window = [
        window.plane,
        window.airport_a,
        window.airport_b,
        window.qt_datetime,
    ]

    print(flight_sql)
    print(flight_window)

    assert flight_window == flight_sql


# def test_insert_into_database(window):
#     person = ["test_imie", "test_nazwisko", "test_stanowisko"]
#     window.lineEdit_imie.setText(person[0])
#     window.lineEdit_nazwisko.setText(person[1])
#     window.lineEdit_stanowisko.setText(person[2])

#     window.insert_into_database()

#     window.query = QSqlQuery()
#     window.query.prepare(
#         "SELECT imie, nazwisko, stanowisko FROM osoba WHERE imie = ? AND nazwisko = ? AND stanowisko = ?"
#     )
#     window.query.addBindValue(person[0])
#     window.query.addBindValue(person[1])
#     window.query.addBindValue(person[2])
#     window.query.exec()
#     window.query.next()
#     person_sql = [window.query.value(0), window.query.value(1), window.query.value(2)]
#     # assert window.query.boundValues() == person
#     assert person == person_sql


# def test_update_database(window):
#     person = ["test_imie", "test_nazwisko", "test_stanowisko"]
#     window.lineEdit_imie.setText(person[0])
#     window.lineEdit_nazwisko.setText(person[1])
#     window.lineEdit_stanowisko.setText(person[2])
#     # window._get_data()
#     # person_dialog = [window.imie, window.nazwisko, window.stanowisko]
#     window.update_database()

#     window.query = QSqlQuery()
#     window.query.prepare(
#         "SELECT imie, nazwisko, stanowisko FROM osoba WHERE osoba_id = ?"
#     )
#     window.query.addBindValue(window.row_id)
#     window.query.exec()
#     window.query.next()
#     person_sql = [window.query.value(0), window.query.value(1), window.query.value(2)]
#     # print(person)
#     # print(person_sql)
#     assert person == person_sql

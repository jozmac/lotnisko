import sys
import pytest
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlQuery
from unittest.mock import Mock, patch

from classes.booking_dialog import BookingDialog
from classes.person_dialog import PersonDialog
from classes.database_handler import DatabaseHandler
from classes.initialize_database import InitializeDatabase


# class MockBookingDialog(BookingDialog):
#     def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.db_handler = db_handler


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
    booking_dialog = BookingDialog(db_handler, row_id=15)
    # booking_dialog.show()
    yield booking_dialog
    booking_dialog.close()
    # sys.exit(application.exec())


def test_row_id(window):
    assert window.row_id == 15


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
        "SELECT osoba_id, lot_id, klasa, miejsce_id, asystent FROM bilet WHERE bilet_id = ?"
    )
    window.query.addBindValue(window.row_id)
    window.query.exec()
    window.query.next()
    bilet_sql = [
        window.query.value(0),
        window.query.value(1),
        window.query.value(2),
        window.query.value(3),
        "Yes" if window.query.value(4) else "No",
    ]
    # window._set_edit_values()
    window._get_data()
    # bilet_window_1 = [
    #     window.person,
    #     window.flight,
    #     window.flightclass,
    #     window.seat,
    #     window.assistant,
    # ]
    bilet_window = [
        window.model_osoba.record(window.comboBox_person.currentIndex()).value(
            "osoba_id"
        ),
        window.model_lot.record(window.comboBox_flight.currentIndex()).value("lot_id"),
        window.flightclass,
        window.model_miejsce.record(window.comboBox_seat.currentIndex()).value(
            "miejsce_samolot_id"
        ),
        window.assistant,
    ]

    print(bilet_sql)
    print(bilet_window)

    assert bilet_window == bilet_sql


# TODO - dlaczego _get_data() działa tutaj inaczej?
# def test_insert_into_database(window):
#     ticket = [
#         1,
#         3,
#         "Buisness",
#         1,
#         1,
#     ]
#     window.comboBox_person.setCurrentIndex(
#         window.comboBox_person.findData(ticket[0], 0)
#     )
#     window.comboBox_flight.setCurrentIndex(
#         window.comboBox_flight.findData(ticket[1], 0)
#     )
#     window.comboBox_class.setCurrentIndex(window.comboBox_class.findData(ticket[2], 0))
#     window.comboBox_seat.setCurrentIndex(window.comboBox_seat.findData(ticket[3], 0))

#     assistant_yes_no = "Yes" if ticket[4] else "No"
#     window.comboBox_assistant.setCurrentIndex(
#         window.comboBox_assistant.findData(assistant_yes_no, 0)
#     )

#     window.insert_into_database()

#     window.query = QSqlQuery()
#     window.query.prepare(
#         "SELECT osoba_id, lot_id, klasa, miejsce_id, asystent FROM bilet WHERE osoba_id = ? AND lot_id = ? AND klasa = ? AND miejsce_id = ? AND asystent = ?"
#     )
#     window.query.addBindValue(ticket[0])
#     window.query.addBindValue(ticket[1])
#     window.query.addBindValue(ticket[2])
#     window.query.addBindValue(ticket[3])
#     window.query.addBindValue(ticket[4])
#     window.query.exec()
#     window.query.next()
#     ticket_sql = [
#         window.query.value(0),
#         window.query.value(1),
#         window.query.value(2),
#         window.query.value(3),
#         window.query.value(4),
#     ]
#     # assert window.query.boundValues() == person
#     assert ticket == ticket_sql


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


# def test_get_data_from_dialog(self):
#     db_handler = Mock()
#     application = QApplication(sys.argv)
#     window = BookingDialog(db_handler)

#     window.comboBox_person.addItem("15 - Harrison Ford")
#     window.comboBox_flight.addItem(
#         "2 - RYBNIK - PIOTRKOWTRYBUNALAKY - 2023-08-09 00:00:00"
#     )
#     window.comboBox_class.addItem("Buisness")
#     window.comboBox_seat("60 - 11F")
#     window.comboBox_assistant.setCurrentIndex(
#         window.comboBox_assistant.findData("Yes", 0)
#     )

#     # window.comboBox_person.setCurrentIndex(
#     #     window.comboBox_person.findData(window.query.value(0), 0)
#     # )
#     # window.comboBox_flight.setCurrentIndex(
#     #     window.comboBox_flight.findData(window.query.value(1), 0)
#     # )
#     # window.comboBox_class.setCurrentIndex(
#     #     window.comboBox_class.findData(window.query.value(2), 0)
#     # )
#     # window.comboBox_seat.setCurrentIndex(
#     #     window.comboBox_seat.findData(window.query.value(3), 0)
#     # )
#     # # window.seat = window.comboBox_seat.itemData(
#     # #     window.comboBox_seat.currentIndex(), Qt.ItemDataRole.EditRole
#     # # )

#     # # print(f"seat_id - {window.query.value(3)}, type - {type(window.query.value(3))}")
#     # # print(
#     # #     f"{type(window.query.value(1))}, {type(window.query.value(2))}, {type(window.query.value(3))}, {type(window.query.value(4))}"
#     # # )

#     # assistant_yes_no = "Yes" if window.query.value(4) else "No"
#     # window.comboBox_assistant.setCurrentIndex(
#     #     window.comboBox_assistant.findData(assistant_yes_no, 0)
#     # )

#     sys.exit(application.exec())


# def test_insert_into_database():
#     db_handler = Mock()
#     application = QApplication(sys.argv)
#     window = BookingDialog(db_handler)
#     # window = MockBookingDialog(db_handler)

#     window._load_combo_boxes = Mock()
#     window._get_data = Mock()
#     window._init_gui()

#     window.person = 1
#     window.flight = 1
#     window.flightclass = "Economic"
#     window.seat = 1
#     window.assistant = "No"

#     window.insert_into_database()
#     print(window.query)

#     assert window.query == (
#         "INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) "
#         "VALUES (1, 1, 'Economic', 1, 'No')"
#     )


# def test_update_database():
#     db_handler = Mock()
#     application = QApplication(sys.argv)
#     window = BookingDialog(db_handler)

#     window._load_combo_boxes = Mock()
#     window._get_data = Mock()
#     window.person = 1
#     window.flight = 1
#     window.flightclass = "Economic"
#     window.seat = 1
#     window.assistant = "No"

#     window.update_database(1)

#     assert window.query == (
#         "UPDATE bilet SET "
#         "osoba_id = 1, "
#         "lot_id = 1, "
#         "miejsce_id = 1, "
#         "asystent = 'No', "
#         "klasa = 'Economic', "
#         "WHERE bilet_id = 1"
#     )

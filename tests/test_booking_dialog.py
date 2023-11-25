import sys
import pytest
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from unittest.mock import Mock, patch

sys.path.insert(0, "C:\\PycharmProjects\\lotnisko")

from classes.booking_dialog import BookingDialog
from classes.database_handler import DatabaseHandler

# TODO - wszystko do poprawy


# class MockBookingDialog(BookingDialog):
#     def __init__(self, db_handler: DatabaseHandler, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.db_handler = db_handler


def test_insert_into_database():
    db_handler = Mock()
    application = QApplication(sys.argv)
    window = BookingDialog(db_handler)
    # window = MockBookingDialog(db_handler)

    window.load_combo_boxes = Mock()
    window.get_data = Mock()
    window.init_gui()

    window.person = 1
    window.flight = 1
    window.flightclass = "Economic"
    window.seat = 1
    window.assistant = "No"

    window.insert_into_database()
    print(window.query)

    assert window.query == (
        "INSERT INTO bilet (osoba_id, lot_id, klasa, miejsce_id, asystent) "
        "VALUES (1, 1, 'Economic', 1, 'No')"
    )


def test_update_database():
    db_handler = Mock()
    application = QApplication(sys.argv)
    window = BookingDialog(db_handler)

    window.load_combo_boxes = Mock()
    window.get_data = Mock()
    window.person = 1
    window.flight = 1
    window.flightclass = "Economic"
    window.seat = 1
    window.assistant = "No"

    window.update_database(1)

    assert window.query == (
        "UPDATE bilet SET "
        "osoba_id = 1, "
        "lot_id = 1, "
        "miejsce_id = 1, "
        "asystent = 'No', "
        "klasa = 'Economic', "
        "WHERE bilet_id = 1"
    )


if __name__ == "__main__":
    # sys.argv.append("--qt=qt6")
    sys.exit(pytest.main(["-v", __file__]))

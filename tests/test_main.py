import pytest
from pytest import MonkeyPatch

from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
import sys, os

from main import MainWindow
from classes.booking_dialog import BookingDialog
from classes.flight_dialog import FlightDialog
from classes.person_dialog import PersonDialog
from classes.initialize_database import InitializeDatabase
from classes.database_handler import DatabaseHandler

# - Positive testing - make sure the expected values are right
# - Edge cases - input 0, NaN, etc. Split edge cases into it's own tests
# - Coverage - % score - lines of code executed by test - all combinations of boolean switch must be tested
# - Negative testing - What mistakes might they make when using a function? error messages

# TODO
# with TestDb as db:
#   def __enter__():
#       self.db =
#       create table
#       insert
#   def __exit__():
#       usunięcie bazy danych

# @contextmanager
# def test_db():
#   db =
#   create tables
#   insert data
#   yield db
#   db.close()


@pytest.fixture
def app():
    application = QApplication(sys.argv)
    # dbinit = InitializeDatabase()
    # dbinit.initialize_sqlite()
    # db_handler = DatabaseHandler(database_name="test_lotnisko")
    db_handler = DatabaseHandler("data/lotnisko.sqlite3")
    db_handler.create_connection_sqlite()
    # db_handler = DatabaseHandler("data\lotnisko.sqlite3", database_type="QSQLITE")
    # db_handler.create_connection()
    widget = MainWindow(db_handler)
    # widget.show()
    # return widget
    yield widget
    widget.close()
    # sys.exit(application.exec())


# class TestMain:
def test_database_connection(app):
    assert app.db_handler.con.isOpen()


def test_tab_labels(app):
    assert app.tabWidget.tabText(0) == "Osoba"
    assert app.tabWidget.tabText(1) == "Bilet"
    assert app.tabWidget.tabText(2) == "Lot"


def test_widget_title(app):
    assert app.windowTitle() == "Airport Management System"


def test_signal_connections(app):
    assert app.pushButton_dodaj_osoba.clicked.disconnect(app.osoba_tab.add_row) == None
    assert app.pushButton_dodaj_bilet.clicked.disconnect(app.bilet_tab.add_row) == None
    assert app.pushButton_dodaj_lot.clicked.disconnect(app.lot_tab.add_row) == None
    assert (
        app.pushButton_usun_osoba.clicked.disconnect(app.osoba_tab.delete_row) == None
    )
    assert (
        app.pushButton_usun_bilet.clicked.disconnect(app.bilet_tab.delete_row) == None
    )
    assert app.pushButton_usun_lot.clicked.disconnect(app.lot_tab.delete_row) == None
    assert (
        app.pushButton_edytuj_osoba.clicked.disconnect(app.osoba_tab.edit_row) == None
    )
    assert (
        app.pushButton_edytuj_bilet.clicked.disconnect(app.bilet_tab.edit_row) == None
    )
    assert app.pushButton_edytuj_lot.clicked.disconnect(app.lot_tab.edit_row) == None
    assert app.pushButton_info_osoba.clicked.disconnect(app.osoba_tab.info_row) == None
    assert app.pushButton_info_bilet.clicked.disconnect(app.bilet_tab.info_row) == None
    assert app.pushButton_info_lot.clicked.disconnect(app.lot_tab.info_row) == None


def test_data_loading(app):
    app.tabWidget.setCurrentIndex(2)
    assert app.index == 2


def test_database_closing(app):
    app.close()
    assert not app.db_handler.con.isOpen()


# def test_pay_order(monkeypatch: MonkeyPatch):
#     inputs = ["1249190007575069", "12", "2024"]
#     monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
#     monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
#     order = Order()
#     order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
#     pay_order(order)


# def test_pay_order_invalid(monkeypatch: MonkeyPatch):
#     with pytest.raises(ValueError):
#         inputs = ["1249190007575069", "12", "2024"]
#         monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
#         monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
#         order = Order()
#         pay_order(order)


# def test_insert_osoba(app):
#     initial_row_count = app.tableView_osoba.model().rowCount()

#     window = PersonDialog(app.db_handler.db)
#     window.lineEdit_imie.setText("Jozef")
#     window.lineEdit_nazwisko.setText("Mackowiak")
#     window.lineEdit_stanowisko.setText("Pilot")
#     window.insert_into_database()
#     app.load_osoba()

#     assert app.tableView_osoba.model().rowCount() == initial_row_count + 1


# def test_add_and_delete_osoba(app):
#     initial_row_count = app.tableView_osoba.model().rowCount()

#     app.dodaj_osoba()
#     assert app.tableView_osoba.model().rowCount() == initial_row_count + 1

#     app.usun_osoba()
#     assert app.tableView_osoba.model().rowCount() == initial_row_count


# def test_add_and_delete_bilet(test_database_connection):
#     app = test_database_connection
#     initial_row_count = app.tableView_bilet.model().rowCount()

#     # Add a new Bilet
#     app.dodaj_bilet()
#     assert app.tableView_bilet.model().rowCount() == initial_row_count + 1

#     # Delete the added Bilet
#     app.usun_bilet()
#     assert app.tableView_bilet.model().rowCount() == initial_row_count


# def test_add_and_delete_lot(test_database_connection):
#     app = test_database_connection
#     initial_row_count = app.tableView_lot.model().rowCount()

#     # Add a new Lot
#     app.dodaj_lot()
#     assert app.tableView_lot.model().rowCount() == initial_row_count + 1

#     # Delete the added Lot
#     app.usun_lot()
#     assert app.tableView_lot.model().rowCount() == initial_row_count


# # Test Editing Records
# def test_edit_osoba(test_database_connection):
#     app = test_database_connection

#     # Add a new Osoba
#     app.dodaj_osoba()

#     # Edit the added Osoba
#     app.edytuj_osoba()
#     # Assert that editing functionality works as expected


# def test_edit_bilet(test_database_connection):
#     app = test_database_connection

#     # Add a new Bilet
#     app.dodaj_bilet()

#     # Edit the added Bilet
#     app.edytuj_bilet()
#     # Assert that editing functionality works as expected


# def test_edit_lot(test_database_connection):
#     app = test_database_connection

#     # Add a new Lot
#     app.dodaj_lot()

#     # Edit the added Lot
#     app.edytuj_lot()
#     # Assert that editing functionality works as expected


# # Test Printing Boarding Pass
# def test_print_boarding_pass(test_database_connection, qtbot):
#     app = test_database_connection

#     # Add a new Bilet
#     app.dodaj_bilet()

#     # Select the added Bilet
#     app.tableView_bilet.selectRow(app.tableView_bilet.model().rowCount() - 1)

#     # Trigger the printing of the boarding pass
#     with qtbot.waitSignal(app.print_preview_signal, timeout=1000):
#         app.info_bilet()
#     # Assert that the boarding pass is printed successfully

# # Test Tab Changes
# def test_tab_changes(test_database_connection):
#     app = test_database_connection

#     app.tabWidget.setCurrentIndex(0)  # Switch to Osoba tab
#     assert app.tabWidget.currentIndex() == 0
#     assert app.tableView_osoba.model() is not None

#     app.tabWidget.setCurrentIndex(1)  # Switch to Bilet tab
#     assert app.tabWidget.currentIndex() == 1
#     assert app.tableView_bilet.model() is not None

#     app.tabWidget.setCurrentIndex(2)  # Switch to Lot tab
#     assert app.tabWidget.currentIndex() == 2
#     assert app.tableView_lot.model() is not None


# @pytest.fixture
# def test_add_and_delete_osoba(app):
#     app = test_database_connection
#     initial_row_count = app.tableView_osoba.model().rowCount()

#     app.dodaj_osoba()
#     assert app.tableView_osoba.model().rowCount() == initial_row_count + 1

#     app.usun_osoba()
#     assert app.tableView_osoba.model().rowCount() == initial_row_count


if __name__ == "__main__":
    # pytest.main(["-vv", f"C:\\PycharmProjects\\lotnisko\\test_main.py"])
    sys.exit(pytest.main(["-vv", __file__]))


# def test_database_connection(qtbot):
#     app = QApplication(sys.argv)
#     db_handler = DatabaseHandler()
#     widget = MainWindow(db_handler)
#     # qtbot.addWidget(widget)
#     # widget.pushButton_info_osoba.click()
#     assert db_handler.db.isOpen()

# @pytest.fixture
# def app(qtbot):
#     app = QApplication(sys.argv)
#     db_handler = DatabaseHandler()
#     app_window = MainWindow(db_handler)
#     # qtbot.addWidget(test_main)
#     yield app_window
#     app_window.close()
#     # app.quit()
#     sys.exit(app.exec())


# def test_database_connection(app):
#     assert app.db_handler.db.isOpen()


# def test_add_record_to_database(app):
#     app.some_add_record_function()
#     assert app.some_check_function()


# if __name__ == "__main__":
#     pytest.main()


# import sys
# import pytest
# from PyQt6.QtWidgets import QApplication
# from main import MainWindow


# @pytest.fixture
# def main_window(qtbot):
#     app = QApplication(sys.argv)
#     db_handler = DatabaseHandler()
#     window = MainWindow(db_handler)
#     window.show()
#     qtbot.addWidget(window)
#     yield window
#     window.close()
#     sys.exit(app.exec())


# def test_main_window_initialization(main_window, qtbot):
#     qtbot.waitForWindowShown(main_window)


# # def test_load_bilet(main_window, qtbot):
# #     qtbot.mouseClick(main_window.pushButton_dodaj_bilet, Qt.MouseButtonPress)
# #     # You may need to interact with the dialog that opens for adding a bilet
# #     # Replace the line above with appropriate interactions as needed
# #     assert main_window.model is not None


# # def test_dodaj_bilet(main_window, qtbot):
# #     # Test the dodaj_bilet method
# #     initial_row_count = main_window.model.rowCount()
# #     qtbot.mouseClick(main_window.pushButton_dodaj_bilet, Qt.MouseButtonPress)
# #     # You may need to interact with the dialog that opens for adding a bilet
# #     # Replace the line above with appropriate interactions as needed
# #     assert main_window.model.rowCount() == initial_row_count + 1


# if __name__ == "__main__":
#     pytest.main()


# @pytest.fixture
# def app():
#     application = QApplication(sys.argv)
#     db_handler = DatabaseHandler()
#     widget = MainWindow(db_handler)
#     yield widget
#     # widget.close()
#     # sys.exit(application.exec())


# def test_database_connection(app):
#     assert app.db_handler.db.isOpen()


# def test_close(app):
#     assert app.close()


# if __name__ == "__main__":
#     pytest.main(["-v", f"C:\\PycharmProjects\\lotnisko\\test_main.py"])

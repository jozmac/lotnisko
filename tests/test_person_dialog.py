import sys, os
import pytest

# import pytest-mock
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from unittest.mock import Mock, patch

# sys.path.insert(1, "../")
# sys.path.append("../")
# sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
# os.chdir(os.path.join(os.path.dirname(__file__), ".."))
# print(os.path.join(os.path.dirname(__file__), ".."))
# print(os.getcwd())

# sys.path.insert(0, "C:\\PycharmProjects\\lotnisko\\classes")
# from person_dialog import PersonDialog
# from database_handler import DatabaseHandler

sys.path.insert(0, "C:\\PycharmProjects\\lotnisko")
from classes.person_dialog import PersonDialog
from classes.database_handler import DatabaseHandler

# from person_dialog import PersonDialog
# from database_handler import DatabaseHandler


# QSqlQuery(None, self.db_handler.con) nie działa poprawnie przez db_handler mock


# class FakeDatabaseHandler(DatabaseHandler):
#     def execute_query(self, query):
#         pass


@pytest.fixture
def window():
    db_handler = Mock()
    # db_handler = DatabaseHandler()
    # db_handler = FakeDatabaseHandler()
    db_handler.create_connection()
    app = QApplication(sys.argv)
    person_dialog = PersonDialog(db_handler)
    yield person_dialog
    # sys.exit(app.exec())


# @patch("classes.database_handler.DatabaseHandler.execute_query")
def test_insert_into_database_query(window):
    window.lineEdit_imie.setText("Jan")
    window.lineEdit_nazwisko.setText("Kowalski")
    window.lineEdit_stanowisko.setText("Pilot")
    # window.insert_into_database()
    # assert window.query.boundValues() == ["Jan", "Kowalski", "Pilot"]
    window.get_data()
    assert [window.imie, window.nazwisko, window.stanowisko] == [
        "Jan",
        "Kowalski",
        "Pilot",
    ]


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


# You can similarly create a test case for `update_database`.

if __name__ == "__main__":
    # sys.argv.append("--qt=qt6")
    sys.exit(pytest.main(["-vv", __file__]))

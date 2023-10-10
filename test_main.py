import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from main import Window

# pytest -v C:\PycharmProjects\lotnisko\test_main.py


@pytest.fixture
def app():
    application = QApplication(sys.argv)
    app_window = Window()
    yield app_window
    app_window.close()
    application.quit()


def test_database_connection(app):
    # Check if the database connection is established
    assert app.db.isOpen()


def test_add_record_to_database(app):
    # Simulate adding a record to the database
    app.some_add_record_function()
    # Assert that the record was added correctly
    assert app.some_check_function()


# Write more test cases for different functionalities


if __name__ == "__main__":
    pytest.main()


# def test_uppercase():
#     assert "loud noises".upper() == "LOUD NOISES"


# def test_reversed():
#     assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]


# def test_some_primes():
#     assert 37 in {
#         num for num in range(2, 50) if not any(num % div == 0 for div in range(2, num))
#     }

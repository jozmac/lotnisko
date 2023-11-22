import sys
from PyQt6.QtWidgets import QApplication
from database_handler import DatabaseHandler


class RunTestDialog:
    def __init__(self, dialog, row_id=0):
        app = QApplication(sys.argv)
        db_handler = DatabaseHandler()
        db_handler.create_connection()
        window = dialog(db_handler, row_id)
        window.show()
        sys.exit(app.exec())

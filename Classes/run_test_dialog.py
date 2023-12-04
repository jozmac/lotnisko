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

        # from PyQt6.QtWidgets import QTableView

        # table_view = QTableView()
        # table_view.show()
        # table_view.setModel(window.model_miejsce)

        sys.exit(app.exec())

    # def display_model(self, model):
    #     from PyQt6.QtWidgets import QTableView

    #     table_view = QTableView()
    #     table_view.show()
    #     table_view.setModel(model)

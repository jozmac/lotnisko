from PyQt6.QtWidgets import (
    QWidget,
    QMessageBox,
    QAbstractItemView,
)
from PyQt6.QtSql import (
    QSqlQueryModel,
    QSqlQuery,
)

from PyQt6.QtCore import Qt, QModelIndex


class Tab(QWidget):
    def __init__(self, db_handler, tab_name, table, query, id_column, dialog_class):
        self.db_handler = db_handler
        self.tab_name = tab_name
        self.table = table
        self.query = query
        self.id_column = id_column
        self.dialog_class = dialog_class
        self.init_ui()
        super().__init__()

    def init_ui(self):
        self.model = QSqlQueryModel(None)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def load_data(self):
        self.model.setQuery(self.query, self.db_handler.con)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def select_row_msg(self, text="Select one of the rows."):
        msg = QMessageBox(self, text=f"{text}")
        msg.setWindowTitle("Information")
        msg.exec()

    def get_selected_row_id(self, index: QModelIndex) -> int:
        if not index.isValid():
            return
        # TODO - aktualnie pierwsza kolumna tabeli musi zawierać id (index.siblingAtColumn(0))
        return self.model.data(index.siblingAtColumn(0), 0)

    def add_row(self):
        window = self.dialog_class(self.db_handler)
        if window.exec():
            window.insert_into_database()
            # self.table.scrollToBottom()
            self.load_data()

    def edit_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if row_id is None:
            return self.select_row_msg()
        window = self.dialog_class(self.db_handler, row_id)
        if not window.exec():
            return
        # window.set_edit_values()
        window.update_database()
        self.load_data()

    def delete_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if row_id is None:
            return self.select_row_msg()

        reply = QMessageBox.question(
            self,
            "Remove Item",
            "Do you want to remove selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            return
        query = QSqlQuery(None, self.db_handler.con)
        query.prepare(f"DELETE FROM {self.tab_name} WHERE {self.id_column} = ?")
        query.addBindValue(row_id)
        if query.exec():
            print("Data deleted successfully.")
        else:
            print(f"Error deleting data: {query.lastError().text()}")
        self.load_data()

    def info_row(self):
        row_id = self.get_selected_row_id(self.table.currentIndex())
        if not row_id:
            return self.select_row_msg()

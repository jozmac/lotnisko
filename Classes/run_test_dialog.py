import sys
from PyQt6.QtWidgets import QApplication, QDialog, QTableView, QVBoxLayout, QTableView
from database_handler import DatabaseHandler

import pandas as pd


class RunTestDialog:
    def __init__(self, dialog, row_id=0):
        app = QApplication(sys.argv)
        db_handler = DatabaseHandler()
        db_handler.create_connection()
        window = dialog(db_handler, row_id)
        window.show()
        sys.exit(app.exec())

    # def display_model(self, model):
    #     from PyQt6.QtWidgets import QTableView

    #     app = QApplication(sys.argv)
    #     table_view = QTableView()
    #     table_view.setModel(model)
    #     table_view.show()
    #     sys.exit(app.exec())


# def display_model(model):
#     app = QApplication(sys.argv)
#     table_view = QTableView()
#     table_view.setModel(model)
#     table_view.show()
#     sys.exit(app.exec())


class DisplayModel(QDialog):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle("Display Model")
        table_view = QTableView()
        table_view.setModel(model)
        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.exec()


class DisplayWidgets(QDialog):
    def __init__(self, *widgets):
        super().__init__()

        layout = QVBoxLayout(self)

        for widget in widgets:
            layout.addWidget(widget)

        self.exec()


def qtmodel_to_dataframe(qt_model):
    """
    Convert a PyQt model to a Pandas DataFrame.

    Parameters:
    - qt_model: The PyQt model to be converted.

    Returns:
    - pd.DataFrame: The Pandas DataFrame containing the data from the PyQt model.
    """
    rows = qt_model.rowCount()
    columns = qt_model.columnCount()

    headers = [
        qt_model.headerData(col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        for col in range(columns)
    ]

    df = pd.DataFrame(columns=headers)

    for row in range(rows):
        data = [qt_model.data(qt_model.index(row, col)) for col in range(columns)]
        df.loc[row] = data

    return df


def dataframe_to_qtmodel(dataframe):
    """
    Convert a Pandas DataFrame to a PyQt model.

    Parameters:
    - dataframe: The Pandas DataFrame to be converted.

    Returns:
    - QStandardItemModel: The PyQt QStandardItemModel containing the data from the DataFrame.
    """
    from PyQt6.QtGui import QStandardItem, QStandardItemModel

    model = QStandardItemModel()

    model.setHorizontalHeaderLabels(dataframe.columns)

    for row in range(dataframe.shape[0]):
        items = [
            QStandardItem(str(dataframe.iloc[row, col]))
            for col in range(dataframe.shape[1])
        ]
        model.appendRow(items)

    return model


def print_qtmodel(qtmodel):
    print(qtmodel_to_dataframe(qtmodel))

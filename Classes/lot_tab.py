from classes.tab import Tab
from classes.flight_dialog import FlightDialog

from PyQt6.QtCore import Qt


class LotTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "lot"
        id_column = "lot_id"
        dialog_class = FlightDialog
        query = (
            # "SELECT l.lot_id, s.model, la.city, lb.city, l.datetime "
            "SELECT l.lot_id AS id, s.model AS plane, la.city AS from, lb.city AS to, l.datetime "
            "FROM lot l "
            "INNER JOIN samolot s ON s.samolot_id = l.samolot_id "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

    # def load_data(self):
    #     self.model.setHeaderData(0, Qt.Orientation.Horizontal, "id")
    #     self.model.setHeaderData(1, Qt.Orientation.Horizontal, "plane")
    #     self.model.setHeaderData(2, Qt.Orientation.Horizontal, "from")
    #     self.model.setHeaderData(3, Qt.Orientation.Horizontal, "to")
    #     self.model.setHeaderData(4, Qt.Orientation.Horizontal, "datetime")
    #     super().load_data()

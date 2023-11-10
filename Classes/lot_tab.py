from classes.tab import Tab
from classes.flight_dialog import FlightDialog


class LotTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "lot"
        id_column = "lot_id"
        dialog_class = FlightDialog
        # query = (
        #     "SELECT l.lot_id, s.model, l.lotnisko_a_id, la.city, l.lotnisko_b_id, lb.city, l.datetime "
        #     "FROM lot l "
        #     "INNER JOIN samolot s ON s.samolot_id = l.samolot_id "
        #     "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
        #     "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        # )
        query = (
            "SELECT l.lot_id, s.model, la.city, lb.city, l.datetime "
            "FROM lot l "
            "INNER JOIN samolot s ON s.samolot_id = l.samolot_id "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

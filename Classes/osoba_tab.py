from classes.tab import Tab
from classes.person_dialog import PersonDialog

from PyQt6.QtCore import Qt


class OsobaTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "osoba"
        id_column = "osoba_id"
        dialog_class = PersonDialog
        # query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        query = "SELECT osoba_id AS id, imie AS name, nazwisko AS surname, stanowisko AS appointment FROM osoba"

        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

    # def load_data(self):
    #     self.model.setHeaderData(0, Qt.Orientation.Horizontal, "id")
    #     self.model.setHeaderData(1, Qt.Orientation.Horizontal, "name")
    #     self.model.setHeaderData(2, Qt.Orientation.Horizontal, "surname")
    #     self.model.setHeaderData(3, Qt.Orientation.Horizontal, "appointment")
    #     super().load_data()

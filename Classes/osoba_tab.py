from classes.tab import Tab
from classes.person_dialog import PersonDialog


class OsobaTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "osoba"
        id_column = "osoba_id"
        dialog_class = PersonDialog
        query = "SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba"
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

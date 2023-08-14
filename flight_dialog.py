from PyQt6.QtWidgets import QDialog, QApplication, QComboBox
from PyQt6.uic import loadUi
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt6.QtCore import QStringListModel

import sys, os
# from functions import get_data, drop_tables, create_tables
from functions import select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik
from datetime import datetime


# class Flight_dialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         directory = os.path.dirname(os.path.realpath(sys.argv[0]))
#         gui_directory = os.path.join(directory, 'GUI')
#         os.chdir(gui_directory)
#         # os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
#         loadUi("flight_dialog.ui", self)

#         self.samolot = select_samolot()
#         self.lotnisko = select_lotnisko()

#         # osoba = select_osoba()
#         # s = [''.join(str(x)) for x in osoba]
#         # self.comboBox_plane.addItems([''.join(str(x)) for x in self.samolot])
#         # self.comboBox_from.addItems([''.join(str(x)) for x in self.lotnisko])
#         # self.comboBox_to.addItems([''.join(str(x)) for x in self.lotnisko])
#         self.populate_combo_boxes()

#         self.comboBox_from.setCurrentIndex(1538)
#         self.comboBox_to.setCurrentIndex(1538)


#     def add_items_to_combo_box(self, combo_box, items):
#         combo_box.addItems([str(item) for item in items])

#     def populate_combo_boxes(self):
#         self.add_items_to_combo_box(self.comboBox_plane, self.samolot)
#         self.add_items_to_combo_box(self.comboBox_from, self.lotnisko)
#         self.add_items_to_combo_box(self.comboBox_to, self.lotnisko)

#     def get_selected_options(self):
#         self.selected_date = self.calendarWidget.selectedDate().toPyDate()
#         self.selected_time = self.timeEdit.time().toPyTime()

#         return [self.comboBox_plane.currentText(),
#                 self.comboBox_from.currentText(), 
#                 self.comboBox_to.currentText(), 
#                 datetime.combine(self.selected_date, self.selected_time)]
    



def create_connection():
    try:
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("localhost")
        db.setDatabaseName("lotnisko")
        db.setUserName("postgres")
        db.setPassword("password")
        db.setPort(5432)

        if not db.open():
            raise ConnectionError(f"Could not open database. Error: {db.lastError().text()}")
        return db
    except Exception as e:
        raise ConnectionError(f"Connection error: {e}")

class Flight_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        loadUi("flight_dialog.ui", self)

        self.samolot = self.select_samolot()
        self.lotnisko = self.select_lotnisko()
        # print(self.samolot)

        # model = QStringListModel()
        # model = self.samolot
        # model.setStringList(self.samolot)
        # combo_box.setModel(model)

        self.comboBox_from.setCurrentIndex(1538)
        self.comboBox_to.setCurrentIndex(1538)


        self.populate_combo_boxes()

    def select_samolot(self):
        query = "SELECT samolot_id, model, ilosc_miejsc FROM samolot"
        # query = "SELECT samolot_id FROM samolot"
        return self.select_data(query)

    def select_lotnisko(self):
        query = "SELECT lotnisko_id, icao_code, name, city, country FROM lotnisko"
        return self.select_data(query)

    def select_data(self, query):
        model = QSqlQueryModel()
        db = create_connection()
        if not db:
            return []
        model.setQuery(query, db)
        # items = [model.record(i).value(0) for i in range(model.rowCount())]
        # return items
        return model

    # def create_connection(self):
    #     # Your create_connection code here...

    def populate_combo_boxes(self):
        self.populate_combo_box(self.comboBox_plane, self.samolot)
        self.populate_combo_box(self.comboBox_from, self.lotnisko)
        self.populate_combo_box(self.comboBox_to, self.lotnisko)

    def populate_combo_box(self, combo_box, items):
        # model = QSqlQueryModel()
        # model = QStringListModel()
        model = items
        # model.setStringList(items)
        combo_box.setModel(model)
        # print(f"input items: {items}")

    def get_selected_options(self):
        self.selected_date = self.calendarWidget.selectedDate().toPyDate()
        self.selected_time = self.timeEdit.time().toPyTime()

        return [self.comboBox_plane.currentText(),
                self.comboBox_from.currentText(),
                self.comboBox_to.currentText(),
                datetime.combine(self.selected_date, self.selected_time)]






#     # self.insertButton.clicked.connect(self.insert_data_to_database)

#     # def insert_data_to_database(self):
#     #     selected_options = self.get_selected_options()
#     #     osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina = selected_options
#     #     self.insert_ticket_to_database(osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina)

#     # def insert_ticket_to_database(self, osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina):
#     #     try:
#     #         with pg2.connect(**DB_CONFIG) as db:
#     #             cur = db.cursor()
#     #             cur.execute("INSERT INTO bilet (osoba_id, lotnisko_a_id, lotnisko_b_id, klasa, miejsce_id, asystent, data, godzina) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#     #                         (osoba, lotnisko_a, lotnisko_b, klasa, miejsce, asystent, data, godzina))
#     #             db.commit()
#     #             print("Ticket added to the database.")
#     #     except pg2.Error as e:
#     #         print("Error while adding ticket:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Flight_dialog()
    window.show()
    sys.exit(app.exec())
    # db.close()

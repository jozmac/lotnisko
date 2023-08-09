from PyQt6.QtWidgets import QDialog, QApplication, QComboBox
from PyQt6.uic import loadUi
import sys, os
# from functions import get_data, drop_tables, create_tables
from functions import select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie, select_pracownik


class Booking_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        gui_directory = os.path.join(directory, 'GUI')
        os.chdir(gui_directory)
        # os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("booking_dialog.ui", self)

        # osoba = select_osoba()
        # s = [''.join(str(x)) for x in osoba]
        self.comboBox_person.addItems([''.join(str(x)) for x in select_osoba()])
        self.comboBox_flight.addItems([''.join(str(x)) for x in select_lot()])
        self.comboBox_seat.addItems([''.join(str(x)) for x in select_miejsce()])



    def get_selected_options(self):
        return [self.comboBox_person.currentText(), 
                self.comboBox_flight.currentText(), 
                self.comboBox_class.currentText(), 
                self.comboBox_seat.currentText(), 
                self.comboBox_assistant.currentText(),]
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # if not createConnection("contacts.sqlite"):
    #     sys.exit(1)


    window = Booking_dialog()
    window.show()
    sys.exit(app.exec())
    # db.close()

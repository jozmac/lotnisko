from PyQt6.QtWidgets import QDialog, QApplication, QComboBox
from PyQt6.uic import loadUi
import sys, os
# from functions import get_data, drop_tables, create_tables
from functions import select_osoba, select_lotnisko, select_samolot, select_bilet, select_lot, select_miejsce, select_zajete_miejsce, select_zatrudnienie


class Booking_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("booking_dialog.ui", self)

        # self.cb_platform = QComboBox(self)
        # self.cb_platform.addItem('Android')
        # self.cb_platform.addItem('iOS')
        # self.cb_platform.addItem('Windows')
        # self.string_list = (["apple", "banana", "cherry"])
        # self.cb_platform.addItems(self.string_list)

        # osoba = select_osoba()
        # s = [''.join(str(x)) for x in osoba]
        self.comboBox_person.addItems([''.join(str(x)) for x in select_osoba()])
        self.comboBox_from.addItems([''.join(str(x)) for x in select_lotnisko()])
        self.comboBox_to.addItems([''.join(str(x)) for x in select_lotnisko()])
        self.comboBox_seat.addItems([''.join(str(x)) for x in select_miejsce()])

    def get_selected_options(self):
        return self.comboBox_person.currentText(), self.comboBox_from.currentText(), self.comboBox_to.currentText(), self.comboBox_class.currentText(), self.comboBox_seat.currentText(), self.comboBox_assistant.currentText()




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # if not createConnection("contacts.sqlite"):
    #     sys.exit(1)


    window = Booking_dialog()
    window.show()
    sys.exit(app.exec())
    # db.close()

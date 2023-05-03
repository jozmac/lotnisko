from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
import sys, os
# from functions import get_data, drop_tables, create_tables


class Booking_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("booking_dialog.ui", self)

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

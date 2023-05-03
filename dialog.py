from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi
import sys, os
# from functions import get_data, drop_tables, create_tables


class Booking_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        loadUi("booking_dialog.ui", self)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # if not createConnection("contacts.sqlite"):
    #     sys.exit(1)


    window = Booking_dialog()
    window.show()
    sys.exit(app.exec())
    # db.close()

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUiType
import os
import bcrypt


UI_PATH = os.path.join(os.path.dirname(__file__), "..", "GUI", "password_dialog.ui")
FORM_CLASS, BASE_CLASS = loadUiType(UI_PATH)


class PasswordDialog(QDialog, FORM_CLASS):
    def __init__(self, db_handler, osoba_id=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_handler = db_handler
        self.osoba_id = osoba_id
        self._init_ui()

    def _init_ui(self):
        self.setupUi(self)
        self.setWindowTitle("Airport Management System")
        self.setWindowIcon(QIcon("GUI/airport.png"))
        self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.buttonBox.accepted.connect(self.check_password)
        self.lineEdit.setFocus()
        # self.buttonBox.rejected.connect(Dialog.reject)

    def check_password(self):
        self.query = QSqlQuery()
        self.query.prepare("SELECT password_hash, salt FROM osoba WHERE osoba_id = ?")
        self.query.addBindValue(self.osoba_id)
        self.query.exec()
        self.query.next()
        password_hash = self.query.value(0).encode("utf-8")
        # salt = self.query.value(1).encode("utf-8")
        # print(f"hash from db: {password_hash}")
        # print(f"salt from db: {salt}")
        # hashed_lineedit_password = bcrypt.hashpw(
        #     self.lineEdit.text().encode("utf-8"), salt
        # )
        # self.match = bcrypt.checkpw(password_hash, hashed_lineedit_password)
        self.match = bcrypt.checkpw(self.lineEdit.text().encode("utf-8"), password_hash)
        # print(hashed_lineedit_password)
        # print(password_hash)
        # print(self.lineEdit.text().encode("utf-8"))
        # print(f"match: {self.match}, {type(self.match)}")
        return self.match


if __name__ == "__main__":
    from run_test_dialog import RunTestDialog

    test_window = RunTestDialog(PasswordDialog, row_id=6)

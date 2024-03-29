from classes.tab import Tab
from classes.booking_dialog import BookingDialog

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QPainter, QColor, QTextDocument, QFont
from PyQt6.QtCore import Qt

from classes.password_dialog import PasswordDialog


class BiletTab(Tab):
    def __init__(self, db_handler, table):
        tab_name = "bilet"
        id_column = "bilet_id"
        dialog_class = BookingDialog
        query = (
            # "SELECT b.bilet_id, o.imie, o.nazwisko, b.lot_id, m.miejsce_samolot_name, b.asystent, b.klasa  "
            # "SELECT b.bilet_id, o.imie, o.nazwisko, la.city || ' - ' || lb.city AS lot, m.miejsce_samolot_name, b.asystent, b.klasa  "
            "SELECT b.bilet_id AS id, o.imie AS name, o.nazwisko AS surname, la.city || ' - ' || lb.city AS flight, m.miejsce_samolot_name AS seat, b.asystent as assistant, b.klasa AS class  "
            "FROM bilet b "
            "INNER JOIN osoba o ON o.osoba_id = b.osoba_id "
            "INNER JOIN miejsce m ON m.miejsce_id = b.miejsce_id "
            "INNER JOIN lot l ON l.lot_id = b.lot_id "
            "INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id "
            "INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id "
        )
        super().__init__(db_handler, tab_name, table, query, id_column, dialog_class)

    # enum lista nazw i for
    # def load_data(self):
    #     self.model.setHeaderData(0, Qt.Orientation.Horizontal, "id")
    #     self.model.setHeaderData(1, Qt.Orientation.Horizontal, "name")
    #     self.model.setHeaderData(2, Qt.Orientation.Horizontal, "surname")
    #     self.model.setHeaderData(3, Qt.Orientation.Horizontal, "flight")
    #     self.model.setHeaderData(4, Qt.Orientation.Horizontal, "seat")
    #     self.model.setHeaderData(5, Qt.Orientation.Horizontal, "assistant")
    #     self.model.setHeaderData(6, Qt.Orientation.Horizontal, "class")
    #     super().load_data()

    def info_row(self):
        id = self.get_selected_row_id(self.table.currentIndex())
        query = QSqlQuery(None, self.db_handler.con)
        query.prepare(
            """
            SELECT o.osoba_id
            FROM bilet b
            INNER JOIN osoba o ON o.osoba_id = b.osoba_id
            WHERE b.bilet_id = ?;
            """
        )
        query.addBindValue(id)
        query.exec()
        query.next()
        self.osoba_id = query.value(0)

        # window = PasswordDialog(self.db_handler, self.osoba_id).exec()
        window = PasswordDialog(self.db_handler, self.osoba_id)
        if not window.exec():
            return
        if window.match == False:
            return self.select_row_msg("Wrong Password.")

        if not self.table.selectedIndexes():
            return self.select_row_msg("Select row to print boarding pass.")
        self.print_preview()
        msg = QMessageBox(self, text="Boarding pass printed successfully.")
        msg.setWindowTitle("Information")
        msg.exec()

    def print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFileName("boarding_pass.pdf")
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_boarding_pass)
        preview_dialog.exec()

    def print_boarding_pass(self, printer: QPrinter):
        painter = QPainter()
        painter.begin(printer)
        painter.setPen(QColor(0, 0, 0, 255))
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Calibri")
        painter.setFont(font)
        id = self.get_selected_row_id(self.table.currentIndex())
        query = QSqlQuery(None, self.db_handler.con)
        query.prepare(
            """
            SELECT o.imie, o.nazwisko, l.datetime, m.miejsce_samolot_id, s.samolot_id, s.model, la.city, lb.city, b.asystent, b.klasa
            FROM bilet b
            INNER JOIN osoba o ON o.osoba_id = b.osoba_id
            INNER JOIN lot l ON l.lot_id = b.lot_id
            INNER JOIN samolot s ON l.samolot_id = s.samolot_id
            INNER JOIN miejsce m ON m.miejsce_id = b.miejsce_id
            INNER JOIN lotnisko la ON la.lotnisko_id = l.lotnisko_a_id
            INNER JOIN lotnisko lb ON lb.lotnisko_id = l.lotnisko_b_id
            WHERE b.bilet_id = ?;
            """
        )
        query.addBindValue(id)
        query.exec()
        query.next()
        name = f"{query.value(0)} {query.value(1)}"
        qt_datetime = query.value(2)
        datetime = qt_datetime.toString("yyyy-MM-dd HH:mm:ss")
        seat = query.value(3)
        plane = f"{query.value(4)}, {query.value(5)}"
        airport_a = f"{query.value(6)}"
        airport_b = f"{query.value(7)}"
        asystent = f"{query.value(8)}"
        klasa = f"{query.value(9)}"

        painter.drawText(100, 100, f"Passenger Name: {name}")
        painter.drawText(100, 300, f"Flight Details: {datetime}")
        painter.drawText(100, 500, f"From: {airport_a}")
        painter.drawText(100, 700, f"To: {airport_b}")
        painter.drawText(100, 900, f"Seat Number: {seat}")
        painter.drawText(100, 1100, f"Plane: {plane}")
        painter.drawText(100, 1300, f"Assistent: {asystent}")
        painter.drawText(100, 1500, f"Class: {klasa}")

        if klasa == "Economic":
            painter.drawText(100, 1900, "Price: 300$")
        else:
            painter.drawText(100, 1900, "Price: 1000$")

        painter.end()

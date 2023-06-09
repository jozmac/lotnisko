import psycopg2 as pg2
import sys

# pyuic6 -x lotnisko1.ui -o lotnisko1.py


class Osoba(object):
    def __init__(self, osoba_id=-1, imie="", nazwisko="", stanowisko=None):
        self.osoba_id = osoba_id
        self.imie = imie
        self.nazwisko = nazwisko
        self.stanowisko = stanowisko

    def load_osoba(self):
        cur.execute(
            f"""SELECT imie, nazwisko, stanowisko FROM osoba WHERE "osoba_id" = '{self.osoba_id}'; """)

        result = cur.fetchone()

        self.imie = result[0]
        self.nazwisko = result[1]
        self.stanowisko = result[2]

    def insert_osoba(self):
        cur.execute(f"""INSERT INTO osoba (imie, nazwisko, stanowisko) VALUES
        ('{self.imie}', '{self.nazwisko}', '{self.stanowisko}')""")
        db.commit()
        print(f"Osoba {self.osoba_id} został dodany")

    def delete_osoba(self):
        cur.execute(f"""DELETE FROM osoba 
                    WHERE osoba_id = {self.osoba_id}""")
        db.commit()

    def edit_osoba(self):
        cur.execute(f"""UPDATE osoba 
        SET imie = '{self.imie}', nazwisko = '{self.nazwisko}', stanowisko = '{self.stanowisko}'
        WHERE osoba_id = {self.osoba_id}""")
        db.commit()

    def __str__(self):
        return f"Id: {self.osoba_id}, Imię: {self.imie}, Nazwisko: {self.nazwisko}, Stanowisko: {self.stanowisko}"


# class Pracownik(Osoba):
#     def __init__(self, imie, nazwisko):
#         super().__init__(imie=imie, nazwisko=nazwisko)


class Bilet:
    def __init__(self, bilet_id=-1, osoba_id=-1, lot_id=-1, miejsce_id=-1, asystent=0):
        self.osoba_id = osoba_id
        self.bilet_id = bilet_id
        self.lot_id = lot_id
        self.miejsce_id = miejsce_id
        self.asystent = asystent

    def load_bilet(self):
        cur.execute(
            f"""SELECT osoba_id, lot_id, miejsce_id, asystent FROM bilet WHERE "bilet_id" = '{self.bilet_id}'; """)

        result = cur.fetchone()

        self.osoba_id = result[0]
        self.lot_id = result[1]
        self.miejsce_id = result[2]
        self.asystent = result[3]

    def insert_bilet(self):
        cur.execute(f"""INSERT INTO bilet (osoba_id, lot_id, miejsce_id, asystent) VALUES
        ('{self.osoba_id}', '{self.lot_id}', '{self.miejsce_id}', '{self.asystent}')""")
        db.commit()
        print(f"Bilet {self.bilet_id} został dodany")

    def delete_bilet(self):
        cur.execute(f"""DELETE FROM bilet
                    WHERE bilet_id = {self.bilet_id}""")
        db.commit()

    def edit_bilet(self):
        cur.execute(f"""UPDATE osoba 
        SET osoba_id = '{self.osoba_id}', lot_id = '{self.lot_id}', miejsce_id = '{self.miejsce_id}', asystent = '{self.asystent}'
        WHERE bilet_id = {self.bilet_id}""")
        db.commit()

    def __str__(self):
        return f"Id: {self.bilet_id}, osoba: {self.osoba_id}, lot: {self.lot_id}, miejsce: {self.miejsce_id}, asystent: {self.asystent}"


# class Samolot:
#     def __init__(self, samolot_id=-1, model="", ilosc_miejsc=""):
#         self.samolot_id = samolot_id
#         self.model = model
#         self.ilosc_miejsc = ilosc_miejsc

#     def load_samolot(self):
#         cur.execute(
#             f"""SELECT model, ilosc_miejsc FROM samolot WHERE "bilet_id" = '{self.samolot_id}'; """)

#         result = cur.fetchone()

#         self.model = result[0]
#         self.ilosc_miejsc = result[1]

#     def insert_samolot(self):
#         cur.execute(f"""INSERT INTO samolot (model, ilosc_miejsc) VALUES
#         ('{self.model}', '{self.ilosc_miejsc}')""")
#         db.commit()
#         print(f"Samolot {self.samolot_id} - {self.model} został dodany")

#     def delete_samolot(self):
#         cur.execute(f"""DELETE FROM bilet
#                     WHERE bilet_id = {self.samolot_id}""")
#         db.commit()

#     def edit_samolot(self):
#         cur.execute(f"""UPDATE osoba 
#         SET model = '{self.model}', ilosc_miejsc = '{self.ilosc_miejsc}'
#         WHERE bilet_id = {self.samolot_id}""")
#         db.commit()

#     def __str__(self):
#         return f"Id: {self.samolot_id}, model: {self.model}, ilosc miejsc: {self.ilosc_miejsc}"
    

class Lotnisko:
    def __init__(self, lotnisko_id=-1, icao="", miasto="", nazwa=""):
        self.id = lotnisko_id
        self.icao = icao
        self.miasto = miasto
        self.nazwa = nazwa

class Lot:
    pass


if __name__ == "__main__":

    try:
        db = pg2.connect(
            database="lotnisko",
            host="localhost",
            user='postgres',
            password='password',
            port='5432'
        )
        cur = db.cursor()
        print(db)
    except pg2.Error as e:
        # self.label_result.setText("Error")
        print(e)
        sys.exit(1)


    jan = Osoba(1, "Jan", "Kowalski", "Pilot")
    jozef = Osoba(osoba_id=33, imie="Jozef", nazwisko="Mackowiak", stanowisko="pilot")
    person = Osoba(osoba_id=7)
    person.load_osoba()
    # jozef.insert_osoba()
    # jozef.delete_osoba()
    jozef.insert_osoba()
    # print(person)
    # print(jan)
    # print(jozef)

    db.close()

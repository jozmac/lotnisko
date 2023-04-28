from functions import get_data, drop_tables, create_tables
import psycopg2 as pg2

# pyuic6 -x lotnisko1.ui -o lotnisko1.py

try:
    db = pg2.connect(
        database="lotnisko",
        host="localhost",
        user='postgres',
        password='password',
        port='5432'
    )
    print(db)
    cur = db.cursor()
except pg2.Error as e:
    # self.label_result.setText("Error")
    print(e)


class Konto(object):
    def __init__(self, konto_id=-1, imie="", nazwisko="", stanowisko=None):
        self.konto_id = konto_id
        self.imie = imie
        self.nazwisko = nazwisko
        self.stanowisko = stanowisko
        # self.connection =
        # self.cur = self.connection.cursor()

    def load_konto(self):
        # db = pg2.connect(
        #     database="lotnisko",
        #     host="localhost",
        #     user='postgres',
        #     password='password',
        #     port='5432'
        # )
        # self.cur = db.cursor()
        # self.cur.execute(f"""SELECT * FROM konto WHERE id = {self.konto_id}""") 
        cur.execute(f"""SELECT * FROM konto WHERE id = {self.konto_id}""") 

        # result = self.cur.fetchone()
        result = cur.fetchone()

        self.imie = result[1]
        self.nazwisko = result[2]
        self.stanowisko = result[3]

    def insert_konto(self):
        # self.connection = db
        # self.cur = self.connection.cursor()
        # self.cur.execute(f"""
        # INSERT INTO konto VALUES
        # {self.konto_id}, {self.imie}, {self.nazwisko}, {self.stanowisko}""")

        # self.connection.commit()
        # self.connection.close()
        pass

    def kup_bilet(self, amount):
        pass

    def __str__(self):
        return f"Id: {self.konto_id}, Imię: {self.imie}, Nazwisko: {self.nazwisko}, Stanowisko: {self.stanowisko}"


# class Pracownik(Osoba):
#     def __init__(self, imie, nazwisko):
#         super().__init__(imie=imie, nazwisko=nazwisko)


class Bilet:
    def __init__(self, bilet_id=-1, konto_id=-1, lot_id=-1, miejsce_id=-1, asystent=0):
        self.konto_id = konto_id
        self.bilet_id = bilet_id
        self.lot_id = lot_id
        self.miejsce_id = miejsce_id
        self.asystent = asystent


# class Purchase:
#     def __init__(self, osoba, lot, data):
#         self.osoba = osoba
#         self.lot = lot
#         self.data = data


class Samolot:
    def __init__(self, samolot_id=-1, model="", ilosc_miejsc=""):
        self.samolot_id = samolot_id
        self.model = model
        self.ilosc_miejsc = ilosc_miejsc
    

class Lotnisko:
    def __init__(self, lotnisko_id=-1, miasto="", nazwa=""):
        self.id = lotnisko_id
        self.miasto = miasto
        self.nazwa = nazwa

class Lot:
    pass


if __name__ == "__main__":
    jan = Konto(1, "Jan", "Kowalski", "Pilot")
    jozef = Konto(2, "Jozef", "Mackowiak")
    person = Konto(7)
    person.load_konto()
    # jozef.insert_konto()
    # jozef.load_konto(7)
    print(person)
    print(jan)
    print(jozef)

import psycopg2 as pg2
import sqlite3
import pandas as pd
import os

# https://manuelvanrijn.nl/blog/2012/01/18/convert-postgresql-to-sqlite/

# #  Making dump
# pg_dump -h host -U user -f database.dump database
# #  Making sqlite database
# pg2sqlite -d database.dump -o sqlite.db


# pg_dump --data-only --inserts lotnisko > lotnisko_dump.sql

# pg_dump -h localhost -U postgres -f lotnisko_database.dump lotnisko
# pg_dump -h localhost -U postgres --data-only --inserts lotnisko > lotnisko_dump.sql


class InitializeDatabase:
    def __init__(
        self,
        database_name="test_lotnisko",
        username="postgres",
        password="password",
        host="localhost",
        port=5432,
    ):
        self.database_name = database_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def create_connection(self):
        try:
            self.connection = pg2.connect(
                database=self.database_name,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
        except pg2.Error as e:
            print("Error connecting to the database:", e)

    def create_connection_sqlite(self):
        try:
            self.connection = sqlite3.connect("data\lotnisko.sqlite3")
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to the database:", e)

    # def clear_database(self):
    #     self.cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
    #     self.cursor.execute(f"CREATE DATABASE {self.database_name}")

    def drop_tables_pg(self):
        self.cursor.execute("DROP TABLE IF EXISTS osoba CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS samolot CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS zatrudnienie CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS lot CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS bilet CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS miejsce CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS lotnisko CASCADE")

    def drop_tables_sqlite(self):
        self.cursor.execute("DROP TABLE IF EXISTS osoba")
        self.cursor.execute("DROP TABLE IF EXISTS samolot")
        self.cursor.execute("DROP TABLE IF EXISTS zatrudnienie")
        self.cursor.execute("DROP TABLE IF EXISTS lot")
        self.cursor.execute("DROP TABLE IF EXISTS bilet")
        self.cursor.execute("DROP TABLE IF EXISTS miejsce")
        self.cursor.execute("DROP TABLE IF EXISTS lotnisko")

    def create_tables_pg(self):
        self.cursor.execute(
            """
            CREATE TABLE osoba (
            osoba_id SERIAL PRIMARY KEY,
            imie VARCHAR(255),
            nazwisko VARCHAR(255),
            stanowisko VARCHAR(255),
            password VARCHAR(255)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE samolot (
            samolot_id SERIAL PRIMARY KEY,
            model VARCHAR(255) NOT NULL,
            ilosc_miejsc INT NOT NULL
            );
            """
        )
        # self.cursor.execute(
        #     """
        #     CREATE TABLE lotnisko (
        #     icao_code CHAR(4),
        #     iata_code CHAR(3),
        #     name VARCHAR(50),
        #     city VARCHAR(50),
        #     country VARCHAR(50),
        #     lat_deg INT,
        #     lat_min INT,
        #     lat_sec INT,
        #     lat_dor CHAR(1),
        #     lon_deg INT,
        #     lon_min INT,
        #     lon_sec INT,
        #     lon_dir CHAR(1),
        #     altitude INT,
        #     lat_decimal DOUBLE PRECISION,
        #     lon_decimal DOUBLE PRECISION,
        #     lotnisko_id SERIAL PRIMARY KEY
        #     );
        #     """
        # )
        # data = pd.read_csv("C:\PycharmProjects\lotnisko\lotnisko.csv")
        # data.to_sql("lotnisko", self.connection, if_exists="replace", index=False)
        self.cursor.execute(
            """
            CREATE TABLE lotnisko (
            icao_code CHAR(4),
            name VARCHAR(50),
            city VARCHAR(50),
            country VARCHAR(50),
            lotnisko_id SERIAL PRIMARY KEY
            );
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lot (
                lot_id SERIAL PRIMARY KEY,
                samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
                lotnisko_a_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
                lotnisko_b_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
                bramka INTEGER NOT NULL,
                -- data DATETIME,
                cena FLOAT
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS zatrudnienie (
                osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
                lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
                PRIMARY KEY(osoba_id, lot_id)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS miejsce (
                miejsce_id SERIAL PRIMARY KEY,
                miejsce_samolot_id INTEGER NOT NULL,
                samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
                klasa_lotu VARCHAR(50),
                miejsce_samolot_name VARCHAR(50)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bilet (
                bilet_id SERIAL PRIMARY KEY,
                osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
                lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
                miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
                asystent BOOLEAN
            );
            """
        )

    def create_tables_sqlite(self):
        self.cursor.execute(
            """
            CREATE TABLE osoba (
            osoba_id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie VARCHAR(255),
            nazwisko VARCHAR(255),
            stanowisko VARCHAR(255),
            password VARCHAR(255)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE samolot (
            samolot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model VARCHAR(255) NOT NULL,
            ilosc_miejsc INT NOT NULL
            );
            """
        )
        # self.cursor.execute(
        #     """
        #     CREATE TABLE lotnisko (
        #     icao_code CHAR(4),
        #     iata_code CHAR(3),
        #     name VARCHAR(50),
        #     city VARCHAR(50),
        #     country VARCHAR(50),
        #     lat_deg INT,
        #     lat_min INT,
        #     lat_sec INT,
        #     lat_dor CHAR(1),
        #     lon_deg INT,
        #     lon_min INT,
        #     lon_sec INT,
        #     lon_dir CHAR(1),
        #     altitude INT,
        #     lat_decimal DOUBLE PRECISION,
        #     lon_decimal DOUBLE PRECISION,
        #     lotnisko_id INTEGER PRIMARY KEY AUTOINCREMENT
        #     );
        #     """
        # )
        # data = pd.read_csv("C:\PycharmProjects\lotnisko\lotnisko.csv")
        # data.to_sql("lotnisko", self.connection, if_exists="replace", index=False)
        self.cursor.execute(
            """
            CREATE TABLE lotnisko (
            icao_code CHAR(4),
            name VARCHAR(50),
            city VARCHAR(50),
            country VARCHAR(50),
            lotnisko_id INTEGER PRIMARY KEY AUTOINCREMENT
            );
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lot (
                lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
                lotnisko_a_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
                lotnisko_b_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
                bramka INTEGER NOT NULL,
                -- data DATETIME,
                cena FLOAT
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS zatrudnienie (
                osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
                lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
                PRIMARY KEY(osoba_id, lot_id)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS miejsce (
                miejsce_id INTEGER PRIMARY KEY AUTOINCREMENT,
                miejsce_samolot_id INTEGER NOT NULL,
                samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
                klasa_lotu VARCHAR(50),
                miejsce_samolot_name VARCHAR(50)
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bilet (
                bilet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
                lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
                miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
                asystent BOOLEAN
            );
            """
        )

    def create_sequences(self):
        self.cursor.execute(
            """CREATE SEQUENCE IF NOT EXISTS bilet_bilet_id_seq INCREMENT 1 START 1"""
        )
        self.cursor.execute(
            """CREATE SEQUENCE IF NOT EXISTS lot_lot_id_seq INCREMENT 1 START 1"""
        )
        self.cursor.execute(
            """CREATE SEQUENCE IF NOT EXISTS lotnisko_id_seq INCREMENT 1 START 1"""
        )
        self.cursor.execute(
            """CREATE SEQUENCE IF NOT EXISTS miejsce_miejsce_id_seq INCREMENT 1 START 1"""
        )
        self.cursor.execute(
            """CREATE SEQUENCE IF NOT EXISTS osoba_id_seq INCREMENT 1 START 1"""
        )

    def insert_data(self):
        self.cursor.execute(
            """
            INSERT INTO osoba (imie, nazwisko, stanowisko)
            VALUES 
            ('Bruce', 'Willis', NULL),
            ('George', 'Clooney', NULL),
            ('Kevin', 'Costner', NULL),
            ('Donald', 'Sutherland', NULL),
            ('Jennifer', 'Lopez', NULL),
            ('Ray', 'Liotta', NULL),
            ('Samuel L.', 'Jackson', NULL),
            ('Nikole', 'Kidman', NULL),
            ('Alan', 'Rickman', NULL),
            ('Kurt', 'Russell', NULL),
            ('Harrison', 'Ford', NULL),
            ('Russell', 'Crowe', NULL),
            ('Steve', 'Martin', NULL),
            ('Michael', 'Caine', NULL),
            ('Angelina', 'Jolie', NULL),
            ('Mel', 'Gibson', NULL),
            ('Michael', 'Douglas', NULL),
            ('John', 'Travolta', NULL),
            ('Sylvester', 'Stallone', NULL),
            ('Tommy Lee', 'Jones', NULL),
            ('Catherine', 'Zeta-Jones', NULL),
            ('Antonio', 'Banderas', NULL),
            ('Kim', 'Basinger', NULL),
            ('Sam', 'Neill', NULL),
            ('Gary', 'Oldman', NULL),
            ('Clint', 'Eastwood', NULL),
            ('Brad', 'Pitt', NULL),
            ('Johnny', 'Depp', NULL),
            ('Pierce', 'Brosnan', NULL),
            ('Sean', 'Connery', NULL), 
            ('Mullah', 'Omar', NULL);
            """
        )
        self.cursor.execute(
            """
            INSERT INTO samolot (samolot_id, model, ilosc_miejsc)
            VALUES
            (1, 'Boeing 737', 120),
            (2, 'Airbus A320', 150),
            (3, 'Boeing 777', 300),
            (4, 'Embraer E175', 80),
            (5, 'Bombardier CRJ900', 90),
            (6, 'Airbus A321', 200),
            (7, 'Boeing 767', 250),
            (8, 'Airbus A319', 134),
            (9, 'Boeing 747', 416),
            (10, 'Embraer E195', 124);
            """
        )
        self.connection.commit()
        self.cursor.execute("SELECT samolot_id, ilosc_miejsc FROM samolot")
        planes = self.cursor.fetchall()
        for plane_id, capacity in planes:
            for seat_id in range(1, capacity + 1):
                self.cursor.execute(
                    f"INSERT INTO miejsce (miejsce_samolot_id, samolot_id) VALUES ({seat_id}, {plane_id})"
                )

        self.cursor.execute(
            """
            INSERT INTO lotnisko (icao_code, name, city, country, lotnisko_id) 
            VALUES 
            ('EPBC', 'N/A', 'WARSAW', 'POLAND', 1522),
            ('EPBK', 'N/A', 'BIALYSTOK', 'POLAND', 1523),
            ('EPGD', 'REBIECHOWO', 'GDANSK', 'POLAND', 1524),
            ('EPGI', 'N/A', 'GRUDZIADZ', 'POLAND', 1525),
            ('EPJG', 'N/A', 'JELENIA GORA', 'POLAND', 1526),
            ('EPKA', 'N/A', 'KIELCE', 'POLAND', 1527),
            ('EPKE', 'N/A', 'KETRZYN', 'POLAND', 1528),
            ('EPKK', 'BALICE JP II INTERNATIONAL AIRPORT', 'KRAKOW', 'POLAND', 1529),
            ('EPKM', 'MUCHOWIEC', 'KATOWICE', 'POLAND', 1530),
            ('EPKO', 'ZEGRZE POMORSKIE', 'KOSZALIN', 'POLAND', 1531),
            ('EPKR', 'N/A', 'KROSNO', 'POLAND', 1532),
            ('EPKT', 'PYRZOWICE', 'KATOWICE', 'POLAND', 1533),
            ('EPLL', 'LUBLINEK', 'LODZ', 'POLAND', 1534),
            ('EPLS', 'N/A', 'LESZNO', 'POLAND', 1535),
            ('EPML', 'MIELEC', 'MIELEC', 'POLAND', 1536),
            ('EPNT', 'N/A', 'NOWY TARG', 'POLAND', 1537),
            ('EPOD', 'N/A', 'OLSZTYN', 'POLAND', 1538),
            ('EPPO', 'LAWICA', 'POZNAN', 'POLAND', 1539),
            ('EPPT', 'N/A', 'PITRKOWTRYBUNALAKY', 'POLAND', 1540),
            ('EPRG', 'N/A', 'RYBNIK', 'POLAND', 1541),
            ('EPRZ', 'JASIONKA', 'RZESZOW', 'POLAND', 1542),
            ('EPSC', 'GOLENIOW', 'SZCZECHIN', 'POLAND', 1543),
            ('EPSD', 'DABIE', 'SZCZECHIN', 'POLAND', 1544),
            ('EPSK', 'REDZIKOWO', 'SLUPSK', 'POLAND', 1545),
            ('EPSN', 'SWIDWIN', 'SHAPAJA', 'PERU', 1546),
            ('EPSW', 'N/A', 'SWIDNIK', 'POLAND', 1547),
            ('EPVN', 'N/A', 'VILA DAS NEVES', 'SAO TOME & PRINCIPE', 1548),
            ('EPWA', 'OKECIE', 'WARSAW', 'POLAND', 1549),
            ('EPWR', 'STRACHOWICE', 'WROCLAW', 'POLAND', 1550),
            ('EPZG', 'BABIMOST', 'ZIELONA GORA', 'POLAND', 1551),
            ('EPZP', 'N/A', 'ZILONA GORA', 'POLAND', 1552),
            ('EPZR', 'N/A', 'ZAR', 'POLAND', 1553);
            """
        )

    def create_indexes(self):
        # self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(lotnisko_id, city);")
        self.cursor.execute("CREATE INDEX idx_samolot ON samolot(samolot_id);")
        self.cursor.execute("CREATE INDEX idx_samolot ON samolot(model);")
        self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(lotnisko_id);")
        self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(city);")
        # self.cursor.execute("CREATE INDEX idx_lot_lotnisko_a_id ON lot(lotnisko_a_id);")
        # self.cursor.execute("CREATE INDEX idx_lot_lotnisko_b_id ON lot(lotnisko_b_id);")

    def insert_seat_names(self):
        self.connection.commit()

        self.seat_columns_count = 6

        self.cursor.execute("SELECT miejsce_id, miejsce_samolot_id FROM miejsce")
        seat_ids = self.cursor.fetchall()

        for seat_id, seat_plane_id in seat_ids:
            row_number = int(seat_plane_id / self.seat_columns_count) + 1
            seat_letter = chr((seat_plane_id - 1) % self.seat_columns_count + 65)
            seat_name = f"{row_number}{seat_letter}"
            # print(f"{seat_id} - {seat_plane_id} - {seat_name}")
            self.cursor.execute(
                f"UPDATE miejsce SET miejsce_samolot_name = '{seat_name}' WHERE miejsce_id = {seat_id};"
            )

    def initialize(self):
        self.create_connection()
        self.drop_tables_pg()
        self.create_tables_pg()
        self.create_sequences()
        self.insert_data()
        self.create_indexes()
        self.connection.commit()
        self.connection.close()

    def initialize_sqlite(self):
        self.create_connection_sqlite()
        self.drop_tables_sqlite()
        self.create_tables_sqlite()
        # self.create_sequences()
        self.insert_data()
        # self.create_indexes()
        self.insert_seat_names()
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    dbinit = InitializeDatabase()
    dbinit.initialize_sqlite()

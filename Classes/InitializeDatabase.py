import psycopg2 as pg2
import pandas as pd
import os


class InitializeDatabase:
    def __init__(self, database_name):
        self.database_name = database_name

    def create_connection(self):
        try:
            self.connection = pg2.connect(
                database=self.database_name,
                host="localhost",
                user="postgres",
                password="password",
                port="5432",
            )
            self.cursor = self.connection.cursor()
        except pg2.Error as e:
            print("Error connecting to the database:", e)

    # def clear_database(self):
    #     self.cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
    #     self.cursor.execute(f"CREATE DATABASE {self.database_name}")

    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS osoba CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS samolot CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS zatrudnienie CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS lot CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS bilet CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS miejsce CASCADE")
        self.cursor.execute("DROP TABLE IF EXISTS lotnisko CASCADE")

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE osoba (
            osoba_id SERIAL PRIMARY KEY,
            imie VARCHAR(255),
            nazwisko VARCHAR(255),
            stanowisko VARCHAR(255)
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
                klasa_lotu VARCHAR(50)
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
            INSERT INTO lotnisko (icao_code, name, city, country)
            VALUES 
            ('EPPO', 'LAWICA', 'POZNAN', 'POLAND'),
            ('EPPT', 'N/A', 'PITRKOWTRYBUNALAKY', 'POLAND')
            """
        )
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
        self.cursor.execute("SELECT samolot_id, ilosc_miejsc FROM samolot")
        planes = self.cursor.fetchall()
        print(planes)
        for plane in planes:
            plane_id = plane[0]
            capacity = plane[1]
            for j in range(1, capacity + 1):
                self.cursor.execute(
                    "INSERT INTO miejsce (miejsce_samolot_id, samolot_id) VALUES (%s, %s)",
                    (j, plane_id),
                )
                print(j)

    def create_indexes(self):
        # self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(lotnisko_id, city);")
        self.cursor.execute("CREATE INDEX idx_samolot ON samolot(samolot_id);")
        self.cursor.execute("CREATE INDEX idx_samolot ON samolot(model);")
        self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(lotnisko_id);")
        self.cursor.execute("CREATE INDEX idx_lotnisko ON lotnisko(city);")
        # self.cursor.execute("CREATE INDEX idx_lot_lotnisko_a_id ON lot(lotnisko_a_id);")
        # self.cursor.execute("CREATE INDEX idx_lot_lotnisko_b_id ON lot(lotnisko_b_id);")

    def initialize(self):
        self.create_connection()
        self.drop_tables()
        self.create_tables()
        self.create_sequences()
        self.insert_data()
        self.create_indexes()
        self.connection.commit()
        self.connection.close()

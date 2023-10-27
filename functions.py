import psycopg2 as pg2

try:
    db = pg2.connect(
        database="lotnisko",
        host="localhost",
        user="postgres",
        password="password",
        port="5432",
    )
    print(db)
    cur = db.cursor()
except pg2.Error as e:
    # self.label_result.setText("Error")
    print(e)
# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     # cur.close()
#     # db.commit()
#     db.close()


def drop_tables():
    cur.execute("DROP TABLE IF EXISTS osoba CASCADE")
    cur.execute("DROP TABLE IF EXISTS samolot CASCADE")
    cur.execute("DROP TABLE IF EXISTS lotnisko CASCADE")
    cur.execute("DROP TABLE IF EXISTS zatrudnienie CASCADE")
    cur.execute("DROP TABLE IF EXISTS lot CASCADE")
    cur.execute("DROP TABLE IF EXISTS bilet CASCADE")
    cur.execute("DROP TABLE IF EXISTS miejsce CASCADE")
    # cur.execute("DROP TABLE IF EXISTS zajete_miejsce CASCADE")
    db.commit()


def create_tables():
    auto_commit = pg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    db.set_isolation_level(auto_commit)

    cur.execute(
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS zatrudnienie (
            osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
            lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
            PRIMARY KEY(osoba_id, lot_id)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS miejsce (
            miejsce_id SERIAL PRIMARY KEY,
            miejsce_samolot_id INTEGER NOT NULL,
            samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
            klasa_lotu VARCHAR(50)
        );
        """
    )
    cur.execute(
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS zajete_miejsce (
            lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
            miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
            bilet_id INTEGER NOT NULL REFERENCES bilet(bilet_id),
            PRIMARY KEY(lot_id, miejsce_id, bilet_id)
        );
        """
    )
    db.commit()


def reset_sequences():
    # SELECT nextval('your_table_id_seq');
    cur.execute("""SELECT setval('bilet_bilet_id_seq', 1);""")
    cur.execute("""SELECT setval('lot_lot_id_seq', 1);""")
    cur.execute("""SELECT setval('lotnisko_id_seq', 1);""")
    cur.execute("""SELECT setval('miejsce_miejsce_id_seq', 1);""")
    cur.execute("""SELECT setval('osoba_id_seq', 1);""")


def insert_into_tables():
    cur.execute(
        """
        CREATE TABLE osoba (
        osoba_id SERIAL PRIMARY KEY,
        imie VARCHAR(255),
        nazwisko VARCHAR(255),
        stanowisko VARCHAR(255)
        );
        """
    )
    cur.execute(
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
        ('Bruce', 'Willis', NULL), 
        ('Mullah', 'Omar', NULL);
        """
    )
    cur.execute(
        """
        CREATE TABLE samolot (
        samolot_id INT PRIMARY KEY,
        model VARCHAR(255) NOT NULL,
        ilosc_miejsc INT NOT NULL
        );
        """
    )
    cur.execute(
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
    db.commit()


def insert_miejsca():
    # Select all planes from the planes table
    cur.execute("SELECT samolot_id, ilosc_miejsc FROM samolot")
    planes = cur.fetchall()
    print(planes)

    # Insert seat information into the seats table based on the capacities of the planes
    for plane in planes:
        plane_id = plane[0]
        capacity = plane[1]
        for j in range(1, capacity + 1):
            cur.execute(
                "INSERT INTO miejsce (miejsce_samolot_id, samolot_id) VALUES (%s, %s)",
                (j, plane_id),
            )
            print(j)
    db.commit()


def delete_seats():
    cur.execute("DELETE FROM miejsce")
    db.commit()


def create_indexes():
    # cur.execute("CREATE INDEX osoba_imie_nazwisko ON osoba (imie, nazwisko)")
    # cur.execute("CREATE INDEX lot_samolot_id ON lot (samolot_id)")
    # cur.execute("CREATE INDEX lot_lotnisko_ids ON lot (lotnisko_a_id, lotnisko_b_id)")
    # cur.execute("CREATE INDEX miejsce_samolot_id ON miejsce (samolot_id)")
    cur.execute("CREATE INDEX lot_lotnisko_ids ON lot (lotnisko_a_id, lotnisko_b_id)")


# def get_data():

#     cur.execute("SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba")
#     osoba = cur.fetchall()

#     cur.execute("""
#                 SELECT lotnisko_id, icao_code, name, city, country
#                 FROM lotnisko
#                 -- WHERE name LIKE 'LAWICA'
#                 -- WHERE name NOT LIKE 'N/A'
#                 """)
#     lotnisko = cur.fetchall()

#     cur.execute("SELECT samolot_id, model, ilosc_miejsc FROM samolot")
#     samolot = cur.fetchall()

#     return osoba, lotnisko, samolot


# def select_osoba():
#     cur.execute("SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba")
#     osoba = cur.fetchall()
#     return osoba


# def select_lotnisko():
#     cur.execute("""
#                 SELECT lotnisko_id, icao_code, name, city, country
#                 FROM lotnisko
#                 -- WHERE name LIKE 'LAWICA'
#                 -- WHERE name NOT LIKE 'N/A'
#                 """)
#     lotnisko = cur.fetchall()
#     return lotnisko


# def select_samolot():
#     cur.execute("SELECT samolot_id, model, ilosc_miejsc FROM samolot")
#     samolot = cur.fetchall()
#     return samolot

# def select_bilet():
#     cur.execute("SELECT bilet_id, osoba_id, lot_id, miejsce_id, asystent FROM bilet")
#     bilet = cur.fetchall()
#     return bilet

# def select_lot():
#     cur.execute("SELECT lot_id, samolot_id, lotnisko_a_id, lotnisko_b_id, datetime FROM lot")
#     lot = cur.fetchall()
#     return lot

# def select_miejsce():
#     cur.execute("SELECT miejsce_id, samolot_id FROM miejsce")
#     miejsce = cur.fetchall()
#     return miejsce

# def select_zajete_miejsce():
#     cur.execute("SELECT lot_id, miejsce_id, bilet_id FROM zajete_miejsce")
#     zajete_miejsce = cur.fetchall()
#     return zajete_miejsce

# def select_zatrudnienie():
#     cur.execute("SELECT osoba_id, lot_id FROM zatrudnienie")
#     zatrudnienie = cur.fetchall()
#     return zatrudnienie

# def select_pracownik():
#     cur.execute("SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba WHERE stanowisko IS NOT NULL")
#     zatrudnienie = cur.fetchall()
#     return zatrudnienie


# drop_tables()
# create_tables()
# insert_miejsca()

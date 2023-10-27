import psycopg2 as pg2

database_name = "test_lotnisko"

try:
    db = pg2.connect(
        database=database_name,
        host="localhost",
        user="postgres",
        password="password",
        port="5432",
    )
    print(db)
    cur = db.cursor()
except pg2.Error as e:
    print(e)

auto_commit = pg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
db.set_isolation_level(auto_commit)


cur.execute("DROP DATABASE IF EXISTS (%s,)", (database_name,))

cur.execute("CREATE DATABASE (%s,)", (database_name,))

# cur.execute("DROP TABLE IF EXISTS osoba CASCADE")
# cur.execute("DROP TABLE IF EXISTS samolot CASCADE")

# cur.execute("DROP TABLE IF EXISTS zatrudnienie CASCADE")
# cur.execute("DROP TABLE IF EXISTS lot CASCADE")
# cur.execute("DROP TABLE IF EXISTS bilet CASCADE")
# cur.execute("DROP TABLE IF EXISTS miejsce CASCADE")
# cur.execute("DROP TABLE IF EXISTS zajete_miejsce CASCADE")

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

cur.execute("""SELECT setval('bilet_bilet_id_seq', 1);""")
cur.execute("""SELECT setval('lot_lot_id_seq', 1);""")
cur.execute("""SELECT setval('lotnisko_id_seq', 1);""")
cur.execute("""SELECT setval('miejsce_miejsce_id_seq', 1);""")
cur.execute("""SELECT setval('osoba_id_seq', 1);""")

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

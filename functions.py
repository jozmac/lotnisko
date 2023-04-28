import psycopg2 as pg2

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
# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     # cur.close()
#     # db.commit()
#     db.close()


def drop_tables():
    cur.execute("DROP TABLE IF EXISTS zatrudnienie CASCADE")
    cur.execute("DROP TABLE IF EXISTS lot CASCADE")
    cur.execute("DROP TABLE IF EXISTS bilet CASCADE")
    cur.execute("DROP TABLE IF EXISTS miejsce CASCADE")
    cur.execute("DROP TABLE IF EXISTS zajete_miejsce CASCADE")
    db.commit()


def create_tables():

    auto_commit = pg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    db.set_isolation_level(auto_commit)

    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS lot (
    #         lot_id SERIAL PRIMARY KEY,
    #         samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
    #         lotnisko_a_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
    #         lotnisko_b_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
    #         bramka INTEGER NOT NULL,
    #         -- data DATETIME,
    #         cena FLOAT
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS zatrudnienie (
    #         osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
    #         lot_id INTEGER NOT NULL REFERENCES lot(lot_id)
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS miejsce (
    #         samolot_id SERIAL PRIMARY KEY,
    #         samolot_id INTEGER NOT NULL REFERENCES samolot(id),
    #         klasa_lotu VARCHAR(50)
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS bilet (
    #         bilet_id SERIAL PRIMARY KEY,
    #         osoba_id INTEGER NOT NULL REFERENCES osoba(id),
    #         lot_id INTEGER NOT NULL REFERENCES lot(id),
    #         miejsce_id INTEGER NOT NULL REFERENCES miejsce(id),
    #         asystent BOOLEAN
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS zajete_miejsce (
    #         lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
    #         miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
    #         bilet_id INTEGER NOT NULL REFERENCES bilet(bilet_id)
    #     );
    #     """
    # )
    # db.commit()


    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS lot (
    #         lot_id SERIAL PRIMARY KEY,
    #         fk_samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
    #         fk_lotnisko_a_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
    #         fk_lotnisko_b_id INTEGER NOT NULL REFERENCES lotnisko(lotnisko_id),
    #         bramka INTEGER NOT NULL,
    #         -- data DATETIME,
    #         cena FLOAT
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS zatrudnienie (
    #         fk_osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
    #         fk_lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
    #         PRIMARY KEY(fk_osoba_id, fk_lot_id)
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS miejsce (
    #         miejsce_id SERIAL PRIMARY KEY,
    #         fk_samolot_id INTEGER NOT NULL REFERENCES samolot(samolot_id),
    #         klasa_lotu VARCHAR(50)
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS bilet (
    #         bilet_id SERIAL PRIMARY KEY,
    #         fk_osoba_id INTEGER NOT NULL REFERENCES osoba(osoba_id),
    #         fk_lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
    #         fk_miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
    #         asystent BOOLEAN
    #     );
    #     """
    # )
    # cur.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS zajete_miejsce (
    #         fk_lot_id INTEGER NOT NULL REFERENCES lot(lot_id),
    #         fk_miejsce_id INTEGER NOT NULL REFERENCES miejsce(miejsce_id),
    #         fk_bilet_id INTEGER NOT NULL REFERENCES bilet(bilet_id),
    #         PRIMARY KEY(fk_lot_id, fk_miejsce_id, fk_bilet_id)
    #     );
    #     """
    # )
    # db.commit()



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


def get_data():

    cur.execute("SELECT osoba_id, imie, nazwisko, stanowisko FROM osoba")
    osoba = cur.fetchall()

    cur.execute("""
                SELECT lotnisko_id, name, city, country
                FROM lotnisko
                -- WHERE name LIKE 'LAWICA'
                -- WHERE name NOT LIKE 'N/A'
                """)
    lotnisko = cur.fetchall()

    cur.execute("SELECT samolot_id, model, ilosc_miejsc FROM samolot")
    samolot = cur.fetchall()

    return osoba, lotnisko, samolot


# def get_data(table_name):
#
#     cur.execute(f"SELECT osoba_id, imie, nazwisko, stanowisko FROM {table_name}")
#     return cur.fetchall()







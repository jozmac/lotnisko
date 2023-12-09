from classes.initialize_database import InitializeDatabase
import bcrypt

database_name = "lotnisko"
username = "postgres"
password = "password"
host = "localhost"
port = 5432


class InitDb(InitializeDatabase):
    def __init__(self, database_name, username, password, host, port):
        super().__init__(database_name, username, password, host, port)

    def insert_seat_names(self):
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

    def insert_passwords(self):
        self.connection.commit()
        self.cursor.execute("SELECT osoba_id, imie FROM osoba")
        person = self.cursor.fetchall()
        for id, name in person:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(name.encode("utf-8"), salt)
            hashed = hashed.decode("utf-8")
            salt = salt.decode("utf-8")
            print(f"id: {id}, name: {name}, hash: {hashed}, salt: {salt}")
            self.cursor.execute(
                f"UPDATE osoba SET password_hash = '{hashed}', salt = '{salt}' WHERE osoba_id = {id};"
            )


if __name__ == "__main__":
    init_db = InitDb(database_name, username, password, host, port)
    init_db.create_connection()
    # init_db.insert_seat_names()
    init_db.insert_passwords()
    init_db.connection.commit()
    init_db.connection.close()

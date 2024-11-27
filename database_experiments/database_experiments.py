import sqlite3


class DatabaseOperator:

    def __init__(self, db_name: str) -> None:
        # Connect to the SQLite database file
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_record(self):
        self.cursor.execute(" SELECT * FROM person; ")
        records = self.cursor.fetchall()
        return records

    def add_record(self, first_name, last_name, age, city):
        self.cursor.execute("INSERT INTO person (first_name, last_name, age, city) VALUES (?, ?, ?, ?);",
                            (first_name, last_name, age, city))
        self.conn.commit()

    def get_record_by_id(self, id):
        pass

    def update_record(self, id, new_first_name, new_last_name, new_age, new_city):
        self.cursor.execute("UPDATE person SET first_name = ?, last_name = ?, age = ?, city = ? WHERE id = ?;",
                            (new_first_name, new_last_name, new_age, new_city, id))
        self.conn.commit()

    def delete_record(self, person_id):
        self.cursor.execute("DELETE FROM person WHERE id = ?;", (person_id,))
        self.conn.commit()

    def close_connection(self):
        # Close the connection when done
        self.conn.close()

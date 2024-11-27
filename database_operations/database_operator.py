import sqlite3


class DatabaseOperator:

    def __init__(self, db_name: str) -> None:
        # Connect to the SQLite database file
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_record(self):
        self.cursor.execute(" SELECT * FROM employees; ")
        records = self.cursor.fetchall()
        return records

    def add_record(self, first_name, last_name, email, role, department, hire_date, leave_date, monday_access, 
                jira_access, slack_access):
        self.cursor.execute(
            "INSERT INTO employees (first_name, last_name, email, role, department, hire_date, leave_date, monday_access, jira_access, slack_access) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (first_name, last_name, email, role, department, hire_date, leave_date, monday_access, 
            jira_access, slack_access))
        self.conn.commit()

    def get_record_by_id(self, id):
        self.cursor.execute("SELECT * FROM employees WHERE id = ?;", (id,))
        record = self.cursor.fetchone()
        return record

    def update_record(self, id, new_first_name, new_last_name, new_email, new_role, new_department, new_hire_date, 
                    new_leave_date, new_monday_access, new_jira_access, new_slack_access):
        self.cursor.execute(
            "UPDATE employees SET first_name = ?, last_name = ?, email = ?, role = ?, department = ?, hire_date = ?, leave_date = ?, monday_access = ?, jira_access = ?, slack_access = ? WHERE id = ?;",
            (new_first_name, new_last_name, new_email, new_role, new_department, new_hire_date, new_leave_date,
            new_monday_access, new_jira_access, new_slack_access, id))
        self.conn.commit()

    def delete_record(self, person_id):
        self.cursor.execute("DELETE FROM employees WHERE id = ?;", (person_id,))
        self.conn.commit()

    def close_connection(self):
        # Close the connection when done
        self.conn.close()

import sqlite3
import random
from datetime import date, timedelta

from faker import Faker
import numpy as np

from database_operations.database_operator import DatabaseOperator

# Layout Ideas:
# first_name, last_name, email, role, department, hire_date, leave_date, monday_access, jira_access, slack_access.

# DBWorker class will have methods to handle the creation of the database
# and will handle the database interactions - CREATE, INSERT, SELECT, UPDATE (CRUD)


class DBWorker(DatabaseOperator):
    def __init__(self, db_path="../data/employees.db"):
        super().__init__(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.fake = Faker()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                role TEXT,
                department TEXT,
                hire_date TEXT,
                leave_date TEXT,
                monday_access INTEGER,
                jira_access INTEGER,
                slack_access INTEGER
            )
        ''')
        self.conn.commit()

    def add_single_employee(self, first_name, last_name, email, role, department, hire_date, leave_date, monday_access,
                            jira_access, slack_access):
        self.cursor.execute('''
            INSERT INTO employees (first_name, last_name, email, role, department, hire_date, leave_date, monday_access, 
            jira_access, slack_access)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, role, department, hire_date, leave_date, monday_access,
              jira_access, slack_access))
        self.conn.commit()

    # Method to create multiple employees using the add_single_employee method, we can specify how many records to
    # generate, with a default of 50
    def add_fake_employees(self, number_of_employees=50):

        for _ in range(number_of_employees):
            hire_date = self.fake.date_between(date(1990, 1, 1), date.today() - timedelta(days=365))
            leave_date = np.random.choice([self.fake.date_between(hire_date, date.today()), "Still Working"],
                                          2, p=[0.375, 0.625])

            self.add_single_employee(
                self.fake.first_name(),
                self.fake.last_name(),
                self.fake.email(),
                str.capitalize(random.choice(["software engineer", "devops engineer", "manager", "maintenance"])),
                str.capitalize(random.choice(["product delivery", "broadband", "sky glass", "mobile"])),
                str(hire_date),
                str(leave_date[0]),
                self.fake.random_int(0, 1),  # Monday
                self.fake.random_int(0, 1),  # Jira
                self.fake.random_int(0, 1)   # Slack
            )

    # Fetch all employees from db
    def get_employees(self):
        self.cursor.execute('''
            SELECT * FROM employees
        ''')
        return self.cursor.fetchall()

    # Fetch employee by ID
    def get_an_employee(self, employee_id):
        try:
            self.cursor.execute('''
                SELECT * FROM employees WHERE id = ?
            ''', (employee_id,))

            return self.cursor.fetchone()
        except sqlite3.Error as e:
            return None

    # Update employee - Note: Need to figure out the best way to handle just updating a single field such
    # as changes to just email or phone number
    def update_employee(self, employee_id, first_name, last_name, email, role, department, hire_date, leave_date,
                        monday_access, jira_access, slack_access):

        self.cursor.execute('''
            UPDATE employees
            SET first_name = ?, last_name = ?, email = ?, role = ?, department = ?, hire_date = ?, 
            leave_date = ?, monday_access = ?, jira_access = ?, slack_access = ? WHERE id = ?''',
                            (first_name, last_name, email, role, department, hire_date, leave_date,
                             monday_access, jira_access, slack_access, employee_id))

        self.conn.commit()
        return True

    def get_max_id(self):
        self.cursor.execute('''
            SELECT MAX(id) FROM employees
        ''')
        return self.cursor.fetchone()[0]

    # Dynamic creation of Employee intermediary class objects - needed to represent the data in the view
    def get_table_schema(self, cursor, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return {row[1]: row[2] for row in cursor.fetchall()}

    def create_class_from_table(self, cursor, table_name):
        schema = self.get_table_schema(cursor, table_name)
        class_name = table_name.capitalize()
        return type(class_name, (object,), schema)

    def fetch_objects(self, class_, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        objects = []
        for row in rows:
            obj = class_()
            for col, val in zip(class_.__dict__.keys(), row):
                match col.lower():
                    case "monday_access":
                        setattr(obj, col, bool(val))
                    case "jira_access":
                        setattr(obj, col, bool(val))
                    case "slack_access":
                        setattr(obj, col, bool(val))
                    case "leave_date":
                        setattr(obj, col, val)
                        if not val == "Still Working":
                            date_tup = tuple(map(int, val.split("-")))
                            date_left = date(*date_tup)
                            setattr(obj, "days_since_leave", (date.today() - date_left).days)
                        else:
                            setattr(obj, "days_since_leave", 0)
                        # time since leave
                    case _:
                        setattr(obj, col, val)
            objects.append(obj)
        return objects

    def fetch_an_employee_to_object(self, class_, employee_id):
        self.cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = self.cursor.fetchone()
        obj = class_()
        for col, val in zip(class_.__dict__.keys(), row):
            match col.lower():
                case "monday_access":
                    setattr(obj, col, bool(val))
                case "jira_access":
                    setattr(obj, col, bool(val))
                case "slack_access":
                    setattr(obj, col, bool(val))
                case "leave_date":
                    setattr(obj, col, val)
                    if not val == "Still Working":
                        date_tup = tuple(map(int, val.split("-")))
                        date_left = date(*date_tup)
                        setattr(obj, "days_since_leave", (date.today() - date_left).days)
                    else:
                        setattr(obj, "days_since_leave", 0)
                    # time since leave
                case _:
                    setattr(obj, col, val)
        return obj

    def delete_employee(self, employee_id):
        self.cursor.execute('''
            DELETE FROM employees WHERE id = ?
        ''', (employee_id,))
        self.conn.commit()
        return True

    def restrict_access(self, employee_id, access_type):
        self.cursor.execute(f'''
            UPDATE employees
            SET {access_type} = 0 WHERE id = ?
        ''', (employee_id,))
        self.conn.commit()
        return True

    def delete_table(self):
        self.cursor.execute('''
            DROP TABLE IF EXISTS employees
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
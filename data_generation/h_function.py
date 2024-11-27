import random
import sqlite3
from datetime import date, timedelta
from faker import Faker
import numpy as np

fake = Faker()


def generate_data(records_generate=400):
  fake = Faker()
  people_data = []

  for i in range(records_generate):
    hire_date = fake.date_between(date(1990, 1, 1), date.today() - timedelta(days=365))
    leave_date = np.random.choice([fake.date_between(hire_date, date.today()), "Still Working"], 
                                  2, p=[0.25, 0.75])

    person = {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "email": fake.email(),
        "role": random.choice(["software engineer", "devops engineer", "manager", "maintenance"]),
        "department": random.choice(["product delivery", "broadband", "sky glass", "mobile"]),
        "hire_date": str(hire_date),
        "leave_date": str(leave_date[0]),
        "monday_ac": random.randint(0,1),
        "jira_ac": random.randint(0,1),
        "slack_ac": random.randint(0,1)
    }

    people_data.append(person)
    
  return people_data



def create_sqlite_db(data, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor() 

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS Employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, surname text, email text, role text, department text, hire_date text, leave_date text, monday_ac bool, jira_ac bool, slack_ac bool)''')

    # Insert data
    c.executemany('''INSERT INTO Employees (name, surname, email, role, department, hire_date, leave_date, monday_ac, jira_ac, slack_ac) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                [(person["name"], person["surname"], person["email"], person["role"], person["department"], person["hire_date"], person["leave_date"], person["monday_ac"], person["jira_ac"], person["slack_ac"]) for person in data])
    
#Commit changes and close connection
    conn.commit()
    conn.close()


def generate_and_create_db(db_name, records_generate=1000):
    data = generate_data(records_generate)
    create_sqlite_db(data, db_name)

print()

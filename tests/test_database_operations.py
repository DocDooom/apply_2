import sqlite3
from database_operations.database_operator import DatabaseOperator

def test_get_record():
    # Initialize a temporary in-memory database connection
    conn = sqlite3.connect(":memory:")
    db_operator = DatabaseOperator(":memory:")  # Pass ":memory:" as the database name
    
    # Create the employees table if it does not exist
    db_operator.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                                    id INTEGER PRIMARY KEY,
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
                                );''')
    
    # Add a record
    db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)
    
    # Get records
    records = db_operator.get_record()
    
    # Assert that at least one record is retrieved
    assert len(records) >= 1

    # Close the database connection
    db_operator.close_connection()
    

def test_add_record():
    # Initialize a temporary in-memory database connection
    conn = sqlite3.connect(":memory:")
    db_operator = DatabaseOperator(":memory:")
    
    # Create the necessary table
    db_operator.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY, 
                            first_name TEXT, 
                            last_name TEXT, 
                            email TEXT, 
                            role TEXT, 
                            department TEXT, 
                            hire_date TEXT, 
                            leave_date TEXT, 
                            monday_access INTEGER, 
                            jira_access INTEGER, 
                            slack_access INTEGER);''')
    
    # Add a record
    db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)
    
    # Get all records
    records = db_operator.get_record()
    
    # Assert that a record was added
    assert len(records) == 1
    
    # Close the database connection
    db_operator.close_connection()
    

def test_get_record_by_id():
    # Initialize a temporary in-memory database connection
    conn = sqlite3.connect(":memory:")
    db_operator = DatabaseOperator(":memory:")
    
    # Create the necessary table
    db_operator.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY, 
                            first_name TEXT, 
                            last_name TEXT, 
                            email TEXT, 
                            role TEXT, 
                            department TEXT, 
                            hire_date TEXT, 
                            leave_date TEXT, 
                            monday_access INTEGER, 
                            jira_access INTEGER, 
                            slack_access INTEGER);''')
    
    # Add a record
    db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)
    
    # Get the record by ID
    record = db_operator.get_record_by_id(1)
    
    # Assert that the record is not None
    assert record is not None
    
    # Close the database connection
    db_operator.close_connection()

def test_update_record():
    # Initialize a temporary in-memory database connection
    conn = sqlite3.connect(":memory:")
    db_operator = DatabaseOperator(":memory:")  # Pass ":memory:" as the database name
    
    # Create the employees table if it does not exist
    db_operator.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                                    id INTEGER PRIMARY KEY,
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
                                );''')
    
    # Add a record
    db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)
    
    # Update the record
    db_operator.update_record(1, "Jane", "Doe", "janedoe@example.com", "developer", "web", "1995-07-11", "Still working", 1, 1, 1)
    
    # Retrieve the updated record
    updated_record = db_operator.get_record_by_id(1)
    
    # Assert that the record was updated correctly
    assert updated_record[1] == "Jane"  # Assuming the first name was updated to "Jane"
    
    # Close the database connection
    db_operator.close_connection()

def test_delete_record():
    # Initialize a temporary in-memory database connection
    conn = sqlite3.connect(":memory:")
    db_operator = DatabaseOperator(":memory:")  # Pass ":memory:" as the database name
    
    # Create the employees table if it does not exist
    db_operator.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                                    id INTEGER PRIMARY KEY,
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
                                );''')
    
    # Add a record
    db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)
    
    # Delete the record
    db_operator.delete_record(1)
    
    # Retrieve the deleted record
    deleted_record = db_operator.get_record_by_id(1)
    
    # Assert that the record was deleted
    assert deleted_record is None
    
    # Close the database connection
    db_operator.close_connection()

# Run tests
test_get_record()
test_add_record()
test_get_record_by_id()
test_update_record()
test_delete_record()


# Import the DatabaseOperator class
from database_experiments import DatabaseOperator

# Create an instance of the DatabaseOperator class
db_operator = DatabaseOperator("test1.db")

# Add a record
db_operator.add_record("John", "Doe", 30, "Valencia")

# Update a record
db_operator.update_record(1000, "Jane", "Doe", 35, "Sydney")  # Assuming the record with ID 1 exists

# Delete a record
db_operator.delete_record(999) # Assuming the record with ID 999 exists

# Get all records
records = db_operator.get_record()
for record in records:
    print(record)

# Close the database connection
db_operator.close_connection()

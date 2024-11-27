# Import the DatabaseOperator class
from database_operator import DatabaseOperator

# Create an instance of the DatabaseOperator class
db_operator = DatabaseOperator("employees1.db")

# Add a record
db_operator.add_record("John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)

# Update a record
db_operator.update_record(50, "John", "Doe", "johndoe@example.com", "maintenance", "mobile", "1993-05-03", "Still working", 1, 0, 1)  # Assuming the record with ID 1000 exists

# Delete a record
db_operator.delete_record(52) # Assuming the record with ID 999 exists

# Get record by ID
record_id = 57  # Assuming the record ID you want to retrieve is 50
record = db_operator.get_record_by_id(record_id)
if record:
    print("Record found:")
    print(record)
else:
    print(f"No record found with ID {record_id}")


# Get all records
records = db_operator.get_record()
for record in records: 
    print(record)

# Close the database connection
db_operator.close_connection()

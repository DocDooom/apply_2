from db_worker import DBWorker

db_worker = DBWorker()  # Using the default path ../data/

db_worker.create_table()
db_worker.add_fake_employees(50)

employees = db_worker.get_employees()
for employee in employees:
    print(employee)

db_worker.close_connection()
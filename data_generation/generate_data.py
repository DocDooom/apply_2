# Here we are generating a CSV file for data persistence
# Currently (08/02/2024) we need to change the fields to match what IT employee data may look like
# at a company

from faker import Faker
from random import randrange

fake = Faker()


class People:
    def __init__(self, name, surname, age, city):
        self.name = name
        self.surname = surname
        self.age = age 
        self.city = city

    def csv_row(self):
        return f"{self.name},{self.surname},{self.age},{self.city}\r\n"


def generate_csv(output_filename, records_generate=1000):
    people_data = [{
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "age": randrange(18, 85),
        "city": fake.city()
    } for _ in range(records_generate)]

    people_objects = [People(i["name"], i["surname"], i["age"], i["city"]) for i in people_data]

    with open(output_filename, "w") as file:
        file.write("name,surname,age,city\r\n")
        for person in people_objects:
            file.write(person.csv_row())

    return people_objects

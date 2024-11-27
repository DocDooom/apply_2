# NOTE: In the initial commit this file was called main.py

import sys
from faker import Faker
from random import randrange
from peewee import *

from data_generation.legacy_code import config, chunking

# Verbose Debug mode data switch - will generate True or False
debug_mode = "-d" in sys.argv or "--debug" in sys.argv

fake = Faker()

people = [{"first_name": fake.first_name(),
           "last_name": fake.last_name(),
           "age": randrange(18, 85),
           "city": fake.city()}
          for _ in range(1000)]

if debug_mode:
    print(sys.getsizeof(people), "bytes")

# Please note to run this you'll need your own postgres database and input the credentials for those
db = PostgresqlDatabase("postgres", host="localhost", port=5432,
                        user="postgres", password=config.db_credentials["pass"])


class Person(Model):
    first_name = CharField()
    last_name = CharField()
    age = IntegerField()
    city = CharField()

    class Meta:
        database = db


db.connect()
if not db.is_closed():
    print("db is connected & open")

print(db.get_tables())
if "person" not in db.get_tables():
    db.create_tables([Person])

for chunk in chunking.chunk_iterator(people, chunk_size=50):  # insert 50 at a time
    if debug_mode:
        print(chunk)
        print(sys.getsizeof(chunk), "bytes")

    with db.atomic():
        Person.insert_many(chunk).execute()


db.close()
if db.is_closed():
    print("db is closed")


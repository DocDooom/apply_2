from dataclasses import dataclass


@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
    city: str

    def csv_info(self):
        return f"{self.first_name},{self.last_name},{self.age},{self.city}"

from typing import Union

from models.db_worker import DBWorker


THREE_YEARS_IN_DAYS = 1095


def check_number(string_input: str, check_type="int") -> Union[int, float, None]:
    try:
        match check_type:
            case "int":
                num = int(string_input)
                return num
            case "float":
                num = float(string_input)
                return num
    except ValueError:
        print("The input cannot be converted to a number!")
        return None


def check_if_string_is_bool(string_input: str) -> Union[bool, None]:
    match string_input.lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            print("The input is not a boolean!")
            return None


class Controller:
    def __init__(self, db_path="../data/employees.db"):
        self.db_worker = DBWorker(db_path)
        self.employee_objects = None

    def create_db_content(self):
        self.db_worker.create_table()
        self.db_worker.add_fake_employees(50)

        return True

    def retrieve_employees(self):
        if not self.db_worker.get_employees():
            self.create_db_content()

        return self.db_worker.get_employees()

    def get_employee_objects(self):
        employees_class = self.db_worker.create_class_from_table(self.db_worker.cursor, "employees")
        self.employee_objects = self.db_worker.fetch_objects(employees_class, "employees")
        return self.employee_objects

    # Over threshold employees - those that have left over 3 years ago
    def over_threshold_employees(self):
        overs = []
        for employee in self.get_employee_objects():
            if employee.days_since_leave >= THREE_YEARS_IN_DAYS:
                overs.append(employee)
        return overs

    # Leaver hits - those that have left
    def leaver_hits(self):
        leavers = []
        for employee in self.get_employee_objects():
            if not employee.leave_date == "Still Working":
                leavers.append(employee)
        return leavers

    def add_employee_to_db(self, employee):
        self.db_worker.add_single_employee(**employee)

    def regenerate_db(self):
        self.db_worker.delete_table()
        self.create_db_content()
        print("Database Regenerated")
        return True


if __name__ == "__main__":
    controller = Controller()

    print([i for i in controller.over_threshold_employees()])


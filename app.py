from flask import Flask, render_template, request, session, redirect, url_for
from controllers.controller import Controller, check_number, check_if_string_is_bool

app = Flask(__name__)
app.secret_key = "654321"
controller = Controller(db_path="./data/employees.db")


@app.route('/', methods=['GET', 'POST'])
def index():
    employees = controller.get_employee_objects()
    return render_template('index.html', employees=employees)


@app.route('/remove', methods=["GET", "POST"])
def remove():
    over_employees = controller.over_threshold_employees()

    if request.method == "POST":
        for i in over_employees:
            print("removing id: ", i.id)
            controller.db_worker.delete_employee(i.id)

        return redirect(url_for("remove_complete"))

    return render_template("remove.html", over_employees=over_employees)


@app.route('/remove_complete', methods=["GET"])
def remove_complete():
    return render_template("remove_complete.html")


@app.route('/new', methods=["GET", "POST"])
def new():
    # Handle the form submission
    if request.method == "POST":
        new_hire = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "role": request.form["role"],
            "department": request.form["department"],
            "hire_date": request.form["hire_date"],
            "leave_date": "Still Working",
            "monday_access": check_if_string_is_bool(request.form["monday_access"]),
            "jira_access": check_if_string_is_bool(request.form["jira_access"]),
            "slack_access": check_if_string_is_bool(request.form["slack_access"])
        }

        controller.add_employee_to_db(new_hire)

        # Getting back the newly created employee
        new_id = controller.db_worker.get_max_id()
        new_employee_class = controller.db_worker.create_class_from_table(controller.db_worker.cursor, "employees")
        added_employee_obj = controller.db_worker.fetch_an_employee_to_object(new_employee_class, new_id)
        print(type(added_employee_obj))

        return render_template("new_added.html", added_employee=added_employee_obj)

    return render_template("new.html")


@app.route('/update', methods=["GET", "POST"])
def update():
    message = ""

    if request.method == "POST":
        if check_number(request.form["get_employee"], check_type="int") is None:
            message = "The input is not an integer, Please try again!"
            return render_template("update.html", message=message)

        if not controller.db_worker.get_max_id() >= int(request.form["get_employee"]):
            message = f"The employee id {request.form['get_employee']} does not exist, Please try again!"
            return render_template("update.html", message=message)

        if int(request.form["get_employee"]) < 1:
            message = "The employee id cannot be less than 1, Please try again!"
            return render_template("update.html", message=message)

        employee_id = request.form["get_employee"]
        session["employee_id"] = employee_id
        employee = controller.db_worker.fetch_an_employee_to_object(controller.db_worker.create_class_from_table(
            controller.db_worker.cursor, "employees"), employee_id)

        # fetch employee data
        employee_record = controller.db_worker.fetch_an_employee_to_object(
            controller.db_worker.create_class_from_table(controller.db_worker.cursor, "employees"), employee_id)

        session["employee_record"] = vars(employee_record)

        return redirect(url_for("update_return"))

    return render_template("update.html", message=message)


@app.route('/update_return', methods=["GET", "POST"])
def update_return():
    # display employee data from id gotten with update
    employee_record = session["employee_record"]

    if request.method == "POST":
        action = request.form["action"]

        if action == "Edit":
            return redirect(url_for("update_form"))
        elif action == "Cancel":
            return redirect(url_for("update"))

    return render_template("update_return.html", employee_record=employee_record)


# Todo: We need to pre-populate the form with the employee data
@app.route('/update_form', methods=["GET", "POST"])
def update_form():
    # We'll use the employee record to fill out the form initially
    employee_record = session["employee_record"]
    employee_id = session["employee_id"]

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        role = request.form["role"]
        department = request.form["department"]
        hire_date = request.form["hire_date"]
        leave_date = request.form["leave_date"]
        monday_access = check_if_string_is_bool(request.form["monday_access"])
        slack_access = check_if_string_is_bool(request.form["slack_access"])
        jira_access = check_if_string_is_bool(request.form["jira_access"])

        update_success = controller.db_worker.update_employee(employee_id, first_name, last_name, email, role,
                                                              department,
                                                              hire_date, leave_date, monday_access, jira_access,
                                                              slack_access)

        if not update_success:
            return url_for("update", message="The update was not successful!")

        return redirect(url_for("update_complete"))

    return render_template("update_form.html", employee_record=employee_record,
                           employee_id=str(employee_id))


@app.route('/update_complete', methods=["GET", "POST"])
def update_complete():
    return render_template("update_complete.html")


@app.route('/leavers', methods=["GET", "POST"])
def leavers():
    leavers_hits = controller.leaver_hits()

    if request.method == "POST":
        for i in leavers_hits:
            print("restricting id: ", i.id)
            controller.db_worker.restrict_access(i.id, "monday_access")
            controller.db_worker.restrict_access(i.id, "jira_access")
            controller.db_worker.restrict_access(i.id, "slack_access")

        return redirect(url_for("leavers_updated"))

    return render_template("leavers.html", leaver_hits=leavers_hits)


@app.route('/leavers_updated', methods=["GET"])
def leavers_updated():
    return render_template("leavers_updated.html")


@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        controller.regenerate_db()

    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)

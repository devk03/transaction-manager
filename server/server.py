from flask import Flask, abort, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from utility.csv_parsing import parse_into_json
# import utility.sql_queries
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate
from models import Employee, transactions, db


### Create a Flask application
app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://[usename]:[password]@localhost:5432/[db_name]"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://devk:root@localhost:5432/ramp"
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

"""
Completed:

    - Setup PSQL Database (Transactions Table, Employees)
    - Setup Flask Backend
    - Employees
        Created post employees route
    - Query by 
        Employee
            By Name -> @app.route("/employee/<string:name>", methods=["GET"])

Todos before interview:
    - Post transactions
    - Query by 
        Transactions
            @app.route("/transaction/", methods=["GET"])
                -> Date
                -> Vendor
                -> Employee Name -> Id

    - Find Recurring Transactions

    - Card Balances Table?
        Ex. amex, mastercard, etc. all have balances
        Payment to pay balance

    - Find some string parsing problem
    - Review csv parsing

GOAL: WRITE CLEAN CODE!!!!!
"""

"""
DEFINING DB SCHEMA -> UPDATING PSQL DB
---------------------------------------
$ rm -r migrations/ -> deleting the migrations directory
$ flask db init -> creates migration repository.
$ flask db migrate -m "Initial migration" -> You can then generate an initial migration:
$ flask db upgrade -> applys the changes made
"""

"""
Recieving Flask Requests
------------------------
For URL query parameters, use request.args.
search = request.args.get("search")
page = request.args.get("page")
---
For posted form input, use request.form.
email = request.form.get('email')
password = request.form.get('password')
---
For JSON posted with content type application/json, use request.get_json().
data = request.get_json()
"""

"""
Different ways to pull request data
-----------------------------------
request.data -> raw data
request.headers.get('key') -> Get a header
request.get_json() -> Parse JSON data from request
request.form.get('key') -> From Form
request.args.get('query') -> Access single query parameter
------------------------------
@app.route('/user/<username>')
def show_user_profile(username):
    # The function parameter "username" captures the value from the URL
---------------------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']  # Access uploaded file
    # Process the file
"""


@app.route("/transaction/", methods=["POST", "GET"])
def transaction():
    request_type = request.method
    match request_type:
        case "POST":
            vendor = request.form.get("vendor")
            employee_first_name = request.form.get("first_name")
            employee_last_name = request.form.get("last_name")
            amount = request.form.get("amount")
            location = request.form.get("amount")
            card_type = request.form.get("card_type")
            transaction_type = request.form.get("transaction_type")
            # FINISH THIS
            return make_response(
                jsonify({"message": "Transaction Posted Successfully"}, 200)
            )
        case "GET":
            return make_response(
                jsonify({"message": "Transactions Queried Successfully"}, 200)
            )


@app.route("/employee/<string:name>", methods=["GET"])
def query_employee(name):
    """Query the database for a specific employee."""
    # Data Cleanup
    name = name.lower()
    first_name_results = Employee.query.filter_by(first_name=name).all()
    last_name_results = Employee.query.filter_by(last_name=name).all()

    total_results = set(first_name_results).union(set(last_name_results))
    employees_dict = dict()
    for employee in total_results:
        employee_id_str = str(employee.employee_id)
        employees_dict[employee_id_str] = {
            "First_Name": employee.first_name,
            "Last_Name": employee.last_name,
            "Email": employee.email,
            "Experience": employee.years_of_experience,
        }
    return make_response(employees_dict, 200)


@app.route("/employee/create/", methods=["POST"])
def create_employee():
    """Creating a unique employee and posting them to the database."""

    # HTTP Request Information Transfer
    email = request.headers.get("email")
    first_name = request.form.get("First Name")
    last_name = request.form.get("Last Name")
    years_of_exp = request.form.get("Years of Experience")

    # ERROR HANDLING -> Form + Header Data
    if not all([email, first_name, last_name, years_of_exp]):
        return make_response(jsonify({"error": "missing data"}), 400)
    try:  # Check years of experience
        years_of_exp = int(years_of_exp)
        if years_of_exp < 0:
            raise ValueError("Years of Experience must be above 0")
    except Exception as error:
        return make_response(jsonify({"error": error}), 400)

    # Data Clean Up
    first_name = first_name.lower()
    last_name = last_name.lower()
    email = email.lower()

    # DB-TRANSACTION -> Posting Employee to DB
    new_employee = Employee(
        first_name=first_name,
        last_name=last_name,
        years_of_experience=years_of_exp,
        email=email,
    )
    try:
        # making the db commit
        db.session.add(new_employee)
        db.session.commit()
    except Exception as error:
        db.session.rollback()  # Roll back in case the db-transaction fails
        return make_response(jsonify({"error": error}), 400)

    return make_response(jsonify({"message": "employee created succesfully"}), 201)


@app.route("/populate_data/", methods=["POST"])
def populate_data():
    """Parse the CSV data and populate the database with the data."""
    try:
        data = parse_into_json()
    except Exception as e:
        print(f"Error: {e}")
        return "Error"
    else:
        for key in data.keys():
            # Print statements for debugging
            # print(key)
            # print(data[key])

            # Create a transaction object
            one_transaction = transactions(
                transaction_id=key,
                transaction_date=data[key]["Date"],
                transaction_time=data[key]["Time"],
                vendor=data[key]["Vendor"],
                employee_name=data[key]["Employee"],
                amount=data[key]["Amount"],
                location=data[key]["Location"],
                card_type=data[key]["Card Type"],
                transaction_type=data[key]["Transaction Type"],
            )

            # Add the transaction (one specific table) to the database
            db.session.add(one_transaction)
            db.session.commit()

        return {"message": "Data populated"}


@app.cli.command("init-db")
def init_db_command():
    """Create the database tables. ONLY RAN ONCE. DO NOT RUN AGAIN"""
    # flask --app server init-db (to run this command)
    print("Creating the database tables...")
    db.create_all()
    print("Database tables created.")


if __name__ == "__main__":
    # Create the database tables if they don't exist
    with app.app_context():
        print("Creating the database tables...")
        db.create_all()
    app.run(debug=True)

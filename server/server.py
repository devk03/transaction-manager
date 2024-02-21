from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from utility.csv_parsing import parse_into_json
from sqlalchemy.dialects.postgresql import UUID
from flask_migrate import Migrate
import uuid

### Create a Flask application
app = Flask(__name__)

### Database Configuration

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://[usename]:[password]@localhost:5432/[db_name]"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://devk:root@localhost:5432/ramp"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""
Completed:

    - Setup PSQL Database (Transactions Table, Employees)
    - Setup Flask Backend
    - Employees
        Created post employees route

Todos before interview:

    - Query by 
        Employee
            By Name
        Transactions
            By Data
            By Card
            By Amount

    - Find Recurring Transactions

    - Card Balances Table?
        Ex. amex, mastercard, etc. all have balances
        Make payments feature
        Payments table
            Query Payments by data

    - Post transactions

GOAL: WRITE CLEAN CODE!!!!!
"""

"""
DEFINING DB SCHEMA -> UPDATING PSQL DB
---------------------------------------
$ flask db init -> creates migration repository.
$ rm -r migrations/ -> deleting the migrations directory
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


class transactions(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    transaction_date = db.Column(db.Date, nullable=False)
    transaction_time = db.Column(db.Time, nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    employee_name = db.Column(
        db.String(255), db.ForeignKey("employee.employee_name"), nullable=False
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.Text, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)


class Employee(db.Model):
    __tablename__ = "employee"
    employee_name = db.Column(db.String(255), primary_key=True, unique=True)
    years_of_experience = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)


# @app.route("/", methods=["GET"])
# def hello_world():
#     return {"message": "Hello World"}


@app.route("/query_employee/<string:name>", methods=["GET"])
def query_employee(name):
    """Query the database for a specific employee."""
    query_results = transactions.query.filter_by(employee_name=name).all()
    print(query_results)
    return "transactions"


@app.route("/employee/create", methods=["POST"])
def create_employee():
    """Creating a unique employee and posting them to the database."""

    # HTTP Request Information Transfer
    email = request.headers.get("email")
    first_name = request.form.get("First Name")
    last_name = request.form.get("Last Name")
    years_of_exp = request.form.get("Years of Experience")

    # ERROR HANDLING -> Form + Header Data
    if not all([email, first_name, last_name, years_of_exp]):
        return make_response(jsonify({"error", "missing data"}), 400)
    try:
        years_of_exp = int(years_of_exp)
        if years_of_exp < 0:
            raise ValueError("Years of Experience must be above 0")
    except Exception as error:
        return make_response(jsonify({"error", error}), 400)

    # DB-TRANSACTION -> Posting Employee to DB
    new_employee = Employee(
        employee_name=f"{first_name} {last_name}",
        years_of_experience=years_of_exp,
        email=email,
    )
    try:
        # making the db commit
        db.session.add(new_employee)
        db.session.commit()
    except Exception as error:
        db.session.rollback()  # Roll back in case the db-transaction fails
        return make_response(jsonify({"error", error}), 400)

    return make_response(jsonify({"message", "employee created succesfully"}), 201)


# @app.route("/query_transactions/", methods=["GET"])
# def query():
#     query_results = transactions.query.all()
#     print(query_results)
#     return "transactions"


# @app.route("/make_payment/", methods=["GET"])
# def make_payment():
#     return {"message": "Make a payment."}


# @app.route("/check_balance/", methods=["GET"])
# def check_balance():
#     return {"message": "Check the Balance."}


# @app.route("/metrics/vendor/", methods=["Get"])
# def vendor_metrics():
#     return {"message", "apply csv data"}


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

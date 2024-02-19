from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from utility.csv_parsing import parse_into_json
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Create a Flask application
app = Flask(__name__)

# Database Configuration

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://[usename]:[password]@localhost:5432/[db_name]"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://devk:root@localhost:5432/ramp"

db = SQLAlchemy(app)


class transactions(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    transaction_date = db.Column(db.Date, nullable=False)
    transaction_time = db.Column(db.Time, nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    employee_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.Text, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)


@app.route("/", methods=["GET"])
def hello_world():
    return {"message": "Hello World"}


@app.route("/query_transactions/", methods=["GET"])
def query():
    query_results = transactions.query.all()
    print(query_results)
    return "transactions"


@app.route("/make_payment/", methods=["GET"])
def make_payment():
    return {"message": "Make a payment."}


@app.route("/check_balance/", methods=["GET"])
def check_balance():
    return {"message": "Check the Balance."}


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


@app.route("/metrics/vendor/", methods=["Get"])
def vendor_metrics():
    return {"message", "apply csv data"}


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

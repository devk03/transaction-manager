import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


# Initialize the database
db = SQLAlchemy()


# Define the models
class transactions(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    transaction_date = db.Column(db.Date, nullable=False)
    transaction_time = db.Column(db.Time, nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    employee_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("employee.employee_id"),
        default=uuid.uuid4,
        nullable=False,
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.Text, nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)


class Employee(db.Model):
    __tablename__ = "employee"
    employee_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)


class Card(db.Model):
    __tablename__ = "card"
    card_name = db.Column(db.String(255), primary_key=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(10, 2), nullable=False)

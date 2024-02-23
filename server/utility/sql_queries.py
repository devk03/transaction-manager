from models import Employee, transactions, Card, db  # i messed up the casing
from datetime import datetime
from flask import abort
from sqlalchemy import select, and_


def post_transaction(information: dict):
    """Post a transaction to the database"""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    # New way to query -> statement + execute
    employee_id_stmt = select(Employee).where(
        and_(
            Employee.first_name == information["first_name"],
            Employee.last_name == information["last_name"],
        )
    )
    employee_query_result = db.session.execute(employee_id_stmt)

    """
    >>> How to iterate through the results
    for object in employee_query_result.scalars():
        print(f"{object.employee_id}")
    """

    # Pulls the first employee that comes up
    employee_id_for_transaction = employee_query_result.scalars().first().employee_id

    # define the transaction object
    new_transaction = transactions(
        transaction_date=current_date,
        transaction_time=current_time,
        vendor=information["vendor"],
        employee_id=employee_id_for_transaction,
        amount=information["amount"],
        location=information["location"],
        card_type=information["card_type"],
        transaction_type=information["transaction_type"],
    )
    try:
        # making the db commit
        db.session.add(new_transaction)
        db.session.commit()
    except Exception as error:
        db.session.rollback()  # Roll back in case the db-transaction fails
        raise Exception("The database commit could not go through.")

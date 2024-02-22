from models import Employee, Transactions, Cards
from datetime import datetime


def post_transaction(information: dict):
    """Post a transaction to the database"""
    
    # Finding the current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

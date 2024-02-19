import csv
import uuid


def parse_into_json():
    """Parses the CSV into a JSON document"""
    # Open the file and open a dictionary reader
    try:
        with open("./transaction_data.csv") as file:
            csvreader = csv.DictReader(file)

            # Create a dictionary and read the data in
            transaction_dict = dict()

            for line in csvreader:
                random_id = str(uuid.uuid1())
                transaction_dict[random_id] = dict()
                for key in line.keys():
                    transaction_dict[random_id][key] = line[key]

            return transaction_dict

    # Handle the exception here
    except Exception as e:
        print(f"Error: {e}")
"""
Testing Locally Instructions
----------------------------
1. Change ""./transaction_data.csv" to "server/transaction_data.csv"

"""

"""
Data Format in JSON
{
  "67042a6e-cece-11ee-a9e7-4eea7e608d3a": {
    "Date": "1/21/24",
    "Time": "4:38:08",
    "Vendor": "Acevedo-Marks",
    "Employee": "Carly Russell",
    "Amount": "436.58",
    "Location": "Port Jordan, Oklahoma, United States Minor Outlying Islands",
    "Card Type": "AmEx",
    "Transaction Type": "Purchase"
  },
  ...
}
"""

from flask import Flask, jsonify
from utility.csv_parsing import parse_into_json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return {"message": "Hello World"}


@app.route("/make_payment/", methods=["GET"])
def make_payment():
    return {"message": "Make a payment."}


@app.route("/check_balance/", methods=["GET"])
def check_balance():
    return {"message": "Check the Balance."}


@app.route("/parse_data", methods=["GET"])
def parse_data():
    return jsonify(parse_into_json())


@app.route("/metrics/vendor", methods=["Get"])
def vendor_metrics():
    return {"message", "apply csv data"}


if __name__ == "__main__":
    app.run(debug=True)

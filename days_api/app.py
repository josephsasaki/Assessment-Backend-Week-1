"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome message."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def between():
    """Returns the number of days between two dates"""
    # Check the request parameters are valid
    request_data = request.get_json()
    first = request_data.get("first")
    last = request_data.get("last")
    if first is None or last is None:
        return {"error": "Missing required data."}, 400
    # Convert strings to datetime
    try:
        first_date = convert_to_datetime(first)
        last_date = convert_to_datetime(last)
    except (ValueError, TypeError):
        return {"error": "Unable to convert value to datetime."}, 400
    # Calculate days difference
    days_between = get_days_between(first_date, last_date)
    add_to_history(request)
    return {"days": days_between}, 200


@app.route("/weekday", methods=["POST"])
def weekday():
    """Returns the day of the week a specific date is"""
    # Check the request parameters are valid
    request_data = request.get_json()
    date_str = request_data.get("date")
    if date_str is None:
        return {"error": "Missing required data."}, 400
    # Convert to datetime object
    try:
        passed_date = convert_to_datetime(date_str)
    except (ValueError, TypeError):
        return {"error": "Unable to convert value to datetime."}, 400
    day_of_week = get_day_of_week_on(passed_date)
    add_to_history(request)
    return {"weekday": day_of_week}, 200


@app.route("/history", methods=["GET", "DELETE"])
def history():
    """GET: Returns details on the last number of requests to the API.
    DELETE: Deletes details of all previous requests to the API"""
    if request.method == "GET":
        args = request.args.to_dict()
        number = args.get("number")
        if number is None:
            number = 5
        elif not number.isnumeric():
            return {"error": "Number must be an integer between 1 and 20."}, 400
        elif int(number) not in range(1, 21):
            return {"error": "Number must be an integer between 1 and 20."}, 400
        number = int(number)
        add_to_history(request)
        return app_history[-number:][::-1], 200
    if request.method == "DELETE":
        app_history.clear()
        return {"status": "History cleared"}, 200
    return {"error": "Unable to convert value to datetime."}, 405


@app.route("/current_age", methods=["GET"])
def current_age():
    """Returns a current age in years based on a given birthdate."""
    # Check the request parameters are valid
    args = request.args.to_dict()
    date_str = args.get("date")
    if date_str is None:
        return {"error": "Date parameter is required."}, 400
    try:
        passed_date = convert_to_datetime(date_str)
    except (ValueError, TypeError):
        return {"error": "Value for data parameter is invalid."}, 400
    age = get_current_age(passed_date)
    add_to_history(request)
    return {"current_age": age}, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)

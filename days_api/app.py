"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

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
    request_data = request.get_json()
    first_date = convert_to_datetime(request_data.get("first"))
    last_date = convert_to_datetime(request.get("last"))
    days_between = get_days_between(first_date, last_date)
    add_to_history(request)
    return {"days": days_between}, 200


@app.route("/weekday", methods=["POST"])
def weekday():
    """Returns the day of the week a specific date is"""
    request_data = request.get_json()
    passed_date = convert_to_datetime(request_data.get("date"))
    weekday = get_day_of_week_on(passed_date)
    add_to_history(request)
    return {"weekday": weekday}, 200


@app.route("/history/", methods=["GET", "DELETE"])
def history():
    """GET: Returns details on the last number of requests to the API.
    DELETE: Deletes details of all previous requests to the API"""
    if request.method == "GET":
        args = request.args.to_dict()
        number = args.get("number")
        if number not in range(1, 21):
            return {"error": True, "message": "Number query parameter must be between 1 and 20 (inclusive)."}, 400
        elif number is None:
            number = 5
        return app_history[5:], 200
    else:
        app_history = []
        return {"status": "History cleared"}, 200


@app.route("/current_age", methods=["GET"])
def current_age():
    """Returns a current age in years based on a given birthdate."""
    return


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)

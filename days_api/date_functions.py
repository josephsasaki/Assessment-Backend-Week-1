"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Converts a string formatted as DD.MM.YYYY to a datetime object."""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        pass
    try:
        return datetime.strptime(date_val, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Unable to convert value to datetime.") from exc


def get_days_between(first: datetime, last: datetime) -> int:
    """Get the number of days between two dates."""
    if not (isinstance(first, datetime) and isinstance(last, datetime)):
        raise TypeError("Datetimes required.")
    return (last - first).days


def get_day_of_week_on(date_val: datetime) -> str:
    """Get the day of the week of a datetime object."""
    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")
    return date_val.strftime("%A")


def get_current_age(birthdate: date) -> int:
    """Gets the current age of someone from their birthday."""
    if not isinstance(birthdate, date):
        raise TypeError("Date required.")
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

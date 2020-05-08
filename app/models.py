import json
from . import db


def empty_json():
    """
    Lazy default for the users column.
    """
    return json.dumps([])


class Channel(db.Model):
    channel = db.Column(db.String, primary_key="True")
    users = db.Column(db.JSON, default=empty_json())

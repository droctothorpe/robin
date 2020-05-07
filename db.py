import json
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "data.sqlite"
# )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Channel=Channel)


def empty_json():
    """
    Lazy default for the users column.
    """
    return json.dumps([])


class Channel(db.Model):
    channel = db.Column(db.String, primary_key="True")
    users = db.Column(db.JSON, default=empty_json())


no_channel = """\
This channel has not been initialized yet.
Run `/robin init` to initialize.
"""


def init(channel: str) -> str:
    """
    Initialize a row for the specified channel in the database.
    """
    c = Channel.query.get(channel)
    if c:
        return "This channel has already been initialized."
    c = Channel(channel=channel)
    db.session.add(c)
    db.session.commit()
    return "Channel successfully initialized."


def list_users(channel: str) -> list:
    """
    Return user list for channel.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    return users


def append_users(channel: str, *users_to_add: str):
    """
    Appends users to the specified channel's user list.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    for user in users_to_add:
        if user not in users:
            users.append(user)
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()


def insert_user(channel, user, index=0):
    """
    Insert user at specified index. Defaults to zero.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    users.insert(index, user)
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()


def delete(channel: str, *users_to_delete: str) -> str:
    """
    Removes users from the specified channe's user list.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    for user in users_to_delete:
        users.remove(user)
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()
    return "User(s) deleted."


def next_user(channel: str) -> str:
    """
    Selects the next user in the specified channel's user list.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    user = users.pop(0)
    users.append(user)
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()
    return user


def bump(channel: str) -> str:
    """
    Bumps the previously selected user to second position.
    """
    c = Channel.query.get(channel)
    users = json.loads(c.users)
    user = users.pop()
    users.insert(1, user)
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()
    return f"Moved {user} to second position."


def edit(channel: str, users: list) -> str:
    """
    Replace the user list for the specified channel with the provided list.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()
    return "User list updated."


if __name__ == "__main__":
    breakpoint()

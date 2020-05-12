import json
from random import choice
from .. import db
from ..models import Channel

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
    return "User(s) added."


def insert_user(channel, user, index=0):
    """
    Insert user at specified index. Defaults to zero.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    print(f"users before insertion: {users}")
    users.insert(index, user)
    print(f"users after insertion: {users}")
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()


def delete(channel: str, *users_to_delete: list) -> str:
    """
    Removes users from the specified channe's user list.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)

    if users_to_delete[0] == "all":
        c.users = json.dumps([])
    else:
        for user in users_to_delete:
            try:
                users.remove(user)
            except ValueError:
                continue
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


def random_user(channel: str) -> str:
    """
    Select a random user from the specified channel's user list.
    Does not modify order.
    """
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    users = json.loads(c.users)
    if len(users) == 0:
        return "No users to randomly select from."
    return f"Selecting a random user:\n{choice(users)}"


def edit(channel: str, *users: list) -> str:
    """
    Replace the user list for the specified channel with the provided list.
    """
    if len(users) == 0:
        return "No new user list provided."
    c = Channel.query.get(channel)
    if not c:
        return no_channel
    c.users = json.dumps(users)
    db.session.add(c)
    db.session.commit()
    return "User list updated."


def temp(*users: list) -> str:
    """
    Select a random user from a temporary, user-provided list.
    """
    if len(users) == 0:
        return "No users to randomly select from."
    return f"Selecting a random user from the provided list:\n{choice(users)}"


if __name__ == "__main__":
    breakpoint()

from . import main
from . import db
from flask import request, jsonify, abort

usage = """\
<http://www.linktorobin.com|*Robin*> is a slackbot for equitably distributing work within teams.

*Usage*:
- */robin init* -- Initialize the channel.
- */robin next* -- Select the next user from the list and rotate.
- */robin random* -- Select a random user from the list. Does not rotate. 
- */robin bump* -- Relocate the previously selected user to the second spot on the list in the event that they're unavailable.
- */robin add <user1> <user2>* -- Add users to the list.
- */robin insert <user> <index>* -- Inserts user at specified index (starts from 1, not 0).
- */robin delete <user1> <user2>* -- Delete users from the list.
- */robin delete all* -- Delete all users from the list.
- */robin edit* -- Pass in a list of users that are comma, space, or line break delimited and it will replace the existing list. Provides more granular control.
"""


@main.route("/", methods=["POST"])
def receiver():
    """
    Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """

    token = request.form.get("token", None)
    if not token:
        abort(400)

    channel = request.form.get("channel_name", None)
    text = request.form.get("text", None)

    text = sanitize_text(text)

    args = text.split()

    if len(args) == 0:
        return render_response(usage)

    subcommand = args[0]

    if subcommand == "help":
        return render_response(usage, "ephemeral")

    switcher = {
        "init": lambda: db.init(channel),
        "list": lambda: list_handler(channel),
        "add": lambda: db.append_users(channel, *args[1:]),
        "insert": lambda: db.insert_user(channel, args[1], int(args[2]) - 1),
        "delete": lambda: db.delete(channel, *args[1:]),
        "next": lambda: db.next_user(channel),
        "bump": lambda: db.bump(channel),
        "random": lambda: db.random_user(channel),
        "edit": lambda: db.edit(channel, *args[1:]),
    }

    func = switcher.get(subcommand)

    if not func:
        return render_response(usage, "ephemeral")

    msg = func()

    return render_response(msg)


# Helper functions


def render_response(msg: str, type="in_channel"):
    """
    Renders formatted response for Slack.
    """
    return jsonify(
        {
            "response_type": type,
            "attachments": [{"color": "#6CA6B7", "text": msg}],
        }
    )


def list_handler(channel: str) -> str:
    users = db.list_users(channel)
    if users == db.no_channel:
        return db.no_channel
    elif len(users) == 0:
        return "The user list for this channel is empty."
    else:
        return "\n".join(users)


def sanitize_text(text):
    """
    Replace commas with spaces in input.
    """
    text = text.replace(",", " ")
    return text


# @main.route("/pdb")
# def pdb():
#     breakpoint()

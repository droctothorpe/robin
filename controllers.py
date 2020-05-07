import db
from flask import Flask

app = Flask(__name__)

# The parameters included in a slash command request (with example values):
#   token=gIkuvaNzQIHg97ATvDxqgjtO
#   team_id=T0001
#   team_domain=example
#   channel_id=C2147483705
#   channel_name=test
#   user_id=U2147483697
#   user_name=Steve
#   command=/weather
#   text=94070
#   response_url=https://hooks.slack.com/commands/1234/5678

# Simplified test
# print(db.list_users("t"))


@app.route("/")
def test():
    # return "test"
    t = db.list_users("t")
    string = ", ".join(t)
    return string


"""
@app.route("/", methods=["POST"])
def receiver():
    Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    

    token = request.form.get("token", None)
    if not token:
        abort(400)

    channel = request.form.get("channel", None)
    text = request.form.get(text)
    args = text.split()
    
    subcommand = args[0]
    
    if subcommand = "next":
        message = 
    
    
    if not User.query.get(channel):
        users = User(channel=channel, users=users_json)
        db.session.add(users)
        db.session.commit()

    # users = request.form.get

    # exists = User.query.get(channel).scalar() is not None

    # print(exists)
    # return exists

    # command = request.form.get("command", None)
    # text = request.form.get("text", None)
    # Validate the request parameters

    # Use one of the following return statements
    # 1. Return plain text
    # return "Simple plain response to the slash command received"
    # return request.form.get("text")
    return request.form.get("team_domain")
    # 2. Return a JSON payload
    # See https://api.slack.com/docs/formatting and
    # https://api.slack.com/docs/attachments to send richly formatted messages
    return jsonify(
        {
            # Uncomment the line below for the response to be visible to everyone
            "response_type": "in_channel",
            "text": "More fleshed out response to the slash command",
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f",
                    "pretext": "Optional text above the attachment block",
                    "author_name": "Bobby Tables",
                    "author_link": "http://flickr.com/bobby/",
                    "author_icon": "http://flickr.com/icons/bobby.jpg",
                    "title": "Slack API Documentation",
                    "title_link": "https://api.slack.com/",
                    "text": "Optional text that appears within the attachment",
                    "fields": [
                        {"title": "Priority", "value": "High", "short": False}
                    ],
                    "image_url": "http://my-website.com/path/to/image.jpg",
                    "thumb_url": "http://example.com/path/to/thumb.png",
                }
            ],
        }
    )
    # 3. Send up to 5 responses within 30 minutes to the response_url
    # Implement your custom logic here
"""

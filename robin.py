import os
from app import create_app, db
from app.models import Channel
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Channel=Channel)


#
@app.cli.command()
def deploy():
    upgrade()

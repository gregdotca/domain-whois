from flask.cli import FlaskGroup

from project import app

cli = FlaskGroup(create_app=lambda: app)

if __name__ == "__main__":
    cli()

from flask.cli import FlaskGroup
from smart_notebook import db, app

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    return


if __name__ == "__main__":
    cli()

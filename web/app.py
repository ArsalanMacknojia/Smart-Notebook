from flask.cli import FlaskGroup
from smart_notebook import db, app
from smart_notebook.models import User, Note

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(id=0, username="NULL", first_name="NULL", last_name="NULL", email="NULL", phone_number="NULL", postal_code="NULL", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y", user_image="default.jpg"))
    db.session.add(User(username="ArsalanMacknojia", first_name="Arsalan", last_name="Macknojia", email="arsalan@gmail.com", phone_number="7781111111", postal_code="V3E3B5", password="$2b$12$ppAg.mOnlIo15d0m7gPYr.1LZaUvuO29JVVBkv6bkQzQz6zK.f66y", user_image="default.jpg"))
    db.session.commit()

    db.session.add(Note(title="Team Meeting Minutes", content="No more tickets lefts. Time to catch up on sleep.", user_id=1))
    db.session.add(Note(title="To-Do list", content="Get Fresh groceries. Meeting with Bill Gates on August 32th 2020. Don't forget to appreciate Professors and TAs for conducting online classes brilliantly. :)", user_id=1))
    db.session.add(Note(title="Book flight for Toronto", content="Check online travel websites!", user_id=1))
    db.session.commit()


if __name__ == "__main__":
    cli()

from flask.cli import FlaskGroup

from app import app, db
from app import models

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    u1=models.TelegramUser(first_name="Ivan", last_name="Ivanov", username="@ivan", phone="55555555")
    u2=models.TelegramUser(first_name="Ivan", last_name="Padalka", username="@kek", phone="80012111")
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    db.session.add(models.Defect(created_by_user=u1, title="lampa ne garit", description="nu ne garit", room=505, work_by_user=u2))
    db.session.commit()

if __name__ == "__main__":
    cli()

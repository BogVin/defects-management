from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
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
    u1 = models.TelegramUser(telegram_id="4234123987", first_name="Ivan", last_name="Ivanov", username="@ivan")
    u2 = models.TelegramUser(telegram_id="9999999999", first_name="Ivan", last_name="Padalka", username="@kek")
    db.session.add(u1)
    db.session.add(u2)
    d1 = models.Defect(title="lampa ne garit", description="nu ne garit", room=505)
    db.session.add(d1)
    db.session.add(models.DefectInfo(created_by_user=u1, defect=d1))
    db.session.commit()


@cli.command("create_admin")
def create_admin():
    password = generate_password_hash("password")
    adm = models.Admin(email="email@gmail.com", password_hash=password)
    db.session.add(adm)
    db.session.commit()


if __name__ == "__main__":
    cli()

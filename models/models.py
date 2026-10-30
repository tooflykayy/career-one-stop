from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), nullable=False, default="Other")
    proficiency = db.Column(db.String(30), nullable=False, default="Beginner")

    def __repr__(self):
        return f"<Skill {self.name}>"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_url = db.Column(db.String(1000), nullable=True)
    date_applied = db.Column(
        db.Date, nullable=True
    )
    status = db.Column(
        db.String(30), nullable=False, default="Saved"
    )
    follow_up_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.Date, nullable=False, default=date.today
    )

    def __repr__(self):
        return f"<Application {self.company}: {self.job_title}>"
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), nullable=False, default="Other")
    proficiency = db.Column(db.String(30), nullable=False, default="Beginner")

    def __repr__(self):
        return f"<Skill {self.name}>"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )
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


class LearningActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )
    career_id = db.Column(db.String(100), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    resource_title = db.Column(db.String(200), nullable=False)
    resource_url = db.Column(db.String(1000), nullable=False)
    status = db.Column(
        db.String(30), nullable=False, default="Planned"
    )
    created_at = db.Column(
        db.Date, nullable=False, default=date.today
    )

    def __repr__(self):
        return f"<LearningActivity {self.skill_name}: {self.status}>"
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), nullable=False, default="Other")
    proficiency = db.Column(db.String(30), nullable=False, default="Beginner")

    def __repr__(self):
        return f"<Skill {self.name}>"

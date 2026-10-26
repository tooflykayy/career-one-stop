import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models.models import db, Skill

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "local-development-key-change-before-deployment"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///career_one_stop.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def dashboard():
    skills = Skill.query.order_by(Skill.name.asc()).all()
    return render_template("dashboard.html", skills=skills)


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Other").strip()
        proficiency = request.form.get("proficiency", "Beginner")

        allowed_levels = {"Beginner", "Intermediate", "Advanced"}

        if not name:
            flash("Please enter a skill name.", "error")
        elif proficiency not in allowed_levels:
            flash("Please choose a valid proficiency level.", "error")
        elif len(name) > 100:
            flash("Skill names must be 100 characters or fewer.", "error")
        else:
            skill = Skill(
                name=name,
                category=category[:80] or "Other",
                proficiency=proficiency,
            )
            db.session.add(skill)
            db.session.commit()
            flash(f"{name} was added to your skills!", "success")
            return redirect(url_for("skills"))

    all_skills = Skill.query.order_by(Skill.name.asc()).all()
    return render_template("skills.html", skills=all_skills)


@app.route("/skills/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    skill = db.get_or_404(Skill, skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash(f"{skill.name} was removed.", "success")
    return redirect(url_for("skills"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(debug=True)

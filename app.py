
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from models.models import db, Skill

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "local-development-key-change-before-deployment"
)

database_url = os.environ.get(
    "DATABASE_URL", "sqlite:///career_one_stop.db"
)

# Render PostgreSQL URLs may use postgres://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


ALLOWED_LEVELS = {"Beginner", "Intermediate", "Advanced"}


@app.route("/")
def dashboard():
    skills = Skill.query.order_by(Skill.name.asc()).all()

    total_skills = len(skills)
    beginner_count = sum(s.proficiency == "Beginner" for s in skills)
    intermediate_count = sum(s.proficiency == "Intermediate" for s in skills)
    advanced_count = sum(s.proficiency == "Advanced" for s in skills)

    return render_template(
        "dashboard.html",
        skills=skills,
        total_skills=total_skills,
        beginner_count=beginner_count,
        intermediate_count=intermediate_count,
        advanced_count=advanced_count
    )


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Other").strip()
        proficiency = request.form.get("proficiency", "Beginner")

        if not name:
            flash("Please enter a skill name.", "error")
        elif len(name) > 100:
            flash("Skill names must be 100 characters or fewer.", "error")
        elif len(category) > 80:
            flash("Categories must be 80 characters or fewer.", "error")
        elif proficiency not in ALLOWED_LEVELS:
            flash("Please choose a valid proficiency level.", "error")
        else:
            skill = Skill(
                name=name,
                category=category or "Other",
                proficiency=proficiency
            )

            db.session.add(skill)
            db.session.commit()

            flash(f"{name} was added to your skills!", "success")
            return redirect(url_for("skills"))

    search = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()
    proficiency_filter = request.args.get("proficiency", "").strip()

    query = Skill.query

    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))

    if category_filter:
        query = query.filter(Skill.category == category_filter)

    if proficiency_filter in ALLOWED_LEVELS:
        query = query.filter(Skill.proficiency == proficiency_filter)

    all_skills = query.order_by(Skill.name.asc()).all()

    categories = [
        category[0]
        for category in db.session.query(Skill.category)
        .distinct()
        .order_by(Skill.category.asc())
        .all()
    ]

    return render_template(
        "skills.html",
        skills=all_skills,
        categories=categories,
        search=search,
        category_filter=category_filter,
        proficiency_filter=proficiency_filter
    )


@app.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
def edit_skill(skill_id):
    skill = db.get_or_404(Skill, skill_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Other").strip()
        proficiency = request.form.get("proficiency", "Beginner")

        if not name:
            flash("Please enter a skill name.", "error")
        elif len(name) > 100:
            flash("Skill names must be 100 characters or fewer.", "error")
        elif len(category) > 80:
            flash("Categories must be 80 characters or fewer.", "error")
        elif proficiency not in ALLOWED_LEVELS:
            flash("Please choose a valid proficiency level.", "error")
        else:
            skill.name = name
            skill.category = category or "Other"
            skill.proficiency = proficiency

            db.session.commit()

            flash(f"{name} was updated successfully!", "success")
            return redirect(url_for("skills"))

    return render_template("edit_skill.html", skill=skill)


@app.route("/skills/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    skill = db.get_or_404(Skill, skill_id)

    name = skill.name

    db.session.delete(skill)
    db.session.commit()

    flash(f"{name} was removed.", "success")
    return redirect(url_for("skills"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")


import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from urllib.parse import urlparse
from models.models import db, Skill, Application
from career_matching import match_careers

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

APPLICATION_STATUSES = (
    "Saved",
    "Applied",
    "Interviewing",
    "Offer",
    "Rejected",
)


@app.route("/applications", methods=["GET", "POST"])
def applications():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        job_url = request.form.get("job_url", "").strip()
        status = request.form.get("status", "Saved").strip()
        notes = request.form.get("notes", "").strip()

        date_applied_text = request.form.get(
            "date_applied", ""
        ).strip()
        follow_up_text = request.form.get(
            "follow_up_date", ""
        ).strip()

        errors = []

        if not company or not job_title:
            errors.append("Company and job title are required.")

        if len(company) > 150 or len(job_title) > 150:
            errors.append(
                "Company and job title must be 150 characters or fewer."
            )

        if status not in APPLICATION_STATUSES:
            errors.append("Please select a valid status.")

        if job_url:
            parsed_url = urlparse(job_url)
            if (
                len(job_url) > 1000
                or parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
            ):
                errors.append("Enter a valid http or https job URL.")

        date_applied = None
        follow_up_date = None

        try:
            if date_applied_text:
                date_applied = date.fromisoformat(date_applied_text)
            if follow_up_text:
                follow_up_date = date.fromisoformat(follow_up_text)
        except ValueError:
            errors.append("Please enter valid dates.")

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            application = Application(
                company=company,
                job_title=job_title,
                job_url=job_url or None,
                date_applied=date_applied,
                status=status,
                follow_up_date=follow_up_date,
                notes=notes,
            )

            db.session.add(application)
            db.session.commit()

            flash("Application saved successfully!", "success")
            return redirect(url_for("applications"))

    saved_applications = Application.query.order_by(
        Application.id.desc()
    ).all()

    return render_template(
        "applications.html",
        applications=saved_applications,
        statuses=APPLICATION_STATUSES,
    )
@app.route(
    "/applications/<int:application_id>/status",
    methods=["POST"],
)
def update_application_status(application_id):
    application = db.get_or_404(Application, application_id)
    new_status = request.form.get("status", "").strip()

    if new_status not in APPLICATION_STATUSES:
        flash("Please select a valid status.", "error")
    else:
        application.status = new_status
        db.session.commit()
        flash("Application status updated!", "success")

    return redirect(url_for("applications"))


@app.route(
    "/applications/<int:application_id>/delete",
    methods=["POST"],
)
def delete_application(application_id):
    application = db.get_or_404(Application, application_id)
    db.session.delete(application)
    db.session.commit()

    flash("Application deleted.", "success")
    return redirect(url_for("applications"))
@app.route(
    "/applications/<int:application_id>/edit",
    methods=["GET", "POST"],
)
def edit_application(application_id):
    application = db.get_or_404(Application, application_id)

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        job_url = request.form.get("job_url", "").strip()
        status = request.form.get("status", "").strip()
        notes = request.form.get("notes", "").strip()

        errors = []

        if not company or not job_title:
            errors.append("Company and job title are required.")

        if len(company) > 150 or len(job_title) > 150:
            errors.append(
                "Company and job title must be 150 characters or fewer."
            )

        if status not in APPLICATION_STATUSES:
            errors.append("Please select a valid status.")

        if job_url:
            parsed_url = urlparse(job_url)
            if (
                len(job_url) > 1000
                or parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
            ):
                errors.append("Enter a valid http or https job URL.")

        date_applied = None
        follow_up_date = None

        try:
            applied_text = request.form.get("date_applied", "").strip()
            follow_up_text = request.form.get(
                "follow_up_date", ""
            ).strip()

            if applied_text:
                date_applied = date.fromisoformat(applied_text)

            if follow_up_text:
                follow_up_date = date.fromisoformat(follow_up_text)
        except ValueError:
            errors.append("Please enter valid dates.")

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            application.company = company
            application.job_title = job_title
            application.job_url = job_url or None
            application.status = status
            application.date_applied = date_applied
            application.follow_up_date = follow_up_date
            application.notes = notes

            db.session.commit()
            flash("Application updated successfully!", "success")
            return redirect(url_for("applications"))

    return render_template(
        "edit_application.html",
        application=application,
        statuses=APPLICATION_STATUSES,
    )
@app.route("/career-match")
def career_match():
    saved_skills = Skill.query.order_by(Skill.name.asc()).all()
    careers = match_careers(saved_skills)

    return render_template(
        "career_match.html",
        careers=careers,
        has_skills=bool(saved_skills),
    )
@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

# Career One Stop

## Project Overview

Career One Stop is a web application designed to help users organize their skills and take steps toward their career goals. The project provides a centralized place for users to record their skills and begin planning their professional development.

The application is being developed as a collaborative software engineering project, with an emphasis on building a functional, accessible, and user-friendly web experience.

## Current Features

- **Dashboard:** Provides an overview of the user's career-planning information, including saved skills.
- **Skills Management:** Allows users to add and organize their skills.
- **Skill Categories:** Supports organizing skills by category.
- **Proficiency Levels:** Allows users to identify their proficiency level for each skill.
- **Data Storage:** Saves skills so users can access their information within the application.

Additional career-planning features, including career matching, learning plans, and job application tracking, are planned for future development.

## Technology Stack

- **Backend:** Python and Flask
- **Frontend:** HTML, CSS, and JavaScript
- **Database:** SQLAlchemy with a configured database
- **Deployment:** Render
- **Version Control:** Git and GitHub
- **Testing:** Python testing tools

## Getting Started

### View the Live Application

Visit the deployed website:

https://career-one-stop.onrender.com

### Run the Project Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/tooflykayy/career-one-stop.git
   ```

2. Navigate into the project directory:

   ```bash
   cd career-one-stop
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On macOS or Linux:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

4. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the Flask application using the project's configured entry point:

   ```bash
   flask --app app run
   ```

6. Open the local address shown in the terminal, typically:

   http://127.0.0.1:5000

## Project Structure

```text
career-one-stop/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── __init__.py
│   └── models.py
│
├── routes/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── skills.py
│   ├── career_match.py
│   ├── learning_plan.py
│   └── applications.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── skills.html
│   ├── edit_skill.html
│   ├── career_match.html
│   ├── learning_plan.html
│   └── applications.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── tests/
    ├── __init__.py
    ├── test_app.py
    ├── test_skills.py
    └── test_routes.py
```

**Note:** The project also contains a `models/` package for model-related code.

## Deployment

Career One Stop is deployed on Render, making the application accessible through a public URL.

- **Live application:** https://career-one-stop.onrender.com
- **Source code:** https://github.com/tooflykayy/career-one-stop

## Future Development

Planned enhancements include:

- **Career Matching:** Compare users' saved skills with the skills associated with different career paths.
- **Learning Plans:** Help users identify skill gaps and organize learning goals.
- **Job Application Tracking:** Provide a way to organize job applications and monitor their progress.
- **Testing and Quality Assurance:** Expand automated tests to verify application functionality and reliability.

## Project Goal

The goal of Career One Stop is to create a practical career-planning tool that helps users understand their existing skills, identify opportunities for growth, and take organized steps toward their professional goals.

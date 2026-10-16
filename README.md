# Career One Stop

A cloud-based career platform to help students connect their skills with employment opportunities by identifying skill gaps, finding learning resources, and tracking job applications.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](#requirements)
[![Docker](https://img.shields.io/badge/docker-ready-green.svg)](#docker)

Table of contents
- [About](#about)
- [Target users](#target-users)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [Docker](#docker)
- [Configuration](#configuration)
- [Testing](#testing)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements & Contact](#acknowledgements--contact)

About
-----
The purpose of Career One Stop is to develop a cloud-based career platform that helps students connect their skills with employment opportunities. Many students struggle to identify the skills employers require, find learning resources, organize their skill development, and keep track of job applications. Career One Stop brings these activities together in one centralized platform.

The application allows users to:
- Create a skill profile
- Select a target job
- Compare current skills with job requirements
- Identify skill gaps
- Find relevant learning resources
- Create development plans
- Track job applications

The goal is to help users make informed career decisions, improve their qualifications, and stay organized throughout their job search.

Target users
------------
- College and university students
- Recent graduates and early-career job seekers
- Individuals preparing to enter the workforce
- Career changers looking to identify transferable skills and develop new qualifications

Features
--------
- Personal skill profiles and skill management
- Job-target selection and requirements comparison
- Skill gap detection with recommendations for learning resources
- Development plan creation and progress tracking
- Job application tracking and history
- Simple authentication and dashboard UI

Tech stack
----------
- Python 3.10+
- Flask (web framework)
- Jinja2 templates (templates/)
- Static assets: CSS and JS (static/)
- Optional: Docker for containerized deployment

Getting started (local)
-----------------------
Prerequisites:
- Python 3.10+
- pip
- (Optional) virtualenv or venv

Install and run:
```bash
git clone https://github.com/tooflykayy/career-one-stop.git
cd career-one-stop
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # create .env from example, fill in values
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

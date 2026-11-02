# Career One Stop

A web-based career development platform built with Python and Flask. Career One Stop helps users manage their skills, explore career opportunities, access learning resources, and organize job applications.

## Features

- **User Authentication:** Register, log in, and log out of user accounts.
- **Dashboard:** View a centralized overview of career development information.
- **Skills Management:** Add, edit, and delete skills while organizing them by category and proficiency level.
- **Career Matching:** Explore career options based on a user's skills and identify potential skill gaps.
- **Job Recommendations:** Browse job opportunities aligned with career interests and skills.
- **Learning Plans:** Access learning resources to help develop relevant skills.
- **Application Tracking:** Organize and manage job applications.

## Technology Stack

| Component        | Technologies                                  |
| ---------------- | --------------------------------------------- |
| Frontend         | HTML, CSS, JavaScript                         |
| Backend          | Python, Flask                                 |
| Database         | SQLAlchemy, SQLite / PostgreSQL configuration |
| Authentication   | Flask-Login                                   |
| Security         | CSRF Protection                               |
| Web Server       | Gunicorn                                      |
| Version Control  | Git, GitHub                                   |
| Containerization | Docker                                        |
| Deployment       | Render                                        |

## Getting Started

### Prerequisites

Install the following before running the application locally:

- Python 3
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/tooflykayy/career-one-stop.git
```

### 2. Navigate to the Project Directory

```bash
cd career-one-stop
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Configure the environment variables required by the application, including its secret key and database connection settings, if applicable.

Do not commit secret keys, passwords, or other sensitive configuration values to GitHub.

### 6. Run the Application

```bash
flask --app app run
```

Once the Flask development server starts, access the application locally:

```text
http://127.0.0.1:5000
```

## Docker

Career One Stop is also packaged as a Docker image.

### Build the Docker Image

```bash
docker build -t makayla3/career-one-stop:v1 .
```

### Run the Container

```bash
docker run -p 5001:5000 makayla3/career-one-stop:v1
```

Access the containerized application locally:\`

```text
http://localhost:5001
```

### Docker Hub

The published Docker image is available at:

[https://hub.docker.com/r/makayla3/career-one-stop](https://hub.docker.com/r/makayla3/career-one-stop)

## Deployment

**Live Application:**
[https://career-one-stop.onrender.com/](https://career-one-stop.onrender.com/)

**GitHub Repository:**
[https://github.com/tooflykayy/career-one-stop](https://github.com/tooflykayy/career-one-stop)

**Docker Hub:**
[https://hub.docker.com/r/makayla3/career-one-stop](https://hub.docker.com/r/makayla3/career-one-stop)

## Developers

Makayla Waleed and Shymik Smith

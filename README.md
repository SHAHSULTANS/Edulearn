EduLearn - Online Course Platform

Introduction
EduLearn is a Django-based web platform for managing and delivering online courses. It allows users to browse, enroll in, and review courses, while instructors can create and manage course content. The platform includes user authentication, payment processing, and a responsive interface powered by Bootstrap.
This README provides a clear, step-by-step guide to setting up, running, and contributing to the project.
Table of Contents

Key Features
Technology Stack
Project Structure
Prerequisites
Setup Instructions
Running the Application
API Usage
Troubleshooting
Contributing
License

Key Features

User Authentication: Register, log in, and manage user profiles with support for password resets.
Course Management: Create, edit, and organize courses, sections, and lessons.
Payment Processing: Secure checkout for course purchases with success and cancellation pages.
Course Reviews: Users can leave feedback and ratings for courses.
Responsive Design: Mobile-friendly interface using Bootstrap CSS and JavaScript.
Admin Panel: Manage courses, users, and payments via Django’s admin interface.
API Support: Access course and enrollment data via Django REST Framework.

Technology Stack

Backend: Django (Python)
Frontend: HTML5, CSS3, JavaScript, Bootstrap
Database: SQLite (Development), PostgreSQL-compatible for production
API: Django REST Framework
Static Files: Bootstrap, custom CSS/JavaScript
Deployment: Heroku-compatible with Procfile and runtime.txt

Dependencies are listed in requirements.txt. Ensure you have the required versions installed.
Project Structure
Here’s an overview of the project’s directory structure:
EduLearn/
├── app/                    # Migration-related files
├── core/                   # Core functionality and shared models
│   ├── management/         # Custom commands (e.g., runserver.py)
│   ├── migrations/         # Database migrations
│   ├── models.py           # Core database models
│   └── views.py            # Core request handling
├── courses/                # Course management
│   ├── management/         # Custom commands (e.g., populate_db.py)
│   ├── migrations/         # Course-related migrations
│   ├── static/             # CSS, JS for courses
│   ├── templates/courses/  # Course-related templates (e.g., course_detail.html)
│   ├── models.py           # Course, section, lesson models
│   └── serializers.py      # API serializers
├── jobapp/                 # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   ├── manage.py           # Django management script
│   └── Procfile            # Deployment configuration
├── payments/               # Payment processing
│   ├── templates/payments/ # Payment templates (e.g., checkout.html)
│   └── models.py           # Payment models
├── reviews/                # Course review system
│   ├── models.py           # Review models
│   └── urls.py             # Review URLs
├── users/                  # User authentication and profiles
│   ├── static/             # User-related static files (e.g., edulearn.svg)
│   ├── templates/users/    # User templates (e.g., login.html, register.html)
│   └── forms.py            # User forms
├── media/                  # Uploaded files (e.g., course thumbnails)
├── static/                 # Static files (Bootstrap CSS/JS)
├── staticfiles/            # Collected static files for production
└── templates/              # Base templates (e.g., base.html)

Prerequisites

Python (version specified in runtime.txt, typically 3.8+)
pip (Python package manager)
Virtualenv (recommended for isolated environments)
SQLite (included with Python, used for development)
Git (optional, for cloning the repository)

Setup Instructions

Clone the Repository (if applicable):
git clone <repository-url>
cd EduLearn


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Apply Database Migrations:
python manage.py makemigrations
python manage.py migrate


Create a Superuser:
python manage.py createsuperuser

Follow the prompts to set a username, email, and password.

(Optional) Populate the Database:Run the custom command to add sample data:
python manage.py populate_db


Collect Static Files:
python manage.py collectstatic



Running the Application

Start the development server:python manage.py runserver


Open http://localhost:8000 in your browser to view the application.
Access the admin panel at http://localhost:8000/admin using your superuser credentials.

API Usage
EduLearn includes API endpoints via Django REST Framework. Example request to fetch course details:
import requests

response = requests.get(
    'http://localhost:8000/api/courses/',
    headers={'Authorization': 'Token YOUR_API_TOKEN'},
    params={'course_id': 1}
)
print(response.json())

To obtain an API token, use the admin panel or authenticate via the /api/auth/ endpoint.
Troubleshooting

Migration Errors:

Ensure all apps are properly installed in settings.py.
Run:python manage.py makemigrations
python manage.py migrate




Static Files Not Loading:

Collect static files:python manage.py collectstatic


Verify STATIC_URL and STATIC_ROOT in settings.py.


Database Issues:

Check if db.sqlite3 is writable.
Delete db.sqlite3 and re-run migrations if necessary.


API Authentication Errors:

Ensure you’re using a valid token or check the /api/auth/ endpoint for token generation.



Contributing
We welcome contributions! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

For major changes, please open an issue to discuss your ideas first.
License
This project is licensed under the MIT License. See the LICENSE file for details.
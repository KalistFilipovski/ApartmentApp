# ApartmentApp
# Apartment Listing Web Application
## About the Application
This is a web application for listing and managing apartments. Users can view apartment details, and administrators can create, edit, and delete apartment listings. The application uses Flask for the backend and integrates Mapbox for location services.

## Technologies Used
- Flask: Web framework for building the backend of the application.
- Flask-Migrate: Extension for handling database migrations.
- Flask-WTF: Integration with WTForms for form handling.
- Flask-Login: User session management.
- SQLAlchemy: ORM for database interactions.
- SQLite: Database used for development and testing.
- Mapbox: Location services and geocoding.
- HTML/CSS: For templating and styling.
- Bootstrap: Frontend framework for responsive design.
- Jinja2: Templating engine for Flask.
- Pytest: For testing the application.
- Pycodestyle: For checking PEP8 compliance.
- Features
- User registration and login.
- User profile management with profile image upload.
- Listing apartments with search functionality.
- Detailed view of each apartment.
- Admin functionalities for creating, editing, and deleting apartment listings.
- Integration with Mapbox for location input and display.
- Installation and Setup
- Prerequisites
- Python 3.11 or later
- pip (Python package installer)
- SQLite (installed with Python)

## Installation

### Clone the repository:
``` bash
git clone https://github.com/yourusername/apartment-listing-webapp.git
cd apartment-listing-webapp
``` 

### Create a virtual environment and activate it:
``` bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### Install the required packages:
``` bash
pip install -r requirements.txt
```

### Set up the database:
``` bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
``` 

### Run the application:
``` bash
cd backend
python main.py
``` 

### Access the application in your web browser:
http://127.0.0.1:5000
Running Tests

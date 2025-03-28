# Flask Task Manager with PostgreSQL, DataTables, and AJAX

## Overview
This is a Flask-based web application for managing tasks with the following features:
- Create, read, update, and delete (CRUD) tasks
- Search and pagination using DataTables
- PostgreSQL database backend
- AJAX-powered interface
- Responsive design with Bootstrap

## Features
- **Task Management**:
  - Add new tasks with content and category
  - Edit existing tasks
  - Delete tasks
- **Data Display**:
  - Interactive table with sorting and filtering
  - Server-side pagination
  - Real-time updates without page reloads
- **Database**:
  - PostgreSQL integration
  - SQLAlchemy ORM
  - Database migrations with Flask-Migrate

## Prerequisites
- Python 3.7+
- PostgreSQL
- pip

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-task-manager.git
   cd flask-task-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Create a database named `db`
   - Update the connection string in `app.py`:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db'
     ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Running the Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Project Structure
```
flask-task-manager/
├── app.py                # Main application file
├── migrations/           # Database migration files
├── static/
│   ├── css/
│   │   └── main.css      # Custom CSS
│   └── js/
│       └── main.js       # JavaScript for DataTables and AJAX
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main page with task table
│   └── update.html       # Task update form
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Migrate
- psycopg2 (PostgreSQL adapter)
- WTForms
- jQuery (via CDN)
- DataTables (via CDN)
- Bootstrap (via CDN)
- Font Awesome (via CDN)

## API Endpoints
- `GET /` - Main application page
- `POST /` - Add new task
- `GET /update/<id>` - Edit task form
- `POST /update/<id>` - Update task
- `GET /delete/<id>` - Delete task
- `GET /api/tasks` - JSON API for DataTables (supports pagination and search)

## Customization
- To change the number of tasks per page, modify the `length` parameter in `main.js`
- To add more categories, update the `choices` in the `TodoForm` class
- To change the database, update the `SQLALCHEMY_DATABASE_URI` in `app.py`
# FlaskProjec

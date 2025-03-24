from operator import or_
from flask import Flask, render_template, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_migrate import Migrate
from math import ceil
from sqlalchemy import or_

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@127.0.0.1/db'  # PostgreSQL connection
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for CSRF protection in Flask-WTF
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy and database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)  # New column
    datecreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Define the TodoForm
class TodoForm(FlaskForm):
    content = StringField('Task', validators=[DataRequired()])
    category = SelectField('Category', choices=[('work', 'Work'), ('personal', 'Personal'), ('shopping', 'Shopping')])
    submit = SubmitField('Add Task')

# Route for the home page
@app.route('/', methods=['POST', 'GET'])
def index():
    form = TodoForm()  # Instantiate the form
    if form.validate_on_submit():  # Validate form on submission
        new_task = Todo(content=form.content.data, category=form.category.data)  # Create a new task with category
        db.session.add(new_task)  # Add task to the session
        db.session.commit()  # Commit changes to the database
        return redirect('/')  # Redirect to the home page
    
    tasks = Todo.query.order_by(Todo.datecreated).all()  # Retrieve all tasks
    return render_template('index.html', tasks=tasks, form=form)  # Render the template with tasks and form

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # Find the task by ID
    db.session.delete(task_to_delete)  # Delete the task
    db.session.commit()  # Commit changes
    return redirect('/')  # Redirect to the home page

# Route to update a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)  # Find the task by ID
    form = TodoForm(obj=task)  # Prepopulate the form with task data
    if form.validate_on_submit():  # Validate form on submission
        task.content = form.content.data  # Update task content
        task.category = form.category.data  # Update task category
        db.session.commit()  # Commit changes
        return redirect('/')  # Redirect to the home page
    return render_template('update.html', form=form, task=task)  # Render the update template

# API endpoint to fetch tasks for DataTables
@app.route('/api/tasks')
def get_tasks():
    # Get pagination parameters from the request
    page = request.args.get('page', default=1, type=int)  # Default to page 1
    length = request.args.get('length', default=10, type=int)  # Default to 10 tasks per page

    # Calculate offset and limit for pagination
    offset = (page - 1) * length
    limit = length

    # Get search query from DataTables
    search_query = request.args.get('search[value]', '')

    # Query tasks with search and pagination
    tasks_query = Todo.query.filter(or_(
    Todo.content.ilike(f'%{search_query}%'), 
    Todo.category.ilike(f'%{search_query}%'),)
    
)
    total_tasks = tasks_query.count()  # Total number of tasks matching the search
    tasks = tasks_query.order_by(Todo.datecreated).offset(offset).limit(limit).all()

    # Prepare the response
    response = {
        'data': [{'id': task.id, 'content': task.content, 'category': task.category, 'datecreated': task.datecreated} for task in tasks],
        'recordsTotal': total_tasks,  # Total number of tasks without filtering
        'recordsFiltered': total_tasks,  # Total number of tasks after filtering
        'page': page,
        'length': length,
        'total_pages': ceil(total_tasks / length)  # Total number of pages
    }

    return jsonify(response)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
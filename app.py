from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking overhead
with app.app_context():
 db = SQLAlchemy(app)  # Initialize SQLAlchemy

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Serial Number (Primary Key)
    title = db.Column(db.String(200), nullable=False)  # Task Title
    desc = db.Column(db.String(500), nullable=False)  # Task Description
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Define the home route
@app.route("/", methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Create a new Todo object and save it to the database
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        # Redirect to the home page after submitting the form
        return redirect('/')
    
    # Handle GET request and fetch all todos
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


# Define the products route

@app.route('/Update/<int:sno>', methods=['GET', 'POST'])
def Update(sno):
    # Fetch the todo item first
    todo = Todo.query.filter_by(sno=sno).first()

    # Check if todo is not found
    if not todo:
        return "Todo not found", 404

    # Handle POST request
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        # Update the todo object with new values
        todo.title = title
        todo.desc = desc

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the home page after updating
        return redirect('/')

    # For GET request, render the update form with the current todo values
    return render_template('updates.html', todo=todo)


@app.route('/Delete/<int:sno>')
def Delete(sno):
    db.session.delete(Todo.query.filter_by(sno=sno).first())  # Directly delete the fetched Todo object
    db.session.commit()  # Commit the changes to the database
    return redirect('/')  # Redirect after deletion

# Main entry point
if __name__ == "__main__":
    # Ensure the database and tables are created before starting the app
    with app.app_context():
        db.create_all()  # Create tables if they don't already exist
    app.run(debug=True, port=8000)  # Run the Flask app on port 8000

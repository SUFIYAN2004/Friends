from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Adjust the URI as needed
db = client["school"]
collection = db["students"]
users_collection = db["users"]  # New collection for users

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        query = request.args.get('query', '')  # Get the search query from the URL
        if query:
            students = list(collection.find({"$or": [
                {"name": {"$regex": query, "$options": "i"}},  # Case-insensitive search by name
                {"rollno": {"$regex": query, "$options": "i"}}  # Case-insensitive search by roll number
            ]}))
        else:
            students = list(collection.find())  # Fetch all students if no query
        return render_template('index.html', students=students, query=query)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        flash('Signup successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or password!')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    rollno = request.form['rollno']
    number = request.form['number']
    dept = request.form['dept']
    address = request.form['address']

    existing_student = collection.find_one({"rollno": rollno})
    if not existing_student:
        student = {
            "name": name,
            "rollno": rollno,
            "number": number,
            "dept": dept,
            "address": address
        }
        collection.insert_one(student)
    return redirect(url_for('index'))

@app.route('/delete/<rollno>', methods=['POST'])
def delete_student(rollno):
    collection.delete_one({"rollno": rollno})
    return redirect(url_for('index'))

@app.route('/show/<rollno>')
def show_student(rollno):
    student = collection.find_one({"rollno": rollno})
    return render_template('show.html', student=student)

@app.route('/edit/<rollno>', methods=['GET', 'POST'])
def edit_student(rollno):
    if request.method == 'POST':
        # Update student details
        name = request.form['name']
        number = request.form['number']
        dept = request.form['dept']
        address = request.form['address']

        collection.update_one(
            {"rollno": rollno},
            {"$set": {
                "name": name,
                "number": number,
                "dept": dept,
                "address": address
            }}
        )
        return redirect(url_for('index'))

    # If it's a GET request, fetch the student details
    student = collection.find_one({"rollno": rollno})
    return render_template('edit.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)

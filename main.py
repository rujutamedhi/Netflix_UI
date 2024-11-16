from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
local_server =True
app = Flask(__name__, static_folder='static')
with open("C:\\projects\\netflix\\config.json") as c:
     params=json.load(c)["params"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rujutamedhi%4004@localhost/netflix'

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phno = db.Column(db.String(20))
    password = db.Column(db.String(100))

# Create the database tables
    with app.app_context():

      db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    

@app.route('/success')
def success():
    return 'User added successfully!'

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to check if the email and password match
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            # If a user with the provided email and password exists, redirect to index page
            return redirect(url_for('index'))
        else:
            # If no matching user found, redirect back to the login page
            return redirect(url_for('login'))

    # Render the login page template for GET requests
    return render_template('signin.html')

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    print("test0")
    print(request.method)
    if request.method == 'POST':
        print("test")
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        password = request.form['password']
        
        # Create a new user instance
        new_user = User(name=name, email=email, phno=phno, password=password)
        
        # Add the new user to the database session
        db.session.add(new_user)
        
        # Commit the session to the database
        db.session.commit()
        
        return render_template('signin.html')
    return render_template('signup.html',params=params)
    


app.run(debug=True)

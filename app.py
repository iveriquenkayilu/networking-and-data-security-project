from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
import os
from flask_cors import CORS


# Generate a random 32-byte (256-bit) key
secret_key = os.urandom(32)
# from models import User
# from .user import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)
CORS(app, supports_credentials=True)



db = SQLAlchemy(app)

# Sample data - you can replace this with your own data source
posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
    # Add more posts as needed
]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Endpoint to get one post by ID
@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post), 200
    else:
        return jsonify({"error": "Post not found"}), 404


# Endpoint to create a new post
@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'title' in data and 'content' in data:
        new_post = {
            "id": len(posts) + 1,
            "title": data['title'],
            "content": data['content']
        }
        posts.append(new_post)
        return jsonify(new_post), 201
    else:
        return jsonify({"error": "Title and content are required"}), 400


# Endpoint to serve HTML page
@app.route('/')
def home():
    return render_template('index.html')
#
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)
#
#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#
#         return redirect(url_for('login'))
#
#     return render_template('signup.html')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         hashed_password = generate_password_hash(password)
#
#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Account created successfully! Please log in.')
#
#         return redirect(url_for('login'))
#     else:
#         # Form validation failed
#         print(form.errors)  # Print form validation errors to console for debugging
#         flash('Form validation failed. Please check your inputs.')
#
#     return render_template('signup.html', form=form)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check if the password matches the confirm password
        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return render_template('signup.html', form=form)

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login-unsafe', methods=['GET', 'POST'])
def loginunsafe():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'csrf_token' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/csrf-attack-prone-login')
def csrf_attack():
    # Render the CSRF attack HTML page
    return render_template('csrf_attack_login.html')

@app.route('/csrf-attack-safe-signup')
def csrf_attack_signup():
    # Render the CSRF attack HTML page
    return render_template('csrf_attack_signup.html')

if __name__ == '__main__':
    with app.app_context():

        db.create_all()
    app.run(debug=True)
    # app.run(port=8080)
    #app.run(port=5001, host='127.0.0.1')


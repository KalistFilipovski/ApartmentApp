from flask import Flask, render_template, redirect, url_for, flash
from forms.user_form import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from models.user_model import User, db
import os

# Initializing Flask app
template_dir = os.path.abspath('../frontend/templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = '@$(aegta$*ae@)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy database
db.init_app(app)

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Creating all tables in the database
with app.app_context():
    db.create_all()

# Loading user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Index route
@app.route('/')
def index():
    user = current_user if current_user.is_authenticated else None
    return render_template('index.html', current_user=user)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, full_name=form.full_name.data, bio=form.bio.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html', title='Log In', form=form)

# User logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# Running the app
if __name__ == '__main__':
    app.run(debug=True)

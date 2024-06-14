from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
import os

from models.user_model import User, db
from models.apartment_model import Apartment

from forms.user_form import RegisterForm, LoginForm
from forms.apartment_form import ApartmentForm  


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

# User profile route
@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)

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

# Apartment management route
@app.route('/admin/apartments', methods=['GET', 'POST'])
@login_required
def create_apartments():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('index'))
    
    form = ApartmentForm()
    if form.validate_on_submit():
        new_apartment = Apartment(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_apartment)
        db.session.commit()
        flash('Apartment added successfully.', 'success')
        return redirect(url_for('create_apartments'))
    
    return render_template('create_apartments.html', form=form)

# Apartment list route
@app.route('/apartments')
def list_apartments():
    apartments = Apartment.query.all()
    return render_template('list_apartments.html', apartments=apartments)

# Delete apartment route
@app.route('/delete_apartment/<int:apartment_id>', methods=['DELETE'])
@login_required
def delete_apartment(apartment_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    apartment = Apartment.query.get_or_404(apartment_id)
    db.session.delete(apartment)
    db.session.commit()
    flash('Apartment deleted successfully.', 'success')
    return redirect(url_for('manage_apartments'))

# Running the app
if __name__ == '__main__':
    app.run(debug=True)

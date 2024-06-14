from flask import Flask, render_template, redirect, url_for, flash, request
from forms.user_form import RegisterForm, LoginForm
from forms.apartment_form import ApartmentForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from models.user_model import User, db
from models.apartment_model import Apartment
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os

# Initializing Flask app
template_dir = os.path.abspath('../frontend/templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = '@$(aegta$*ae@)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initializing SQLAlchemy database
db.init_app(app)

# Initializing Flask-Migrate
migrate = Migrate(app, db)

# Initializing CSRF protection
csrf = CSRFProtect(app)

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Creating all tables in the database
with app.app_context():
    db.create_all()

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Loading user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Index route
@app.route('/')
def index():
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('index.html', user=user)

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

# User profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# List apartments route
@app.route('/apartments')
def list_apartments():
    apartments = Apartment.query.all()
    return render_template('list_apartments.html', apartments=apartments)

# Manage apartments route
@app.route('/create_apartments', methods=['GET', 'POST'])
@login_required
def create_apartments():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    form = ApartmentForm()
    if form.validate_on_submit():
        if form.photo.data and allowed_file(form.photo.data.filename):
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        new_apartment = Apartment(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            price=form.price.data,
            photo=filename
        )
        db.session.add(new_apartment)
        db.session.commit()
        flash('Apartment added successfully.', 'success')
        return redirect(url_for('list_apartments'))

    apartments = Apartment.query.all()
    return render_template('create_apartments.html', form=form, apartments=apartments)

# Delete apartment route
@app.route('/delete_apartment/<int:apartment_id>', methods=['POST'])
@login_required
def delete_apartment(apartment_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    apartment = Apartment.query.get_or_404(apartment_id)
    db.session.delete(apartment)
    db.session.commit()
    flash('Apartment deleted successfully.', 'success')
    return redirect(url_for('list_apartments'))

# Apartment detail route
@app.route('/apartment/<int:apartment_id>')
def apartment_detail(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    return render_template('detail_apartments.html', apartment=apartment)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from forms.user_form import RegisterForm, LoginForm
from forms.apartment_form import ApartmentForm
from forms.upload_photo import UploadForm
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
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024 

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initializing SQLAlchemy database
db.init_app(app)

# Initializing Flask-Migrate
migrate = Migrate(app, db)

# Initializing CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Creating all tables in the database
with app.app_context():
    db.create_all()

# Function to check allowed file extensions
def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    :param filename: The name of the file to check.
    :return: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Loading user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by their user ID.

    :param user_id: The user ID to load.
    :return: The user object if found, None otherwise.
    """
    return User.query.get(int(user_id))

# Index route
@app.route('/')
def index():
    """
    Render the index page.

    :return: The rendered index page template.
    """
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('index.html', user=user)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    Render the registration form and process the form submission.
    If the form is valid, create a new user and redirect to the login page.

    :return: The rendered registration page template or a redirect to the login page.
    """
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
    """
    Handle user login.

    Render the login form and process the form submission.
    If the form is valid and credentials are correct, log in the user and redirect to the index page.

    :return: The rendered login page template or a redirect to the index page.
    """
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
    """
    Handle user logout.

    Log out the current user and redirect to the index page.

    :return: A redirect to the index page.
    """
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# List apartments route
@app.route('/apartments', methods=['GET', 'POST'])
def list_apartments():
    """
    List all apartments or search for apartments by name or location.

    :return: The rendered list of apartments page template.
    """
    search = request.args.get('search')
    if search:
        apartments = Apartment.query.filter(Apartment.name.contains(search) | Apartment.location.contains(search)).all()
    else:
        apartments = Apartment.query.all()
    return render_template('list_apartments.html', apartments=apartments)

# Manage apartments route
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/create_apartments', methods=['GET', 'POST'])
def create_apartments():
    """
    Handle the creation of new apartments.

    Render the apartment creation form and process the form submission.
    If the form is valid, create a new apartment and redirect to the list of apartments.

    :return: The rendered apartment creation page template or a redirect to the list of apartments page.
    """
    form = ApartmentForm()
    if form.validate_on_submit():
        photo_filename = None
        if form.photo.data:
            photo_file = form.photo.data
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        
        new_apartment = Apartment(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data,
            price=form.price.data,
            photo=photo_filename
        )
        db.session.add(new_apartment)
        db.session.commit()
        flash('Apartment created successfully!', 'success')
        return redirect(url_for('list_apartments'))
    return render_template('create_apartments.html', form=form)

# Delete apartment route
@app.route('/delete_apartment/<int:apartment_id>', methods=['POST'])
@login_required
def delete_apartment(apartment_id):
    """
    Handle the deletion of an apartment.

    Only admin users can delete apartments. If the current user is not an admin,
    a permission error is shown. If the user is an admin, the apartment is deleted.

    :param apartment_id: The ID of the apartment to delete.
    :return: A redirect to the list of apartments page.
    """
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
    """
    Display the details of a specific apartment.

    :param apartment_id: The ID of the apartment to display.
    :return: The rendered apartment detail page template.
    """
    apartment = Apartment.query.get_or_404(apartment_id)
    return render_template('detail_apartments.html', apartment=apartment)

# Apartment edit route

@app.route('/apartment/<int:apartment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_apartment(apartment_id):
    """
    Handle the editing of an apartment.

    Only admin users can edit apartments. If the current user is not an admin,
    a permission error is shown. If the user is an admin, the apartment is updated
    with the new data from the form submission.

    :param apartment_id: The ID of the apartment to edit.
    :return: The rendered apartment edit page template or a redirect to the apartment detail page.
    """
    apartment = Apartment.query.get_or_404(apartment_id)
    if not current_user.is_admin:
        flash('You do not have permission to edit this apartment.')
        return redirect(url_for('apartment_detail', apartment_id=apartment_id))

    form = ApartmentForm(obj=apartment)
    if form.validate_on_submit():
        # Update fields
        apartment.name = form.name.data
        apartment.location = form.location.data
        apartment.description = form.description.data
        apartment.price = form.price.data
        
        # Handle file upload
        if form.photo.data:
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            apartment.photo = filename

        db.session.commit()
        flash('Apartment updated successfully.')
        return redirect(url_for('apartment_detail', apartment_id=apartment.id))

    return render_template('edit_apartment.html', form=form, apartment=apartment)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and update the user's profile.

    Render the profile page with a form to upload a profile image.
    If the form is valid and the file extension is allowed, save the file
    and update the user's profile image.

    :return: The rendered profile page template.
    """
    form = UploadForm()
    if form.validate_on_submit():
        file = form.profile_image.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            current_user.profile_image = filename
            db.session.commit()
            flash('Profile image uploaded successfully', 'success')
            return redirect(url_for('profile'))

    profile_image_url = current_user.profile_image_url
    return render_template('profile.html', user=current_user, profile_image_url=profile_image_url, form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve the uploaded files.

    :param filename: The name of the file to serve.
    :return: The file from the upload directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)

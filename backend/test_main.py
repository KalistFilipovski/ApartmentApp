import unittest
from main import app, db
from models.user_model import User
from models.apartment_model import Apartment
from flask import url_for
from werkzeug.security import generate_password_hash

class TestApp(unittest.TestCase):
    """
    A test case for the Flask application.

    This test case sets up a testing environment for the Flask application,
    including creating a test database and adding a test user. It includes
    tests for user registration, user login, and apartment creation.
    """
    
    def setUp(self):
        """
        Set up the test environment.

        This method is called before each test. It configures the Flask application
        for testing, creates a test database, and adds a test user.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SERVER_NAME'] = 'localhost.localdomain'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.test_user = User(username='testuser', email='test@example.com',
                              password=generate_password_hash('password', method='pbkdf2:sha256'),
                              full_name='Test User')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """
        Tear down the test environment.

        This method is called after each test. It removes the database session,
        drops all tables, and pops the application context.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """
        Test user registration.

        This test sends a POST request to the 'register' endpoint with user data
        and checks if the response status code is 200 and if the new user is
        added to the database.
        """
        with app.test_request_context():
            response = self.app.post(url_for('register'), data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'newpassword',
                'confirm_password': 'newpassword',
                'full_name': 'New User'
            }, follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 200)
            new_user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(new_user)

    def test_user_login(self):
        """
        Test user login.

        This test sends a POST request to the 'login' endpoint with user credentials
        and checks if the response status code is 200 and if the login message is
        present in the response data.
        """
        with app.test_request_context():
            response = self.app.post(url_for('login'), data={
                'email': 'test@example.com',
                'password': 'password'
            }, follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Logged in successfully.', response.data)

    def test_create_apartment(self):
        """
        Test apartment creation.

        This test logs in as a user, sends a POST request to the 'create_apartments'
        endpoint with apartment data, and checks if the response status code is 200
        and if the new apartment is added to the database.
        """
        with app.test_request_context():
            self.app.post(url_for('login'), data={
                'email': 'test@example.com',
                'password': 'password'
            }, follow_redirects=True)

            response = self.app.post(url_for('create_apartments'), data={
                'name': 'Test Apartment',
                'location': 'Test Location',
                'description': 'Test Description',
                'price': '1000'
            }, follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 200)
            apartment = Apartment.query.filter_by(name='Test Apartment').first()
            self.assertIsNotNone(apartment)

    def test_delete_apartment_as_admin(self):
        """
        Test apartment deletion as an admin user.

        This test creates an admin user, logs in as the admin, creates an apartment,
        sends a POST request to the 'delete_apartment' endpoint, and checks if the
        response status code is 200 and if the apartment is deleted from the database.
        """
        with app.test_request_context():
            admin_user = User(username='admin', email='admin@example.com',
                              password=generate_password_hash('adminpassword', method='pbkdf2:sha256'),
                              full_name='Admin User', is_admin=True)
            db.session.add(admin_user)
            db.session.commit()

            self.app.post(url_for('login'), data={
                'email': 'admin@example.com',
                'password': 'adminpassword'
            }, follow_redirects=True)

            apartment = Apartment(name='Delete Test Apartment', location='Test Location', description='Test Description', price='1000')
            db.session.add(apartment)
            db.session.commit()

            response = self.app.post(url_for('delete_apartment', apartment_id=apartment.id), follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 200)
            deleted_apartment = Apartment.query.filter_by(name='Delete Test Apartment').first()
            self.assertIsNone(deleted_apartment)

    def test_edit_apartment_as_admin(self):
        """
        Test apartment editing as an admin user.

        This test creates an admin user, logs in as the admin, creates an apartment,
        sends a POST request to the 'edit_apartment' endpoint with updated data,
        and checks if the response status code is 200 and if the apartment is updated
        in the database.
        """
        with app.test_request_context():
            admin_user = User(username='admin', email='admin@example.com',
                              password=generate_password_hash('adminpassword', method='pbkdf2:sha256'),
                              full_name='Admin User', is_admin=True)
            db.session.add(admin_user)
            db.session.commit()

            self.app.post(url_for('login'), data={
                'email': 'admin@example.com',
                'password': 'adminpassword'
            }, follow_redirects=True)

            apartment = Apartment(name='Edit Test Apartment', location='Test Location', description='Test Description', price='1000')
            db.session.add(apartment)
            db.session.commit()

            response = self.app.post(url_for('edit_apartment', apartment_id=apartment.id), data={
                'name': 'Edited Apartment',
                'location': 'Edited Location',
                'description': 'Edited Description',
                'price': '2000'
            }, follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 200)
            edited_apartment = Apartment.query.filter_by(id=apartment.id).first()
            self.assertEqual(edited_apartment.name, 'Edited Apartment')
            self.assertEqual(edited_apartment.location, 'Edited Location')

    def test_delete_apartment_as_non_admin(self):
        """
        Test apartment deletion as a non-admin user.

        This test creates a non-admin user, logs in as the non-admin, creates an apartment,
        sends a POST request to the 'delete_apartment' endpoint, and checks if the response
        status code is 403 (Forbidden) and if the apartment is not deleted from the database.
        """
        with app.test_request_context():
            non_admin_user = User(username='nonadmin', email='nonadmin@example.com',
                                  password=generate_password_hash('nonadminpassword', method='pbkdf2:sha256'),
                                  full_name='Non-Admin User', is_admin=False)
            db.session.add(non_admin_user)
            db.session.commit()

            self.app.post(url_for('login'), data={
                'email': 'nonadmin@example.com',
                'password': 'nonadminpassword'
            }, follow_redirects=True)

            apartment = Apartment(name='Delete Test Apartment Non-Admin', location='Test Location', description='Test Description', price='1000')
            db.session.add(apartment)
            db.session.commit()

            response = self.app.post(url_for('delete_apartment', apartment_id=apartment.id), follow_redirects=True)
            print(response.data)  # Add this line
            self.assertEqual(response.status_code, 403)  # Forbidden
            non_deleted_apartment = Apartment.query.filter_by(name='Delete Test Apartment Non-Admin').first()
            self.assertIsNotNone(non_deleted_apartment)

if __name__ == '__main__':
    unittest.main()

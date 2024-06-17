import unittest
import os
from main import app, db
from models.user_model import User
from models.apartment_model import Apartment


class TestModels(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        # Test creating a new user
        user = User(username='test_user', email='test@example.com',
                    password='password', full_name='Test User')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_create_apartment(self):
        # Test creating a new apartment
        apartment = Apartment(name='Test Apartment', location='Test Location',
                              description='Test Description', price=1000)
        db.session.add(apartment)
        db.session.commit()
        self.assertIsNotNone(apartment.id)


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        # Test registering a new user
        response = self.app.post('/register', data=dict(
            username='test_user', email='test@example.com',
            password='password', full_name='Test User'
        ), follow_redirects=True)
        self.assertIn(b'Account created successfully', response.data)


if __name__ == '__main__':
    unittest.main()

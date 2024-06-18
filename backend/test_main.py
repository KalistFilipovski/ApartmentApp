import unittest
from main import app, db


from models.user_model import User
from models.apartment_model import Apartment


class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        # Example test creating a new user
        new_user = User(username='tuser', email='t@example.com',
                        password='securepassword', full_name='alenser')
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username='tuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 't@example.com')
        self.assertEqual(user.password, 'securepassword')


if __name__ == '__main__':
    unittest.main()

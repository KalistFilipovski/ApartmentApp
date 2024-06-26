from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import url_for
db = SQLAlchemy()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(100), default='default.jpg')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def profile_image_url(self):
        if self.profile_image and self.profile_image != 'default.jpg':
            return url_for('static', filename='uploads/' + self.profile_image)
        return url_for('static', filename='uploads/default.jpg')
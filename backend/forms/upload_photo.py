from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[DataRequired()])

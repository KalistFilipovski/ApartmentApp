from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Length


class ApartmentForm(FlaskForm):
    name = StringField(
        'Name', validators=[DataRequired(), Length(min=2, max=50)]
    )
    location = StringField(
        'Location', validators=[DataRequired(), Length(min=2, max=100)]
    )
    description = TextAreaField(
        'Description', validators=[DataRequired(), Length(min=10, max=500)]
    )
    price = IntegerField('Price', validators=[DataRequired()])
    photo = FileField('Photo')

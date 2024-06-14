from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired

# Form for creating an apartment
class ApartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    photo = FileField('Photo')
    submit = SubmitField('Add Apartment')

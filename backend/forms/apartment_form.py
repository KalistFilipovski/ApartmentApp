from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField
from wtforms import FileField, SubmitField
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
    price = DecimalField('Price')
    photo = FileField('Photo')
    submit = SubmitField('submit')

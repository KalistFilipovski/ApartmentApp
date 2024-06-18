from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# Form for registering a user
class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=50)]
    )
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), Length(min=6, max=50)]
    )
    full_name = StringField(
        'Full Name', validators=[DataRequired(), Length(min=2, max=50)]
    )
    bio = TextAreaField('Bio', validators=[Length(max=200)])

    submit = SubmitField('Register')


# Form for logging in a user
class LoginForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

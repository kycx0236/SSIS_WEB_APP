from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class Courses(FlaskForm):
    course_code = StringField('college_code', [validators.DataRequired(), validators.Length(min=3, max=20)])
    course_name = StringField('college_name', [validators.Length(min=3, max=100)])
    college_code = StringField('college_code', [validators.DataRequired(), validators.Length(min=9, max=20)])
    submit = SubmitField("Submit")

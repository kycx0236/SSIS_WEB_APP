from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class CourseForm(FlaskForm):
    course_code = StringField('college_code', [validators.DataRequired(), validators.Length(min=1, max=20)])
    course_name = StringField('college_name', [validators.Length(min=1, max=100)])
    college_code = StringField('college_code', [validators.DataRequired(), validators.Length(min=1, max=20)])
    submit = SubmitField("Submit")

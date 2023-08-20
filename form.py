from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class AddForm(FlaskForm):
    task = StringField('Enter the Task: ')
    submit = SubmitField('Add Task')

class DelForm(FlaskForm):
    id = IntegerField('Task No: ')
    submit = SubmitField('Delete Task')


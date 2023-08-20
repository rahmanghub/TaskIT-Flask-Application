########## Imports #############
import os
from form import AddForm,DelForm
from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

########## Initiate app #############

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

########## Database #############

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db =SQLAlchemy(app)
Migrate(app,db)

########## Models #############

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.Text)

    def __init__(self,task):
        self.task=task

    def __repr__(self):
        return f"Task {self.id}: {self.task}"
    
########## VIEW FUNCTIONS #############

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add',methods=['GET','POST'])
def addTask():
    form = AddForm()
    if form.validate_on_submit():
        task = form.task.data
        newTask = Tasks(task)
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for('listTask'))
    return render_template('add.html',form=form)

@app.route('/list')
def listTask():
    tasks = Tasks.query.all()
    return render_template('list.html',tasks = tasks)

@app.route('/delete',methods=['GET','POST'])
def deleteTask():
    form = DelForm()
    if form.validate_on_submit():
        idFilter = form.id.data
        task = Tasks.query.filter_by(id=idFilter).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('listTask'))
        else:
            return redirect(url_for('listTask'))
    return render_template('delete.html',form=form)

if __name__ == "__main__":
    app.run()
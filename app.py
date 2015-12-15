import os
from datetime import date
from flask import Flask, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters, ModelView

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)

app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'detention.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# @app.route('/detention.csv')
# def generate_detention_csv():
# 	def generate():
# 		rows = Detention.query.all()
# 		yield 'Student Name, Assigned By, Reason, Date Assigned, Due By, Attended, 	Date Attended\n'
# 		for row in rows:
# 			yield ', '.join(str(item[1]) for item in row.__dict__.items()[0:]) + '\n'

# 	return Response(generate(), mimetype='text/csv')


class Student(db.Model):
	__tablename__ = 'students'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True)
	email = db.Column(db.String(120), unique=True)
	
	detentions = db.relationship('Detention', backref='student', lazy='dynamic')
	
	def __repr__(self):
		return '{}'.format(self.name)


class Detention(db.Model):
	__tablename__ = 'detentions'
	id = db.Column(db.Integer, primary_key=True)
	student_name = db.Column(db.Integer, db.ForeignKey('students.name'))
	assigned_by = db.Column(db.String(64))
	reason = db.Column(db.Text)
	date_assigned = db.Column(db.Date, default=date.today())
	due_by = db.Column(db.Date)
	attended = db.Column(db.Boolean)
	date_attended = db.Column(db.Date)
	
	def __repr__(self):
		return 'Date: {}'.format(self.date_assigned)

		
class StudentView(ModelView):
	can_create = True
	can_edit = True
	can_delete = True
	form_excluded_columns = ['detentions']
	

class DetentionView(ModelView):
	page_size = 50
	column_list = ('student_name', 'assigned_by', 'reason', 'date_assigned', 'due_by', 'attended', 'date_attended')
	column_filters = ['student.name', 'assigned_by', 'due_by', 'date_assigned', 'attended', 'date_attended']
	form_choices = {'assigned_by': [('Elaine Harper', 'Elaine Harper'), ('Justin Robertson', 'Justin Robertson'), ('Rashaad Williams', 'Rashaad Williams'),
	('Cimone Sanders', 'Cimone Sanders')]}
	
	
admin = admin.Admin(app, name='RBHS Detention Tracker', template_mode='bootstrap3')
admin.add_view(DetentionView(Detention, db.session))
admin.add_view(StudentView(Student, db.session))

if __name__ == '__main__':
	manager.run()

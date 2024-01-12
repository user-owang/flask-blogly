"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
  return redirect('/users')

@app.route('/users')
def list_users():
  """list of all users in table"""
  users = Users.query.all()
  return render_template('users.html', users=users)

@app.route('/users/new')
def show_user_form():
  """Show form to add new user"""
  return render_template('newuser.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
  """Logic to add new user to table"""
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  img_url = request.form['img_url']

  if img_url != '':
    new_user = Users(first_name=first_name, last_name=last_name, img_url=img_url)
  else:
    new_user = Users(first_name=first_name, last_name=last_name)
  db.session.add(new_user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  """display details of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
  """show form to edit detials of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  return render_template('edituser.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
  """logic to edit details of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  if request.form['img_url']:
    user.img_url = request.form['img_url']

  db.session.add(user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  """logic to delete a single user with user.id == user_id from the table"""
  Users.query.filter_by(id=user_id).delete()

  db.session.commit()
  return redirect('/users')

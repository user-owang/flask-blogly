"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts

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

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
  """show form to add a new post as user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  return render_template('newpost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
  """logic to add a new post to table as a user with user.id == user_id"""
  title = request.form['title']
  content = request.form['content']
  user = Users.query.get_or_404(user_id)
  new_post = Posts(title=title, content=content, auth_id=user.id)

  db.session.add(new_post)
  db.session.commit()
  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  """Show post details where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
  """Show form to edit post where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  return render_template('editpost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
  """logic to edit post and update table where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  db.session.add(post)
  db.session.commit()
  return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
  """logic to delete a post with post.id == post_id from the table"""
  post = Posts.query.get_or_404(post_id)
  auth = post.auth_id
  Posts.query.filter_by(id=post_id).delete()

  db.session.commit()
  return redirect(f'/users/{auth}')

"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, User #, make_db, seed_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'chickenzarcool21837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    return redirect('/users', code=302)

@app.route('/users')
def list_users():
    """Shows homepage"""
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def show_form():
    return render_template('/add_user.html')


@app.route('/users/new', methods = ['POST'])
def adduser_form():
    """Shows add user form"""
    firstn=request.form['firstname']
    lastn=request.form['lastname']
    img=request.form['imgurl']

    User.add(firstn, lastn, img)
    return redirect("/", code=302)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows user information"""
    user = User.query.filter_by(id = user_id).first()
    return render_template('showuser.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """Show edit form"""
    user = User.query.filter_by(id = user_id).first()
    return render_template('edituser.html', user = user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    User.edituser(user_id, request)
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete')
def delete(user_id):
    User.delete_user(user_id)
    return redirect('/users')

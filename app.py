"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, get_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.route('/')
def go_home():
    """Shows list of all pets in db"""
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/users/<id>')
def show_user(id):
    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/users/<id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<id>/edit')
def edit_user(id):
    # id = request.args.get('id')
    new_user = User.query.get(id)
    return render_template('edit-user.html', new_user=new_user)


@app.route('/users/<id>/edit', methods=["POST"])
def edit(id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    newUser = User(id=id, first_name=first_name,
                   last_name=last_name, image_url=image_url)
    db.session.merge(newUser)
    db.session.commit()
    return redirect('/')


@app.route('/users/new')
def add_user():
    return render_template('add-user.html')


@app.route('/add-user', methods=["POST"])
def add_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    newUser = User(first_name=first_name,
                   last_name=last_name, image_url=image_url)
    db.session.add(newUser)
    db.session.commit()
    return redirect('/')

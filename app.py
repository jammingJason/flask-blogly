"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.route('/')
def go_home():
    """Shows list of all users in db"""
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
    if image_url != '':
        newUser = User(id=id, first_name=first_name,
                       last_name=last_name, image_url=image_url)
    else:
        newUser = User(id=id, first_name=first_name, last_name=last_name)
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
    if image_url != '':
        newUser = User(first_name=first_name,
                       last_name=last_name, image_url=image_url)
    else:
        newUser = User(first_name=first_name, last_name=last_name)
    db.session.add(newUser)
    db.session.commit()
    return redirect('/')


@app.route('/users/<id>/posts/new')
def add_post(id):
    """Show form to add a post for that user."""
    user = User.query.get(id)
    return render_template('new-post.html', user=user)


@app.route('/users/<id>/posts/new', methods=['POST'])
def add_new_post(id):
    """ Handle add form; add post and redirect to the user detail page."""

    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=id)
    db.session.add(new_post)
    db.session.commit()
    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/posts/<id>')
def show_post(id):
    """Show a post."""
    return redirect('/')

# Show buttons to edit and delete the post.


@app.route('/posts/<id>/edit')
def edit_post(id):
    """Show form to edit a post, and to cancel (back to user page)."""
    return redirect('/')


@app.route('/posts/<id>/edit', methods=['POST'])
def edit_existing_post(id):
    """Handle editing of a post. Redirect back to the post view."""
    return redirect('/')


@app.route('/posts/<id>/delete')
def delete_post(id):
    """Delete the post."""
    return redirect('/')

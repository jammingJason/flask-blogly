"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag


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
    content = request.form['content'].strip()
    new_post = Post(title=title, content=content, user_id=id)
    db.session.add(new_post)
    db.session.commit()
    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/posts/<id>')
def show_post(id):
    """Show a post."""
    post = Post.query.get(id)
    created = post.created_at

    return render_template('post.html', post=post, created=created.strftime("%c"))

# Show buttons to edit and delete the post.


@app.route('/posts/<id>/edit')
def edit_post(id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get(id)
    tags = Tag.query.all()
    posts_tags = PostTag.query.filter_by(post_id=id).all()
    return render_template('edit-post.html', post=post, tags=tags, posts_tags=posts_tags)


@app.route('/posts/<id>/edit', methods=['POST'])
def edit_existing_post(id):
    """Handle editing of a post. Redirect back to the post view."""

    title = request.form['title']
    content = request.form['content']

    post = Post(id=id, title=title, content=content)
    db.session.merge(post)
    db.session.commit()
    return redirect('/posts/'+id)


@app.route('/posts/<id>/delete')
def delete_post(id):
    """Delete the post."""

    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/tags/new')
def new_tag():
    posts = Post.query.all()
    return render_template('tag.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    posts = request.form['posts']
    for post in posts:
        pt = PostTag(post_id=post, tag_id=tag.id)
        db.session.add(pt)
        db.session.commit()
    return redirect('/tags')


@app.route('/tags')
def show_all_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('all-tags.html', tags=tags)


@app.route('/tags/<id>')
def get_tag(id):
    tag = Tag.query.get(id)
    posts_id = PostTag.query.filter_by(tag_id=id).all()
    posts = []
    for id in posts_id:
        posts = posts + Post.query.filter_by(id=id.post_id).all()
    return render_template('view-tag.html', tag=tag, posts=posts)


@app.route('/tags/<id>/edit')
def show_edit_tag(id):
    edit_tag = Tag.query.get(id)
    return render_template('edit-tag.html', tag=edit_tag)


@app.route('/tags/<id>/edit', methods=['POST'])
def edit_tag(id):
    name = request.form['name']
    edit_tag = Tag(id=id, name=name)
    db.session.merge(edit_tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<id>/delete', methods=['POST'])
def del_tag(id):

    PostTag.query.filter_by(tag_id=id).delete()
    Tag.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<t_id>/remove-from-post/<p_id>')
def remove_from_post(t_id, p_id):
    del_tag = PostTag.query.filter_by(
        post_id=p_id, tag_id=t_id).delete()
    del_tag
    db.session.commit()
    return "Removed"


@ app.route('/tags/<t_id>/add-to-post/<p_id>')
def add_to_post(t_id, p_id):
    pt = PostTag(post_id=p_id, tag_id=t_id)
    db.session.add(pt)
    db.session.commit()
    return "Added"

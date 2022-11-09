# import arithmetic
from unittest import TestCase
from app import app, db
from models import User, Post


class TestUsers(TestCase):

    """Examples of unit tests."""

    def setUp(self):
        """Add sample post."""

    def tearDown(self):
        """Clean up any fouled transaction."""
        # db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_new_user(self):

        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add User</h1>', html)

    def test_add_new_user(self):

        with app.test_client() as client:
            resp = client.post('/add-user',
                               data={'first_name': 'Jackson', 'last_name': 'Costner', 'image_url': 'https://www.picture.com'})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

    def test_delete_user(self):
        with app.test_client() as client:
            new_user = User(first_name='Billy', last_name='Goat',
                            image_url='https://www.picture.com')
            db.session.add(new_user)
            db.session.commit()

            resp = client.post('/users/'+str(new_user.id)+'/delete')
            # html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

    def test_delete_post(self):
        with app.test_client() as client:
            new_user = User(first_name='Van', last_name='Crews')
            db.session.add(new_user)
            db.session.commit()
            db.session.flush()
            new_post = Post(title='Testing Post',
                            content='testing content', user_id=new_user.id)
            db.session.add(new_post)
            db.session.commit()
            resp = client.get('/posts/'+str(new_post.id)+'/delete')
            # html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

    def test_edit_post(self):
        with app.test_client() as client:
            new_user = User(first_name='Van Jason', last_name='Crews')
            db.session.add(new_user)
            db.session.commit()
            db.session.flush()
            new_post = Post(title='Testing Post', user_id=new_user.id)
            db.session.add(new_post)
            db.session.commit()

            another_post = Post(id=new_post.id, title='Testing Post',
                                content='testing content', user_id=new_user.id)
            db.session.merge(another_post)
            resp = client.post('/posts/'+str(new_post.id) +
                               '/edit', data={'title': 'Testing Post', 'content': 'testing content'})

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertIn(str(another_post.id), html)

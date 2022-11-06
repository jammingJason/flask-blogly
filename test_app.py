# import arithmetic
from unittest import TestCase
from app import app, db
from models import User


class TestUsers(TestCase):

    # def setUp(self):
    #     """Stuff to do before every test."""

    # def tearDown(self):
    #     """Stuff to do after every test"""

    """Examples of unit tests."""

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

            # db.session.delete(new_user)
            # db.session.commit()
            resp = client.post('/users/'+str(new_user.id)+'/delete')
            # html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

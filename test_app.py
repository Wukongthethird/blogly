from unittest import TestCase
from app import app
from models import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class SampleAppTestCase(TestCase):
    """Test flask app of Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # testing for routing to root
            self.assertEqual(response.status_code, 302)


    def test_homepage_redirect(self):
        with self.client as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            # Testing template #
            self.assertEqual(response.status_code, 200)
            # self.assertIn('ming', html)
            self.assertIn('testing', html)


    def test_create_user(self):
        with self.client as client:
            response = client.post('/users/new', 
                                    data={'first_name': 'alextest', 'last_name': 'rutantest', 'image_url': None})
            html = response.get_data(as_text=True)

            new_user =  User(first_name='alextest', last_name='rutantest',image_url=None)
            db.session.add(new_user)
            db.session.commit()

            self.assertEqual(response.status_code, 302)
            self.assertIn('testing', html)

    def test_edit_user(self):
        with self.client as client:
            response = client.post('/users/3/edit', 
                                    data={'first_name': 'alextest', 'last_name': '', 'image_url': None})
            html = response.get_data(as_text=True)

            db.session.commit()

            self.assertEqual(response.status_code, 302)
            self.assertIn('testing', html)


    # MAKE A TEST THAT TESTS IF A 404 STATUS CODE is  AN ID THAT DOESNT EXIST IS PASSED IN 
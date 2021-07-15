from unittest import TestCase
from app import app
from models import User, db 
from sample_model import initial_information


app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()
db.create_all()


class SampleAppTestCase(TestCase):
    """Test flask app of Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        initial_information()
        self.user_id = User.query.get(1).id
        print( 'LOOK AT HERE' , self)

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    # def test_homepage(self):
    #     """Make sure information is in the session and HTML is displayed"""

    #     with self.client as client:
    #         response = client.get('/')

    #         # testing for routing to root
    #         self.assertEqual(response.status_code, 302)


    # def test_homepage_redirect(self):
    #     with self.client as client:
    #         response = client.get('/users')
    #         html = response.get_data(as_text=True)

    #         # Testing template #
    #         self.assertEqual(response.status_code, 200)
    #         # self.assertIn('ming', html)
    #         self.assertIn('testing', html)


    # def test_create_user(self):
    #     with self.client as client:
    #         response = client.post('/users/new', 
    #                                 data={'first_name': 'alextest', 'last_name': 'rutantest', 'image_url': 
    #                                 "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/440px-SpongeBob_SquarePants_character.svg.png"},follow_redirects=True)
    #         html = response.get_data(as_text=True)

    #         new_user =  User(first_name='alextest', last_name='rutantest',image_url=None)
    #         db.session.add(new_user)
    #         db.session.commit()

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('testing', html)


    def test_edit_user(self):
        with self.client as client:
            response = client.post(f'/users/{self.user_id}/edit', 
                                    data={'first_name': 'alextest', 'last_name': '', 'image_url': "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/440px-SpongeBob_SquarePants_character.svg.png"},follow_redirects=True)
            html = response.get_data(as_text=True)

            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIn('alextest', html)


    # MAKE A TEST THAT TESTS IF A 404 STATUS CODE is  AN ID THAT DOESNT EXIST IS PASSED IN 
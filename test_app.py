from unittest import TestCase
from app import app
from models import User, db 
from sample_model import initial_information, user_one


app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

# create a function to add users so you can show where the grab the info without query

class SampleAppTestCase(TestCase):
    """Test flask app of Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        User.query.delete()
        self.client = app.test_client()
        # test_users = initial_information()

        test_user1 = User(**user_one)

        db.session.add_all( [test_user1] )
        db.session.commit()

        # self.user_id = User.query.get(1).id
        self.test_user1 = test_user1


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # testing for routing to root
            self.assertEqual(response.status_code, 302)


    def test_homepage_redirect(self):
        with self.client as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            # Testing template #
            self.assertEqual(response.status_code, 200)
            # self.assertIn('ming', html)
            self.assertIn('users template', html)


    def test_create_user(self):
        with self.client as client:
            d = {'first_name': 'alextest', 'last_name': 'rutantest', 'image_url': 
                                    "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/440px-SpongeBob_SquarePants_character.svg.png"}
            response = client.post('/users/new', 
                                    data=d ,follow_redirects=True)
            html = response.get_data(as_text=True)

            # new_user =  User(first_name='alextest', last_name='rutantest',image_url=None)
            # db.session.add(new_user)
            # db.session.commit()

            self.assertEqual(response.status_code, 200)
            #explicit test name
            self.assertIn('testing', html)
            self.assertIn(f" {d['first_name']} {d['last_name']}", html)


    def test_edit_user(self):
        with self.client as client:
            d = {'first_name': 'alextest', 'last_name': '', 'image_url': "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/440px-SpongeBob_SquarePants_character.svg.png"}
            response = client.post(f'/users/{self.test_user1.id}/edit', 
                                    data=d,follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f" {d['first_name']} {d['last_name']}", html)

    # MAKE A TEST THAT TESTS IF A 404 STATUS CODE is  AN ID THAT DOESNT EXIST IS PASSED IN 
    def test_404(self):
        with self.client as client:
            response = client.get('/users/1000',
                                    follow_redirects=True)
            self.assertEqual(response.status_code, 404)

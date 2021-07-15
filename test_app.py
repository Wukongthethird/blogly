from unittest import TestCase
from app import app

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
            html = response.get_data(as_text=True)

            # testing for routing to root
            self.assertEqual(response.status_code, 200)

            # Testing template #
            self.assertIn('testing', html)

    # def test_new_user(self):
    #     """Test starting a new game."""

    #     with self.client as client:
    #         response = client.get('/api/new-game')

    #         #maybe to delete of them
    #         #implicitly testing if return is json

    #         #testing if we are getting a response
    #         assert any(response.get_json()) is not False

    #         #testing the response if it is a dictionary
    #         assert type(response.get_json()) is dict
            
    #         #testing if we are getting a list 
    #         assert type(response.get_json()["board"]) is list

    #         #testing if game id has been serialized
    #         assert type(response.get_json()["gameId"]) is str 
   
    # def test_score_word(self):
    #     """Test word score"""

    #     with self.client as client:

    #         game_id = client.post("/api/new-game").get_json()['gameId']
    #         game = games[game_id]

    #         game.board[0] = ["C", "A", "X", "X", "X"]
    #         game.board[1] = ["X", "T", "X", "X", "X"]
    #         game.board[2] = ["D", "O", "G", "X", "X"]
    #         game.board[3] = ["X", "X", "X", "X", "X"]
    #         game.board[4] = ["X", "X", "X", "X", "X"]

            
    #         response = self.client.post(
    #             "/api/score-word",
    #             json={"word": "CAT", "gameId": game_id})
    #         self.assertEqual(response.get_json(), {'result': 'ok'})

    #         response = self.client.post(
    #             "/api/score-word",
    #             json={"word": "DOG", "gameId": game_id})
    #         self.assertEqual(response.get_json(), {'result': 'ok'})

    #         response = self.client.post(
    #             "/api/score-word",
    #             json={"word": "XXX", "gameId": game_id})
    #         self.assertEqual(response.get_json(), {'result': 'not-word'})

    #         response = self.client.post(
    #             "/api/score-word",
    #             json={"word": "NOPE", "gameId": game_id})
    #         self.assertEqual(response.get_json(), {'result': 'not-on-board'})



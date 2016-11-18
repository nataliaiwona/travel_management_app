from unittest import TestCase
from server import app
from model import connect_to_db, db, User, Location, Pin
import helper


class FlaskTestsDatabase(TestCase):
    """Testing database."""

    def setUp(self):
        """Define instructions that will be executed before each test method."""

        # Get the Flask test client
        app.config['SECRET_KEY'] = 'MEMORY'
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
    #     connect_to_db(app, "postgresql:///travels")

    #     # Create tables and add sample data
    #     db.create_all()
    #     example_data()

    # def tearDown(self):
    #     db.session.close()
    #     db.drop_all()

#     def test_check_login(self):

#     def test_check_email(self):
    def test_signup_post_form(self):
        result = self.client.post('/signup',
                                  data={"fname": "Test", "lname": "Test",
                                        "email": "ok@ok.com", "password": "hi"},
                                  follow_redirects=True)
        self.assertIn('You are now logged in. Bon Voyage!', result.data)

    # def test_create_or_get_known_location(self):
    #     """ """

    #     result = create_or_get_location("San Francisco", "California", "United States", "37.773972", "-122.431297") 

    #     assert result.id = "3"

    # def test_create_or_get_location(self):
    #     """ """
        # query location of what you just added and test it




class AppIntegrationTestCase(TestCase):

    def setUp(self):
        """Define instructions that will be executed before each test method."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_landing_page(self):
        """Testing the index route."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<title>Travel Management Application</title>', result.data)

    def test_signup(self):
        """Testing signup route, GET method."""
        result = self.client.get('/signup')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Sign Up for an Account</h2>', result.data)

    def test_login(self):
        """Testing login route, GET method."""
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Login</h1>", result.data)

    # def test_homepage(self):
    #     """Testing the user homepage, GET method."""
    #     result = self.client.get('/user_homepage')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("<title>Search by City</title>", result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()

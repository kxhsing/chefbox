from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session

class FlaskTestBasic(TestCase):
    """Flask tests that don't require user to be logged in"""

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()

        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page"""
        result = self.client.get("/")
        self.assertIn("Log In", result.data)



class FlaskTestsLogInLogOut(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'karen@gmail.com', 'password': user.password.encode('utf8')},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], '1')
            self.assertIn("You are logged in", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('You are logged out.', result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()
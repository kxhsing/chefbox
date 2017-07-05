from unittest import TestCase
from model import User, connect_to_db, db, example_data
from server import app
from flask import session


class TestIndex(TestCase):
    """Flask tests that don't require user to be logged in"""

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page"""
        result = self.client.get("/")
        self.assertIn("Login", result.data)



class TestsLogInLogOut(TestCase):
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

        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'karen@gmail.com', 'password': 'cookies'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user_id'], user.user_id)
            self.assertIn("Hello", result.data)

    def test_logout(self):
        """Test logout route."""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('Login', result.data)


class TestUserIngredRecipeBoard(TestCase):
    """Test user Ingredient Inventory, Recipe Box, Chef Board."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_dashboard(self):
        """Test user's dashboard"""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()
        user_id = user.user_id
        firstname = user.firstname

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/users/'+str(user_id),
                            follow_redirects=True
                            )

            self.assertIn("Hello", result.data)
            self.assertIn(firstname, result.data)

    def test_unauthorized_user(self):
        """Test case of unathorized user trying to access dashboard"""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()
        user_id = user.user_id

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/users/'+str(2),
                            follow_redirects=True
                            )

            self.assertIn("You are not authorized to view this profile", result.data)


    def test_ingred(self):
        """Test user's Ingredient Inventory"""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()
        user_id = user.user_id
        firstname = user.firstname

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/ingred/'+str(user_id),
                            follow_redirects=True
                            )

            self.assertIn("Add Ingredient", result.data)


    def test_recipes(self):
        """Test user's Recipe Box"""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()
        user_id = user.user_id
        firstname = user.firstname

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/recipes/'+str(user_id),
                            follow_redirects=True
                            )

            self.assertIn("Mark completed recipes as \"Cooked\" to move them to your Chef Board", result.data)


    def test_recipes_no_recipes(self):
        """Test user's Chef Board"""
        user = db.session.query(User).filter(User.email=='jesse@gmail.com').one()
        user_id = user.user_id
        firstname = user.firstname

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/recipes/'+str(user_id),
                            follow_redirects=True
                            )

            self.assertIn("ChefBox - Recipe Box", result.data)
            self.assertIn("There are currently no recipes saved in your recipe box.", result.data)


    def test_recipes_with_recipes(self):
        """Test user's recipes with recipes in box"""
        user = db.session.query(User).filter(User.email=='karen@gmail.com').one()
        user_id = user.user_id
        firstname = user.firstname

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.user_id

            result = c.get('/recipes/'+str(user_id),
                            follow_redirects=True
                            )

            self.assertIn("Cooked", result.data)
            self.assertIn("If you are no longer interested in a recipe, you can \"Remove\" it from your Recipe Box.", result.data)





if __name__ == "__main__":
    import unittest

    unittest.main()
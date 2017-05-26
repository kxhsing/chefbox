from unittest import TestCase
import actions
from server import app
from flask import session
from model import User, Recipe, Ingredient, RecipeIngredient, UserIngredient, UserRecipe, Review, connect_to_db, db, example_data
from spoonacular import get_recipe_info


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
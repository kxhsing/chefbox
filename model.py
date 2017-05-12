"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of recipe finder app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    #Define association table relationships
    ingredients = db.relationship("Ingredient", secondary="user_ingredients",
                                    backref="users")
    recipes = db.relationship("Recipe", secondary="user_recipes",
                                    backref="users")


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id={} email={}>".format(self.user_id,
                                                   self.email)


class Ingredient(db.Model):
    """Ingredients used by any/all user(s) in app"""

    __tablename__ = "ingredients"

    ingred_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    ingred_name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Ingredient ingred_id={} ingred_name={}>".format(self.ingred_id,
                                                   self.ingred_name)


class Recipe(db.Model):
    """Recipes saved by users"""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=True)
    cooked = db.Column(db.Boolean)

    #Define association relationship with ingredient
    ingredients = db.relationship("Ingredient", secondary="recipe_ingredients", 
                                    backref="recipes")


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Recipe recipe_id={} title={}>".format(self.recipe_id,
                                                       self.title)


class RecipeIngredient(db.Model):
    """Ingredients for recipe"""

    __tablename__ = "recipe_ingredients"

    recipe_ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingred_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingred_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)


class UserIngredient(db.Model):
    """Ingredients for each user"""

    __tablename__ = "user_ingredients"

    user_ingred_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    ingred_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingred_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<UserIngredient user_ingred_id={} user_id={}>".format(self.user_ingred_id, 
                                                                        self.user_id)


class UserRecipe(db.Model):
    """Recipes for each user"""

    __tablename__ = "user_recipes"

    user_recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # #Establish relationships
    # user = db.relationship("User", backref=db.backref("user_recipes"))
    # recipe = db.relationship("Recipe", backref=db.backref("user_recipess"))


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<UserRecipe user_recipe_id={} user_id={} recipe={}>".format(
                                                                    self.user_recipe_id,
                                                                    self.user_id,
                                                                    self.recipe.title)


class Review(db.Model):
    """Reviews for recipes"""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer,
                db.ForeignKey('recipes.recipe_id'),
                nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    photo_url = db.Column(db.Text, nullable=True)
    review = db.Column(db.Text, nullable=True)

    #Establish relationships
    user = db.relationship("User", backref=db.backref("reviews"))
    recipe = db.relationship("Recipe", backref=db.backref("reviews"))


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Review review_id={} recipe_id={} user_id={}>".format(self.review_id,
                                                       self.recipe_id, self.user_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    
    print "Connected to DB."

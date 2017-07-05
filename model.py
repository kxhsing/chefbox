"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy
import bcrypt

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
    source_name = db.Column(db.String(100), nullable=True)
    url = db.Column(db.Text, nullable=True, unique=True)
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True, unique=True)

    #Define association relationship with ingredient
    ingredients = db.relationship("Ingredient", secondary="recipe_ingredients", 
                                    backref="recipes") #will only lead to name of ingreds
    ingredient_info = db.relationship("RecipeIngredient", backref="recipes") #not sure about this


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Recipe recipe_id={} title={}>".format(self.recipe_id,
                                                       self.title.encode('utf-8'))


class RecipeIngredient(db.Model):
    """Ingredients for recipe"""

    __tablename__ = "recipe_ingredients"

    recipe_ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    ingred_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingred_id'), nullable=False)
    ingred_info = db.Column(db.String(100)) # will include recipe ingredient name, amount, and unit


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<RecipeIngredient recipe_ingred_id={} ingred_id={} recipe_id={}>".format(
                                                                                self.recipe_ingredient_id, 
                                                                                self.ingred_id,
                                                                                self.recipe_id)


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
    cooked = db.Column(db.Boolean)


    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<UserRecipe user_recipe_id={} user_id={} recipe_id={}>".format(
                                                                    self.user_recipe_id,
                                                                    self.user_id,
                                                                    self.recipe_id)


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
# For testing

def example_data():
    """Create some sample data."""

    # Add sample users
    password='cookies' 
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    karen = User(firstname='Karen', lastname='Hsing', email='karen@gmail.com', password=hashed_pw)

    password='noodles' 
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    jesse = User(firstname='Jesse', lastname='Boeuf', email='jesse@gmail.com', password=hashed_pw)

    password='corolla' 
    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    cora = User(firstname='Cora', lastname='Car', email='cora@gmail.com', password=hashed_pw)


    thai_shrimp_pasta = Recipe(title="Thai Shrimp Pasta", 
                            source_name="Taste of Home", 
                            url="http://www.tasteofhome.com/Recipes/thai-shrimp-pasta", 
                            instructions='{"Soak noodles according to package directions. Meanwhile, in a large dry skillet over medium heat, toast curry powder until aromatic, about 1-2 minutes. Stir in the coconut milk, shrimp, salt and pepper. Bring to a boil. Reduce heat; simmer, uncovered, for 5-6 minutes or until shrimp turn pink.","Drain noodles; add to pan. Stir in cilantro; heat through.","Serve with lime wedges if desired."}',
                            image="https://spoonacular.com/recipeImages/Thai-Shrimp-Pasta-421073.jpg")

    db.session.add_all([karen, jesse, cora, thai_shrimp_pasta])
    db.session.flush()
    thai_shrimp_pasta_id = Recipe.query.filter(Recipe.url=="http://www.tasteofhome.com/Recipes/thai-shrimp-pasta").first().recipe_id
    karen_id = User.query.filter(User.email=='karen@gmail.com').first().user_id

    karen_thai_pasta = UserRecipe(recipe_id=thai_shrimp_pasta_id, user_id=karen_id, cooked=False)
    db.session.add(karen_thai_pasta)

    
    db.session.commit()



##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///recipes"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)

    print "Connected to DB."

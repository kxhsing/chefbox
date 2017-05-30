

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify, url_for)

from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
import json
import bcrypt
from model import User, Recipe, Ingredient, RecipeIngredient, UserIngredient, UserRecipe, Review, connect_to_db, db
from spoonacular import get_recipe_request, get_recipe_info
from actions import delete_ingredient, add_ingredient, delete_recipe, add_to_board, upload_photo, delete_photo, create_review, add_new_recipe


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "jd8gakhHdiemvkldov"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = "static/photos/"
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Homepage. Also houses the login form"""

    return render_template("homepage.html")


# Go to the register form page
@app.route('/register', methods=["GET"])
def register_form():
    """Registration for new user."""

    return render_template("register_form.html")


# After user registers
@app.route('/register', methods=["POST"])
def register_complete():
    """After user registers, adds to db and goes back to homepage."""
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email").lower()
    password = request.form.get("password")

    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    if not User.query.filter(User.email==email).all():
        new_user = User(firstname=firstname, 
                        lastname=lastname, 
                        email=email, 
                        password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()
        flash ("Registration successful! Login to start using the app.")
        return redirect("/")
    else:
        flash("User email already exists.")
        return redirect("/register")


@app.route('/login', methods=["POST"])
def login_check():
    """Check if email and password match to database"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not User.query.filter(User.email==email).all():
        flash("User does not exist. Please register an account and try again.")
        return redirect("/")
    else:
        user = User.query.filter(User.email==email).one()

        if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
            session['user_id'] = user.user_id 
            print session['user_id']
            flash("You are logged in")
            return redirect("/users/"+str(user.user_id))
        else:
            flash("Password is incorrect, please try again")
            return redirect("/")

    return redirect("/")


@app.route('/logout')
def logout():
    """Logs out user."""
    flash("You are logged out.")
    del session["user_id"]

    return redirect("/")


@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Show user's dashboard, which houses linkes to saved recipes and ingredients"""

    user_id_session = str(session.get("user_id"))

    if user_id != user_id_session:
        flash("You are not authorized to view this profile")
        return redirect("/")

    user = User.query.filter(User.user_id==user_id_session).one()

    return render_template("dashboard.html", user=user)


@app.route('/recipes/<user_id>')
def show_user_recipes(user_id):
    """Show user's saved recipes"""

    user_id_session = str(session.get("user_id"))

    if user_id != user_id_session:
        flash("You are not authorized to view this profile")
        return redirect("/")

    user = User.query.filter(User.user_id==user_id_session).one()

    #Creating list of recipes that have not been cooked before to display in Recipe Box for user
    recipes_to_cook = UserRecipe.query.filter(UserRecipe.user_id==user_id, UserRecipe.cooked==False).all() 
    recipes_list = []
    for recipe in recipes_to_cook:
        recipe_id = recipe.recipe_id
        recipe_to_cook = Recipe.query.filter(Recipe.recipe_id==recipe_id).one()
        recipes_list.append(recipe_to_cook)

    return render_template("user_recipes.html", user=user, recipes_list=recipes_list)


@app.route('/ingred/<user_id>')
def show_user_ingredients(user_id):
    """Show user's ingredients"""
    
    user_id_session = str(session.get("user_id"))

    if user_id != user_id_session:
        flash("You are not authorized to view this profile")
        return redirect("/")

    user = User.query.filter(User.user_id==user_id_session).one()

    return render_template("user_ingred.html", user=user)


@app.route('/board/<user_id>')
def show_user_board(user_id):
    """Show user's board of completed recipes"""
    
    user_id_session = str(session.get("user_id"))

    if user_id != user_id_session:
        flash("You are not authorized to view this profile")
        return redirect("/")

    user = User.query.filter(User.user_id==user_id_session).one()

    return render_template("user_board.html", user=user)


@app.route('/add_ingred', methods=["POST"])
def add_ingred():
    """Add ingredient to user's inventory and master inventory if not already
    in the database"""

    user_id = session.get("user_id")
    ingredient = request.form.get("ingredient").lower()
    result = add_ingredient(user_id, ingredient)

    return result


@app.route('/del_ingred', methods=['POST'])
def del_ingred():
    """Delete ingredient from user's ingredient inventory"""

    user_id = session.get("user_id")
    ingred_id = int(request.form.get("ingredient"))
    result = delete_ingredient(user_id, ingred_id)

    return result


@app.route('/search_recipe')
def search_recipe():
    """Search recipe page"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    #Spoonacular recipe search parameters
    cuisines = ["african", "chinese", "japanese", "korean", "vietnamese", "thai", "indian", "british", "irish", "french", "italian", "mexican", "spanish", "middle eastern", "jewish", "american", "cajun", "southern", "greek", "german", "nordic", "eastern european", "caribbean", "latin american"]
    diets = ["pescetarian", "lacto vegetarian", "ovo vegetarian", "vegan", "paleo", "primal", "vegetarian"]
    intolerances = ["dairy", "egg", "gluten", "peanut", "sesame", "seafood", "shellfish", "soy", "sulfite", "tree nut", "wheat"]

    return render_template("search_recipe.html", 
                            user=user, 
                            cuisines=cuisines, 
                            diets=diets, 
                            intolerances=intolerances)


@app.route('/request_recipe', methods=["POST"])
def request_recipe():
    """GET request for recipes"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    include_ingredients = request.form.getlist('search_ingredients')
    cuisines = request.form.getlist('cuisines')
    intolerances = request.form.getlist('intolerances')
    diet = request.form.get('diet')
    offset = 0

    #Save user's search parameters in session in case want to search more
    session['include_ingred'] = include_ingredients 
    session['cuisines'] = cuisines
    session['intolerances'] = intolerances
    session['diet'] = diet
    session['offset'] = offset

    result = get_recipe_request(include_ingredients, diet, cuisines, intolerances, offset)
    if result:
        recipe_results_list = result[1]
        total_results = result[0]
    else:
        recipe_results_list = []
        total_results = 0

    return render_template("recipe_results.html", user=user, recipe_results_list=recipe_results_list, total_results=total_results)


@app.route('/search_more', methods=["POST"])
def search_more():
    """If user wants more search results, request more from API"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    #Get number to offset in search results and increment session
    offset_increment = int(request.form.get("more_results"))

    offset = session.get("offset")
    offset += offset_increment
    session['offset'] = offset

    include_ingredients = session.get("include_ingred")
    diet = session.get("diet")
    cuisines = session.get("cuisines")
    intolerances = session.get("intolerances")


    result = get_recipe_request(include_ingredients, diet, cuisines, intolerances, offset)

    if result:
        recipe_results_list = result[1]
        total_results = result[0]
    else:
        recipe_results_list = []
        total_results = 0

    # return render_template("recipe_results.html", user=user, recipe_results_list=recipe_results_list, total_results=total_results)
    return jsonify({'recipe_results_list': recipe_results_list, 'total_results': total_results})


@app.route('/add_recipe', methods=["POST"])
def add_recipe():
    """Add recipe to user's recipe box"""

    user_id = session.get("user_id")
    recipe_id = request.form.get("recipe_id")
    result = add_new_recipe(user_id, recipe_id)

    return result


@app.route('/del_recipe', methods=['POST'])
def del_recipe():
    """Delete recipe from user's recipe box"""

    user_id = session.get("user_id")
    recipe_id = int(request.form.get("recipe_id"))
    result = delete_recipe(user_id, recipe_id)

    return result


@app.route('/review_recipe', methods=["POST"])
def review_recipe():
    user_id = session.get("user_id")
    recipe_id = request.form.get("recipe_id") 
    result = add_to_board(user_id, recipe_id)

    return result


photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    user_id = session.get("user_id")
    photo = request.files["photo"]
    recipe_id = request.form.get("recipe_id")

    try:    
        if request.method == "POST" and "photo" in request.files:
            filename = photos.save(photo)
    except:
        # flash("Not a valid photo file. Please try again.")
        return jsonify({})

    result = upload_photo(user_id, filename, recipe_id)

    return result


@app.route('/del_photo', methods=["POST"])
def del_photo():

    user_id = session.get("user_id")
    recipe_id = request.form.get("recipe_id") 
    result = delete_photo(user_id, recipe_id)

    return result


@app.route('/write_review', methods=["POST"])
def write_review():
    user_id = session.get("user_id")
    recipe_id = request.form.get("recipe_id")
    submitted_review = request.form.get("review")
    result = create_review(user_id, recipe_id, submitted_review)

    return result





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension

    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')

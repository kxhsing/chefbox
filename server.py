

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Recipe, Ingredient, RecipeIngredient, UserIngredient, UserRecipe, Review, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "secretsecretsecrets"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


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
    email = request.form.get("email")
    password = request.form.get("password")

    if not User.query.filter(User.email==email).all():
        new_user = User(firstname=firstname, 
                        lastname=lastname, 
                        email=email, 
                        password=password)

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
        if password==user.password:
            session['user_id'] = user.user_id 
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
def user_info(user_id):
    """Show user's dashboard, which houses linkes to saved recipes and ingredients"""

    user = User.query.filter(User.user_id==user_id).one()

    return render_template("dashboard.html", user=user)


@app.route('/recipes/<user_id>')
def user_recipes(user_id):
    """Show user's saved recipes"""
    pass


@app.route('/ingred/<user_id>')
def user_recipes(user_id):
    """Show user's ingredients"""
    pass


@app.route('/add_ingred')
def add_ingred():
    pass


@app.route('/search_recipe')
def search_recipe():
    pass


@app.route('/add_recipe')
def add_recipe():
    pass


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension

    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')



from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Recipe, Ingredient, RecipeIngredient, UserIngredient, UserRecipe, Review, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    # """Homepage."""

    # return render_template("homepage.html")
    pass


# Go to the register form page
@app.route('/register', methods=["GET"])
def register_form():
    # """Registration for new user."""

    # return render_template("register_form.html")
    pass


# After user registers
@app.route('/register', methods=["POST"])
def register_complete():
    """After user registers, adds to db and goes back to homepage."""
    # email = request.form.get("email")
    # password = request.form.get("password")

    # # import pdb; pdb.set_trace()

    # if not User.query.filter(User.email==email).all():
    #     new_user = User(email=email, password=password)

    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect("/")
    # else:
    #     flash("User email already exists.")
    #     return redirect("/register")
    pass


@app.route('/login', methods=["GET"])
def login_form():
    # """Direct users to login page"""

    # return render_template("login_form.html")
    pass


@app.route('/login', methods=["POST"])
def login_check():
    """Check if email and password match to database"""
    # email = request.form.get("email")
    # password = request.form.get("password")

    # if not User.query.filter(User.email==email).all():
    #     flash("User does not exist")
    #     return redirect("/login")
    # else:
    #     user = User.query.filter(User.email==email).one()
    #     if password==user.password:
    #         session['user_id'] = user.user_id 
    #         flash("You are logged in")
    #         return redirect("/users/"+str(user.user_id))
    #     else:
    #         flash("Password is incorrect, please try again")
    #         return redirect("/login")

    # # else:
    # #     if User.query.filter(User.email==email).one().password

    # return redirect("/")
    pass


@app.route('/logout')
def logout():
    # """Logs out user."""
    # flash("You are logged out.")
    # del session["user_id"]

    # return redirect("/")
    pass

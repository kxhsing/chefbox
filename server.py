

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Recipe, Ingredient, RecipeIngredient, UserIngredient, UserRecipe, Review, connect_to_db, db

import requests

import os

import json


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "secretsecretsecrets"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


#####SPOONACULAR ENDPOINTS - all GET requests
search_recipe_complex = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/searchComplex"
get_recipe_info = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information"
bulk_recipe_info = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/informationBulk"
auto_complete_ingred = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete"

YOURKEY = os.environ['YOURKEY']

headers={
    "X-Mashape-Key": YOURKEY,
    "Accept": "application/json"
  }


#####

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
def show_user_info(user_id):
    """Show user's dashboard, which houses linkes to saved recipes and ingredients"""

    user = User.query.filter(User.user_id==user_id).one()

    return render_template("dashboard.html", user=user)


@app.route('/recipes/<user_id>')
def show_user_recipes(user_id):
    """Show user's saved recipes"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    return render_template("user_recipes.html", user=user)


@app.route('/ingred/<user_id>')
def show_user_ingredients(user_id):
    """Show user's ingredients"""
    
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    return render_template("user_ingred.html", user=user)


@app.route('/add_ingred', methods=["POST"])
def add_ingred():
    """Add ingredient to user's inventory and master inventory if not already
    in the database"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()
    ingredient = request.form.get("ingredient").lower()

    #Check if ingredient is in master list is in user's inventory
    if Ingredient.query.filter(Ingredient.ingred_name==ingredient).all():
        ingredient_id = Ingredient.query.filter(Ingredient.ingred_name==ingredient).one().ingred_id
        if UserIngredient.query.filter(UserIngredient.user_id==user_id, UserIngredient.ingred_id==ingredient_id).all():
            flash(ingredient.title()+" already exists in your inventory.")
            return jsonify({})  
        else:
            new_user_ingred = UserIngredient(ingred_id=ingredient_id, user_id=user.user_id) 
            db.session.add(new_user_ingred)
            db.session.commit()
            ingred_id = str(new_ingred.ingred_id)
            print ingred_id
            flash ("Added to inventory: "+ingredient.title())
            return jsonify({'ingredient': ingredient, 'ingred_id':ingred_id})

        # return redirect("/ingred/"+str(user_id))
        # return flash ("Added to inventory: "+ingredient)

    #If ingredient not in master ingredient list, add to master ingredients
    #and also add to user's ingredient inventory
    else:
        new_ingred = Ingredient(ingred_name=ingredient)
        db.session.add(new_ingred)
        # db.session.commit()
        db.session.flush()
        new_user_ingred = UserIngredient(ingred_id=new_ingred.ingred_id, user_id=user.user_id)
        db.session.add(new_user_ingred)
        db.session.commit()
        ingred_id = str(new_ingred.ingred_id)
        print ingred_id
        flash ("Added to inventory: "+ingredient) 
        return jsonify({'ingredient': ingredient, 'ingred_id':ingred_id})

    # return redirect("/ingred/"+str(user_id))


@app.route('/del_ingred', methods=['POST'])
def delete_ingred():
    """Delete ingredient from user's ingredient inventory"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()
    ingred_id = int(request.form.get("ingredient"))
    ingred_to_del = UserIngredient.query.filter(UserIngredient.ingred_id==ingred_id, UserIngredient.user_id==user.user_id).one() 
    db.session.delete(ingred_to_del)
    db.session.commit()
    flash ("Ingredient removed.") 

    return redirect("/ingred/"+str(user_id))


@app.route('/search_recipe')
def search_recipe():
    """Search recipe page"""

    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    #Spoonacular recipe search parameters
    cuisines = ["african", "chinese", "japanese", "korean", "vietnamese", "thai", "indian", "british", "irish", "french", "italian", "mexican", "spanish", "middle eastern", "jewish", "american", "cajun", "southern", "greek", "german", "nordic", "eastern european", "caribbean", "latin american"]
    diets = ["pescetarian", "lacto vegetarian", "ovo vegetarian", "vegan", "paleo", "primal", "vegetarian"]
    intolerances = ["dairy", "egg", "gluten", "peanut", "sesame", "seafood", "shellfish", "soy", "sulfite", "tree nut", "wheat"]
    types = ["main course", "side dish", "dessert", "appetizer", "salad", "bread", "breakfast", "soup", "beverage", "sauce", "drink"] #not sure if going to keep this, seems to really limit search results

    return render_template("search_recipe.html", 
                            user=user, 
                            cuisines=cuisines, 
                            diets=diets, 
                            intolerances=intolerances, 
                            types=types)



def get_recipe_request(include_ingredients, diet, cuisines, intolerances, offset):
    """Make GET requests to API for recipe searches."""

    payload = {
            'addRecipeInformation': False, 
            'includeIngredients': include_ingredients,
            'instructionsRequired': True,
            'diet': diet,
            'cuisine': cuisines,
            'intolerances': intolerances,
            'ranking': 1,
            'offset': offset
        }

    recipes = requests.get(search_recipe_complex, headers=headers, params=payload)
    recipes = recipes.json()

    recipe_formatted = json.dumps(recipes, indent=4, sort_keys=True) #formatting the responses nicely in terminal
    print recipe_formatted #view formatted response in terminal

    recipe_results_list = [] #list of recipes to pass to recipe_results.html

    recipe_results = recipes['results'] 
    total_results = recipes['totalResults']
    if recipe_results: #checking if any results returned. 
        # print recipe_results

        recipe_ids = []

        for recipe in recipe_results: #fetch each recipe id, add to id list and run in "Get Bulk Recipe Info" endpoint
            recipe_id = str(recipe['id'])
            recipe_ids.append(recipe_id)

        recipe_ids_bulk = ','.join(recipe_ids)
        print recipe_ids_bulk

        bulk_recipe_results = requests.get(bulk_recipe_info, headers=headers, params={'ids': recipe_ids_bulk}) 
        bulk_recipe_results = bulk_recipe_results.json()

        # print bulk_recipe_results

        for recipe in bulk_recipe_results:
            recipe_id = recipe['id']
            recipe_title = recipe['title']
            recipe_source_name = recipe.get('sourceName')
            recipe_source_url = recipe.get('sourceUrl')
            recipe_img = recipe['image']

            steps = recipe['analyzedInstructions'][0]['steps']
            step_instructions = [] #create list for all instruction steps

            for step in steps:
                if len(step['step']) > 1:
                    step_instructions.append(step['step'])

            ingredients = recipe['extendedIngredients'] # list of dictionaries. each dict contains info about all ingredients, including 'name', 'amount', 'unit'

            ingredient_names_amt = []
            for ingredient in ingredients:
                ingredient_name = ingredient['name'].title()
                ingredient_amt = str(ingredient['amount'])+" "
                ingredient_unit = ingredient['unitShort'].lower()+" - "
                ingredient_final = ingredient_amt + ingredient_unit + ingredient_name
                ingredient_names_amt.append(ingredient_final)


            #master list of info with id, title, name, source, image, for each recipe
            recipe_info = [recipe_id, recipe_title, recipe_source_name, recipe_source_url, recipe_img, step_instructions, ingredient_names_amt]
            recipe_results_list.append(recipe_info)

        request_result = (total_results, recipe_results_list)

    return request_result    



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

    result = get_recipe_request(include_ingredients, cuisines, intolerances, diet, offset)

    recipe_results_list = result[1]
    total_results = result[0]

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


    result = get_recipe_request(include_ingredients, cuisines, intolerances, diet, offset)

    recipe_results_list = result[1]
    total_results = result[0]

    return render_template("recipe_results.html", user=user, recipe_results_list=recipe_results_list, total_results=total_results)


@app.route('/add_recipe', methods=["POST"])
def add_recipe():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()

    recipe_id = request.form.get('recipe_id')
    print recipe_id

    saved_recipe = requests.get(get_recipe_info.format(recipe_id), headers=headers)
    saved_recipe = saved_recipe.json() #dict
    print saved_recipe


    saved_recipe_title = saved_recipe['title'].encode('utf-8')
    saved_recipe_source_name = saved_recipe.get('sourceName')
    saved_recipe_source_url = saved_recipe.get('sourceUrl')


    steps = saved_recipe['analyzedInstructions'][0]['steps']
    step_instructions = [] #create list for all instruction steps

    for step in steps:
        if len(step['step']) > 1:
            step_instructions.append(step['step'])

    # print step_instructions

    if not Recipe.query.filter(Recipe.url==saved_recipe_source_url).all():
        #Create new recipe for database if does not exist already
        new_recipe = Recipe(title=saved_recipe_title, 
                            source_name=saved_recipe_source_name, 
                            url=saved_recipe_source_url, 
                            instructions=step_instructions)

        db.session.add(new_recipe)
        db.session.flush()

        new_recipe_id = new_recipe.recipe_id

        ingredients = saved_recipe['extendedIngredients'] # list of dictionaries. each dict contains info about all ingredients, including 'name', 'amount', 'unit'
        #Create Ingredient instances for ingredients that do not already exist in db
        for ingredient in ingredients:
            ingredient_name = ingredient['name']
            ingredient_amt = ingredient['amount']
            ingredient_unit = ingredient['unitShort']
            if not Ingredient.query.filter(Ingredient.ingred_name==ingredient_name).all(): #if ingredient not in db. add to it
                new_ingred = Ingredient(ingred_name=ingredient_name)
                db.session.add(new_ingred)
                db.session.flush()

            ingred_id = Ingredient.query.filter(Ingredient.ingred_name==ingredient_name).one().ingred_id

            #Create RecipeIngredient instances 
            ingred_info = str(ingredient_amt)+ " " + ingredient_unit.lower() + " - " + ingredient_name.title()

            new_recipe_ingred = RecipeIngredient(recipe_id=new_recipe_id, 
                                                ingred_id=ingred_id, 
                                                ingred_info=ingred_info)
            db.session.add(new_recipe_ingred)
            db.session.flush()


    existing_recipe_id = Recipe.query.filter(Recipe.url==saved_recipe_source_url).one().recipe_id

    if not UserRecipe.query.filter(UserRecipe.user_id==user_id, UserRecipe.recipe_id==existing_recipe_id).all():
        new_user_recipe = UserRecipe(recipe_id=existing_recipe_id, user_id=user_id, cooked=False)
        db.session.add(new_user_recipe)
        db.session.flush()

    db.session.commit()

    return redirect('/search_recipe')


@app.route('/review_recipe', methods=["POST"])
def review_recipe():
    user_id = session.get("user_id")
    user = User.query.filter(User.user_id==user_id).one()
    recipe_id = request.form.get("recipe_id") 
    cooked_recipe = UserRecipe.query.filter(UserRecipe.user_id==user_id, UserRecipe.recipe_id==recipe_id).one()
    cooked_recipe.cooked = True #does this need to be committed?

    new_review = Review(recipe_id=recipe_id, user_id=user_id)
    db.session.add(new_review)
    db.session.commit()


    return render_template("user_board.html", user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension

    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')

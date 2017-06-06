# <img src="/static/images/readme/homepage.png">

ChefBox is an all-in-one tool for aspiring chefs and home cooks to discover recipes, save memories of their culinary accomplishments, and reduce food waste. ChefBox searches for recipes based on users' available ingredients, personal preferences, and dietary restrictions. Registered users have personalized dashboards where they can add ingredients to their inventory, find new recipes that utilize their ingredients, access saved recipes from previous sessions, and upload photos and reviews of their completed dishes.

## Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [Installation](#install)
* [Future Features](#future)

## <a name="technologies"></a>Technologies

Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, JSON, Jinja2, HTML5, CSS, Bootstrap<br/>
API: Spoonacular API<br/>
Libraries: Flask Uploads, Bcrypt

## <a name="features"></a>Features

![alt tag](/static/images/readme/homepage.png)

Users register to use ChefBox with their email, and passwords are hashed before being stored in the PostgreSQL database.
Registered users have a personalized dashboard only they have access to once logged in.

![alt tag](/static/images/readme/dashboard.png)

Users can add ingredients they have in their kitchen pantry to their Ingredient Inventory, which will be appended to their ingredient list via AJAX post requests.

![alt tag](/static/images/readme/ingred.gif)

Users can search for recipes that maximize the use of the ingredients in their inventory, any keywords, preferred cuisines, dietary needs, and allergies to the search query.

![alt tag](/static/images/readme/search.gif)

When the search form is submitted, the app will start making calls to the Spoonacular API, and results will be rendered into recipe cards and displayed in a Masonry-like fashion for users to browse and save to their recipe box.

![alt tag]("/static/images/readme/results.png")

ChefBox allows users to infinitely scroll for more results using AJAX post requests, which will continuously make calls to the API when the bottom of the window is reached. Recipe results will be continously to the end of the page until a user decides they've found what they're looking for (or when they reach the end of the results). 

![alt tag]("/static/images/readme/results-scroll.gif")

When a user clicks on the "Save Recipe" button, an AJAX call posts the recipe info to the database under the user's recipes. The recipe card is then hidden and a confirmation message is displayed using jQuery.

All saved recipes are stored in the database which can be accessed by the user in later sessions.

![alt tag]("/static/images/readme/recipes.gif")

Once a recipe has been completed, the user can mark it as as "Cooked", which will move it to their Chef Board. 

![alt tag]("/static/images/readme/cooked.gif")

Using the Flask uploads library, ChefBox lets users upload photos and write reviews of completed recipes, all of which can be edited later should the user wish to.



## <a name="install"></a>Installation

To run ChefBox:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/kxhsing/chefbox.git
```

To have this app running on your local computer:
Create and activate a virtual environment inside your ChefBox directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [Spoonacular API](https://spoonacular.com/food-api).

Save your API key in a file called <kbd>secrets.sh</kbd> using this format:

```
export YOURKEY="YOURKEYHERE"
```

In the same file called <kbd>secrets.sh</kbd>, designate any secret key to use the Flask app:

```
export FLASK_SECRET_KEY="YOURKEYHERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Create database 'recipes'.
```
createdb recipes
```
Create your database tables
```
python model.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to start cooking with ChefBox.


## <a name="future"></a>Future Features
* Autocomplete ingredient search feature
* Feature to generate shareable links of completed recipes (including photos and reviews)
* Import saved recipe pins from a user's Pinterest account

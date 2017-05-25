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


def add_ingredient(user_id, ingredient):

    
    user = User.query.filter(User.user_id==user_id).one()
    #Check if ingredient is in master list and then if it is in user's inventory
    if Ingredient.query.filter(Ingredient.ingred_name==ingredient).all():
        ingredient_id = Ingredient.query.filter(Ingredient.ingred_name==ingredient).one().ingred_id
        if UserIngredient.query.filter(UserIngredient.user_id==user_id, UserIngredient.ingred_id==ingredient_id).all():
            return jsonify({})  
        else:
            new_user_ingred = UserIngredient(ingred_id=ingredient_id, user_id=user.user_id) 
            db.session.add(new_user_ingred)
            db.session.commit()
            ingred_id = str(new_user_ingred.ingred_id)
            print ingred_id
            return jsonify({'ingredient': ingredient, 'ingred_id':ingred_id})

    #If ingredient not in master ingredient list, add to master ingredients
    #and also add to user's ingredient inventory
    else:
        new_ingred = Ingredient(ingred_name=ingredient)
        db.session.add(new_ingred)
        db.session.flush()
        new_user_ingred = UserIngredient(ingred_id=new_ingred.ingred_id, user_id=user.user_id)
        db.session.add(new_user_ingred)
        db.session.commit()
        ingred_id = str(new_ingred.ingred_id)
        print ingred_id
        # flash ("Added to inventory: "+ingredient.title()) 
        return jsonify({'ingredient': ingredient, 'ingred_id':ingred_id})


def delete_ingredient(user_id, ingred_id):
    """Query for ingredient in user's ingredients and delete"""

    user = User.query.filter(User.user_id==user_id).one()
    ingred_to_del = UserIngredient.query.filter(UserIngredient.ingred_id==ingred_id, UserIngredient.user_id==user.user_id).one() 
    db.session.delete(ingred_to_del)
    db.session.commit()

    return jsonify({})




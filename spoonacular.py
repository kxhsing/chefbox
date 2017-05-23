import requests

import os

import json

#####SPOONACULAR ENDPOINTS - all GET requests
search_recipe_complex = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/searchComplex"
get_recipe_info_endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information"
bulk_recipe_info = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/informationBulk"
auto_complete_ingred = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete"

YOURKEY = os.environ['YOURKEY']

headers={
    "X-Mashape-Key": YOURKEY,
    "Accept": "application/json"
  }


def get_recipe_api(include_ingredients, diet, cuisines, intolerances, offset):
    """Make GET request to API for recipe searches"""
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

    print payload

    recipes = requests.get(search_recipe_complex, headers=headers, params=payload)

    if recipes.status_code != requests.codes.ok: #need 504 error to happen to confirm if this works
        return None

    return recipes


def get_detailed_recipe_info(recipe_ids_bulk):
    """Feed recipe results ids into bulk_recipe_info API endpoint"""
    bulk_recipe_results = requests.get(bulk_recipe_info, headers=headers, params={'ids': recipe_ids_bulk})

    return bulk_recipe_results


def process_bulk_recipes(bulk_recipe_results):
    """Take bulk recipe results and extract needed info about each recipe"""
    recipe_results_list = []
    for recipe in bulk_recipe_results:
            recipe_id = recipe['id']
            recipe_title = recipe['title']
            recipe_source_name = recipe.get('sourceName')
            recipe_source_url = recipe.get('sourceUrl')
            recipe_img = recipe['image']

            steps = recipe['analyzedInstructions'][0]['steps']
            step_instructions = [] #create list for all instruction steps

            for step in steps:
                if len(step['step']) > 2:
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

    return recipe_results_list


def get_recipe_request(include_ingredients, diet, cuisines, intolerances, offset):
    """Make recipe search request, get detailed recipe info for each and display results"""

    recipes = get_recipe_api(include_ingredients, diet, cuisines, intolerances, offset)

    # if recipes.status_code != requests.codes.ok: #need 504 error to happen to confirm if this works
    #     return None

    recipes = recipes.json()

    recipe_formatted = json.dumps(recipes, indent=4, sort_keys=True) #formatting the responses nicely in terminal
    print recipe_formatted #view formatted response in terminal

    recipe_results_list = [] #list of recipes to pass to recipe_results.html

    recipe_results = recipes['results'] 
    total_results = recipes['totalResults']

    if recipe_results: #checking if any results returned. 
        # print recipe_results

        recipe_ids = [str(recipe['id']) for recipe in recipe_results] #fetch each recipe id, add to id list and run in "Get Bulk Recipe Info" endpoint

        recipe_ids_bulk = ','.join(recipe_ids)
        # print recipe_ids_bulk

        bulk_recipe_results = get_detailed_recipe_info(recipe_ids_bulk)
        bulk_recipe_results = bulk_recipe_results.json()

        # print bulk_recipe_results

        recipe_results_list = process_bulk_recipes(bulk_recipe_results)
        request_result = (total_results, recipe_results_list)
        return request_result
    else:
        return None


def get_recipe_info(recipe_id):
    """Make GET requests to API for recipe searches."""
    
    saved_recipe = requests.get(get_recipe_info_endpoint.format(recipe_id), headers=headers)
    saved_recipe = saved_recipe.json() #dict

    return saved_recipe




if __name__ == "__main__":
    print
    import doctest
    if doctest.testmod().failed == 0:
        print "*** ALL TESTS PASSED ***"
    print


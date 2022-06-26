from welsh_app import app, db

from welsh_app.models import Ingredient, Recipe, User
from welsh_app.schema import ingredient_schema, ingredients_schema, recipe_schema, recipes_schema, user_schema

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import datetime

"""
===========================
endpoints
===========================
"""
# endpoint CREATE ingredient
@app.route("/ingredients", methods=["POST"])
@jwt_required()
def create_ingredient():
    try:
        name = request.json['name']
        new_obj = Ingredient(name)

        db.session.add(new_obj)
        db.session.commit()

        result = ingredient_schema.dump(new_obj)

        data = {
            'message': 'New Ingredient Created!',
            'status': 201,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


@app.route("/ingredients", methods=["GET"])
@jwt_required()
def get_ingredients():
    try:
        all_objects = Ingredient.query.all()
        result = ingredients_schema.dump(all_objects)

        data = {
            'message': 'All Ingredients!',
            'status': 200,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


# endpoint CREATE recipe
@app.route("/recipes", methods=["POST"])
@jwt_required()
def create_recipe():
    try:
        name = request.json['name']
        ingredient_ids = request.json['ingredients']
        new_obj = Recipe(name)
        for ingredient_id in ingredient_ids:
            ingredient = Ingredient.query.get(ingredient_id)
            if ingredient:
                new_obj.ingredients.append(ingredient)

        db.session.add(new_obj)
        db.session.commit()

        result = recipe_schema.dump(new_obj)

        data = {
            'message': 'New Recipe Created!',
            'status': 201,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


@app.route("/recipes", methods=["GET"])
@jwt_required()
def get_recipes():
    try:
        all_objects = Recipe.query.all()
        result = recipes_schema.dump(all_objects)

        data = {
            'message': 'All recipes!',
            'status': 200,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


# endpoint tp LOGIN user
@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        authorized = user.check_password(password)
        if not authorized:
            return {'message': 'Email or password invalid',
                    'status': 401,
                    'data': None}
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        data = {
            'message': 'Logged in successfully',
            'status': 200,
            'data': {'token': access_token}
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return data



# endpoint to CREATE user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        username = request.json['username']
        password = request.json['password']
        new_obj = User(username, password)
        new_obj.hash_password()
        db.session.add(new_obj)
        db.session.commit()
        result = user_schema.dump(new_obj)
        data = {
            'message': 'New User Created!',
            'status': 201,
            'data': result
        }
    except Exception as e:

        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


@app.route("/users", methods=["GET"]) # get user with his favorites recipes
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        result = user_schema.dump(user)

        data = {
            'message': 'User with favorite_recipes fetched!',
            'status': 200,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


@app.route("/users", methods=["PATCH"])
@jwt_required()
def flag_unflag_recipe():
    try:
        recipe_id = request.json['recipe_id']
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        recipe = Recipe.query.get(recipe_id)
        result = None
        if recipe:
            if recipe not in user.favorite_recipes:
                user.favorite_recipes.append(recipe)
                message = "Recipe flagged successfully!"
            else:
                user.favorite_recipes.remove(recipe)
                message = "Recipe was unflagged successfully!"

            db.session.commit()
            result = user_schema.dump(user)
            status = 204
        else:
            message = "Recipe with id = %s does not exist" % recipe_id
            status = 404

        data = {
            'message': message,
            'status': status,
            'data': result
        }
    except Exception as e:
        data = {
            'message': "Error: %s" % str(e),
            'status': 400,
            'data': None
        }
    return make_response(jsonify(data))


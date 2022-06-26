from welsh_app import app

from welsh_app.models import Ingredient, Recipe, User
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

"""
=============
schema classes
=============
"""
class IngredientSchema(ma.Schema):
    class Meta:
        model = Ingredient
        fields = ('id', 'name') # fields to expose


ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


class RecipeSchema(ma.Schema):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients') # fields to expose

    ingredients = ma.Nested(IngredientSchema, many=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'favorite_recipes') # fields to expose

    favorite_recipes = ma.Nested(RecipeSchema, many=True)


user_schema = UserSchema()
#users_schema = UserSchema(many=True)

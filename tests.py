import random

import pytest
import secrets
from welsh_app import app, db

ingredients = []
recipes = []
favorite_recipes = []


class WelshTester:
    token = None

    def __init__(self):
        self.username = "username_test678"
        self.password = "password987"
        app.secret_key = secrets.token_hex(16)
        with app.test_client() as client:
            self.client = client

    def create_user(self):
        response = self.client.post("/users", json={
            "username": self.username,
            "password": self.password
        })
        return response.json

    def login(self):
        response = self.client.post("/login", json={
            "username": self.username,
            "password": self.password
        })
        self.token = response.json['data']['token']
        return response.json

    def create_ingredient(self):
        response = self.client.post("/ingredients", json={
            "name": "Test ingredient %d" % len(ingredients)
        }, headers={
            "Authorization": "Bearer %s" % self.token
        })
        print(response.json["data"])
        ingredients.append(response.json["data"]["id"])
        return response.json

    def create_recipe(self):
        response = self.client.post("/recipes", json={
            "name": "Test recipe %d" % len(recipes),
            "ingredients": random.sample(ingredients, 3) # get 3 ingredients randomly
        }, headers={
            "Authorization": "Bearer %s" % self.token
        })
        recipes.append(response.json["data"]["id"])
        print(response.json["data"])
        return response.json

    def update_user_recipes(self, recipe_id):
        response = self.client.patch("/users", json={
            "recipe_id": recipe_id
        }, headers={
            "Authorization": "Bearer %s" % self.token
        })
        return response.json

    def flag_recipe(self, recipe_id):
        result = self.update_user_recipes(recipe_id)
        favorite_recipes.extend(result["data"]["favorite_recipes"])
        return result

    def unflag_recipe(self, recipe_id):
        result = self.update_user_recipes(recipe_id)
        return result

    def get_user(self):
        response = self.client.get("/users", headers={
            "Authorization": "Bearer %s" % self.token
        })
        return response.json

    def ingredients(self):
        response = self.client.get("/ingredients", headers={
            "Authorization": "Bearer %s" % self.token
        })
        return response.json

    def get_recipes(self):
        response = self.client.get("/recipes", headers={
            "Authorization": "Bearer %s" % self.token
        })
        return response.json


@pytest.fixture(scope='module')
def client():
    db.create_all()
    yield WelshTester()
    db.drop_all()


def test_create_user(client):
    assert client.create_user()["status"] == 201


def test_login(client):
    assert client.login()["status"] == 200


def test_create_ingredients(client):
    for i in range(30):
        assert client.create_ingredient()["status"] == 201


def get_ingredients(client):
    assert client.get_ingredients()["status"] == 200


def test_create_recipes(client):
    for i in range(30):
        assert client.create_recipe()["status"] == 201


def get_recipes(client):
    assert client.get_recipes()["status"] == 200


def test_flag_recipes(client):
    for recipe_id in random.sample(recipes, 10):
        assert client.flag_recipe(recipe_id)["status"] == 204


def test_unflag_recipes(client):
    recipes_to_unflag = random.sample(favorite_recipes, 2)
    for recipe in recipes_to_unflag:
        assert client.unflag_recipe(recipe["id"])["status"] == 204


def test_get_user(client):
    assert client.get_user()["status"] == 200


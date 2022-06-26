from welsh_app import app, db

from flask_bcrypt import generate_password_hash, check_password_hash



"""
=============
model classes
=============
"""
ingredient_identifier = db.Table('ingredient_identifier', db.Model.metadata,
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
)

favorite_recipes_identifier = db.Table('favorite_recipes_identifier', db.Model.metadata,
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


# See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
# for details on the column types.
class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.relationship("Ingredient", secondary=ingredient_identifier)

    def __init__(self, name):
        self.name = name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    favorite_recipes = db.relationship("Recipe", secondary=favorite_recipes_identifier)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

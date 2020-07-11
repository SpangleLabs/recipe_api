import flask
from flask import Flask

from data import NewRecipe, Ingredient
from database import Database

app = Flask(__name__)
db = Database()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/recipes")
def list_recipes():
    return flask.jsonify([r.to_json() for r in db.list_recipes()])


@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = flask.request.get_json()
    ingredients = []
    for ingredient in data["ingredients"]:
        ingredients.append(Ingredient(
            ingredient["amount"],
            ingredient["item"]
        ))
    new_recipe = NewRecipe(
        data["name"],
        data["ingredients"],
        data["recipe"]
    )
    recipe = db.save_recipe(new_recipe)
    return flask.jsonify(recipe.to_json())


@app.route("/recipes/<recipe_id>")
def show_recipe(recipe_id):
    recipe = db.get_recipe_by_id(recipe_id)
    if recipe is None:
        flask.abort(404)
        return None
    return flask.jsonify(recipe.to_json())


@app.route("/schedule")
def show_schedule():
    return {}


@app.route("/history")
def show_history():
    return {}


if __name__ == '__main__':
    app.run()

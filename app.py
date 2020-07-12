import flask

from data import NewRecipe, Ingredient
from database import Database
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

DATABASE = '/path/to/database.db'


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return "Hello World, let's cook!"


@app.route("/recipes")
def list_recipes():
    return flask.jsonify([r.to_json() for r in get_db().list_recipes()])


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
        ingredients,
        data["prep"],
        data["recipe"]
    )
    recipe = get_db().save_recipe(new_recipe)
    return flask.jsonify(recipe.to_json())


@app.route("/recipes/<recipe_id>")
def show_recipe(recipe_id):
    recipe = get_db().get_recipe_by_id(recipe_id)
    if recipe is None:
        flask.abort(404)
        return None
    return flask.jsonify(recipe.to_json())


@app.route("/schedule")
def show_schedule():
    entries = get_db().list_schedule()
    return flask.jsonify(
        {
            entry.date: entry.to_json() for entry in entries
        }
    )


@app.route("/history")
def show_history():
    entries = get_db().list_history()
    return flask.jsonify(
        {
            entry.date: entry.to_json() for entry in entries
        }
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5647)

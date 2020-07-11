import flask
from flask import Flask

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
    return "Not yet implemented"


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

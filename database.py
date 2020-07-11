import sqlite3
from typing import List, Optional

import dateutil.parser

from data import Ingredient, FullRecipe, ScheduleEntryForRecipe, HistoryEntryForRecipe, NewRecipe, ScheduleEntry, \
    RecipeEntry, HistoryEntry


class Database:
    DB_FILE = "recipes.sqlite"

    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self._create_db()

    def _create_db(self) -> None:
        cur = self.conn.cursor()
        with open("database_schema.sql", "r") as f:
            cur.executescript(f.read())
        self.conn.commit()

    def close(self):
        self.conn.close()

    def list_recipes(self) -> List[FullRecipe]:
        cur = self.conn.cursor()
        recipes = []
        for row in cur.execute("SELECT recipe_id, name, recipe FROM recipes"):
            ingredients = self.list_ingredients_for_recipe(row.recipe_id)
            history = self.list_history_for_recipe(row.recipe_id)
            schedule = self.list_schedule_for_recipe(row.recipe_id)
            recipes.append(FullRecipe(row.recipe_id, row.name, ingredients, row.recipe, history, schedule))
        return recipes

    def list_ingredients_for_recipe(self, recipe_id: int) -> List[Ingredient]:
        cur = self.conn.cursor()
        ingredients = []
        for ingredient in cur.execute("SELECT amount, item FROM ingredients WHERE recipe_id = ?", (recipe_id,)):
            ingredients.append(Ingredient(ingredient.amount, ingredient.item))
        return ingredients

    def list_schedule_for_recipe(self, recipe_id: int) -> List[ScheduleEntryForRecipe]:
        cur = self.conn.cursor()
        schedule = []
        for entry in cur.execute("SELECT date FROM schedule WHERE recipe_id = ?", (recipe_id,)):
            schedule.append(ScheduleEntryForRecipe(dateutil.parser.parse(entry.date)))
        return schedule

    def list_history_for_recipe(self, recipe_id: int) -> List[HistoryEntryForRecipe]:
        cur = self.conn.cursor()
        history = []
        for entry in cur.execute("SELECT date, start_time, end_time FROM history WHERE recipe_id = ?", (recipe_id,)):
            history.append(HistoryEntryForRecipe(
                dateutil.parser.parse(entry.date),
                dateutil.parser.parse(entry.start_time) if entry.start_time is not None else None,
                dateutil.parser.parse(entry.end_time) if entry.end_time is not None else None
            ))
        return history

    def get_recipe_by_id(self, recipe_id: int) -> Optional[FullRecipe]:
        cur = self.conn.cursor()
        cur.execute("SELECT recipe_id, name, recipe FROM recipes WHERE recipe_id = ?", (recipe_id,))
        row = cur.fetchone()
        if row is None:
            return None
        ingredients = self.list_ingredients_for_recipe(row.recipe_id)
        history = self.list_history_for_recipe(row.recipe_id)
        schedule = self.list_schedule_for_recipe(row.recipe_id)
        return FullRecipe(row.recipe_id, row.name, ingredients, row.recipe, history, schedule)

    def get_recipe_entry_by_id(self, recipe_id: int) -> Optional[RecipeEntry]:
        cur = self.conn.cursor()
        cur.execute("SELECT recipe_id, name, recipe FROM recipes WHERE recipe_id = ?", (recipe_id,))
        row = cur.fetchone()
        if row is None:
            return None
        ingredients = self.list_ingredients_for_recipe(row.recipe_id)
        return RecipeEntry(row.recipe_id, row.name, ingredients, row.recipe)

    def save_recipe(self, recipe: NewRecipe) -> FullRecipe:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO recipes (name, recipe) VALUES (?, ?)", (recipe.name, recipe.recipe))
        recipe_id = cur.lastrowid
        for ingredient in recipe.ingredients:
            cur.execute(
                "INSERT INTO ingredients (recipe_id, amount, item) VALUES (?, ?, ?)",
                (recipe_id, ingredient.amount, ingredient.item)
            )
        return self.get_recipe_by_id(recipe_id)

    def list_schedule(self) -> List[ScheduleEntry]:
        cur = self.conn.cursor()
        schedule = []
        for row in cur.execute("SELECT recipe_id, date FROM schedule"):
            recipe = self.get_recipe_entry_by_id(row.recipe_id)
            schedule.append(ScheduleEntry(
                dateutil.parser.parse(row.date),
                recipe
            ))
        return schedule

    def list_history(self) -> List[HistoryEntry]:
        cur = self.conn.cursor()
        history = []
        for row in cur.execute("SELECT recipe_id, date, start_time, end_time FROM history"):
            recipe = self.get_recipe_entry_by_id(row.recipe_id)
            history.append(HistoryEntry(
                dateutil.parser.parse(row.date),
                dateutil.parser.parse(row.start_time) if row.start_time is not None else None,
                dateutil.parser.parse(row.end_time) if row.end_time is not None else None,
                recipe
            ))
        return history

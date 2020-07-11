import datetime
from typing import Optional, List


class FullRecipe:
    def __init__(
            self,
            recipe_id: int,
            name: str,
            ingredients: List['Ingredient'],
            recipe: str,
            history: List['HistoryEntryForRecipe'],
            schedule: List['ScheduleEntryForRecipe']
    ):
        super().__init__(name, ingredients, recipe)
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients
        self.recipe = recipe
        self.history = history
        self.schedule = schedule

    def to_json(self):
        return {
            "recipe_id": self.recipe_id,
            "name": self.name,
            "ingredients": [i.to_json() for i in self.ingredients],
            "recipe": self.recipe,
            "history": [h.to_json() for h in self.history],
            "schedule": [s.to_json() for s in self.schedule]
        }


class Ingredient:
    def __init__(self, amount: str, item: str):
        self.amount = amount
        self.item = item

    def to_json(self):
        return {
            "amount": self.amount,
            "item": self.item
        }


class HistoryEntryForRecipe:
    def __init__(
            self,
            date: datetime.date,
            start_time: Optional[datetime.datetime],
            end_time: Optional[datetime.datetime]
    ):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def to_json(self):
        return {
            "date": self.date.isoformat(),
            "start_time": self.start_time.isoformat() if self.start_time is not None else None,
            "end_time": self.end_time.isoformat() if self.end_time is not None else None
        }


class ScheduleEntryForRecipe:
    def __init__(self, date: datetime.date):
        self.date = date

    def to_json(self):
        return {
            "date": self.date.isoformat()
        }

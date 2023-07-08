from typing import List

from common.errors.NotFound import NotFoundError
from common.errors.Conflict import ConflictError
from dishes.DishesService import DishesService
from dishes.models.Dish import Dish
from .models.Meal import Meal
from .models.CreateMealDto import CreateMealDto
from .models.UpdateMealDto import UpdateMealDto
from .errors.NonExistingDishInMeal import NonExistingDishInMeal

fake_db = []


class MealsService:
    def get_meals() -> List[Meal]:
        return sorted(fake_db, key=lambda x: x.ID)

    def get_meal_by_id(id: int) -> Meal:
        try:
            return next(x for x in fake_db if x.ID == id)
        except StopIteration:
            raise NotFoundError

    def get_meal_by_name(name: str) -> Meal:
        try:
            return next(x for x in fake_db if x.name == name)
        except StopIteration:
            raise NotFoundError

    def delete_meal_by_id(id: int) -> Meal:
        dish_to_remove = MealsService.get_meal_by_id(id)
        fake_db.remove(dish_to_remove)
        return dish_to_remove.ID

    def delete_meal_by_name(name: str) -> Meal:
        dish_to_remove = MealsService.get_meal_by_name(name)
        fake_db.remove(dish_to_remove)
        return dish_to_remove.ID

    def create_meal(data: CreateMealDto) -> int:
        if data.name in [x.name for x in fake_db]:
            raise ConflictError

        new_meal_id = max([x.ID for x in fake_db]) + 1 if len(fake_db) > 0 else 1
        new_meal = MealsService._generate_meal(new_meal_id, data)

        fake_db.append(new_meal)
        return new_meal_id

    def update_meal(id: int, data: UpdateMealDto) -> int:
        updated_meal = MealsService._generate_meal(id, data)
        MealsService.delete_meal_by_id(id)
        fake_db.append(updated_meal)
        return id

    def notify_deleted_dish(dish: Dish):
        for meal in fake_db:
            MealsService._try_remove_dish_from_meal_by_key(meal, dish, "appetizer")
            MealsService._try_remove_dish_from_meal_by_key(meal, dish, "main")
            MealsService._try_remove_dish_from_meal_by_key(meal, dish, "dessert")

    def _generate_meal(id: int, data: CreateMealDto | UpdateMealDto) -> Meal:
        try:
            appetizer = DishesService.get_dish_by_id(data.appetizer)
            main = DishesService.get_dish_by_id(data.main)
            dessert = DishesService.get_dish_by_id(data.dessert)
        except NotFoundError:
            raise NonExistingDishInMeal

        all_dishes = [appetizer, main, dessert]
        new_meal = Meal(
            ID=id,
            name=data.name,
            appetizer=data.appetizer,
            main=data.main,
            dessert=data.dessert,
            cal=MealsService._reduce_dishes_info(all_dishes, "cal"),
            sodium=MealsService._reduce_dishes_info(all_dishes, "sodium"),
            sugar=MealsService._reduce_dishes_info(all_dishes, "sugar"),
        )
        return new_meal

    def _reduce_dishes_info(l: List[Dish], key: str) -> int | float:
        return sum([x.dict()[key] for x in l])

    def _try_remove_dish_from_meal_by_key(meal: Meal, dish: Dish, key: str):
        if meal.dict()[key] == dish.ID:
            setattr(meal, key, None)
            meal.cal -= dish.cal
            meal.sodium -= dish.sodium
            meal.sugar -= dish.sugar

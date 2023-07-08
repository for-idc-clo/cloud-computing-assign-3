from typing import List

from common.errors.NotFound import NotFoundError
from common.errors.Conflict import ConflictError
from .models.Dish import Dish
from .models.CreateDishDto import CreateDishDto
from .errors.NoNutritionInfoFound import NoNutritionInfoFound
from .errors.NutritionEnricherError import NutritionEnricherError


from .NutritionEnricherService import NutritionEnricherService

fake_db = []


class DishesService():

    def get_dishes() -> List[Dish]:
        return sorted(fake_db, key=lambda x: x.ID)

    def get_dish_by_id(id: int) -> Dish:
        try:
            return next(x for x in fake_db if x.ID == id)
        except StopIteration:
            raise NotFoundError

    def get_dish_by_name(name: str) -> Dish:
        try:
            return next(x for x in fake_db if x.name == name)
        except StopIteration:
            raise NotFoundError

    def delete_dish_by_id(id: int) -> Dish:
        dish_to_remove = DishesService.get_dish_by_id(id)
        fake_db.remove(dish_to_remove)
        return dish_to_remove

    def delete_dish_by_name(name: str) -> Dish:
        dish_to_remove = DishesService.get_dish_by_name(name)
        fake_db.remove(dish_to_remove)
        return dish_to_remove

    def submit_dish(data: CreateDishDto) -> int:
        if (data.name in [x.name for x in fake_db]):
            raise ConflictError

        try:
            nutrition_info = NutritionEnricherService.get_nutrition_info_sum_for_dish(
                data.name)
        except NotFoundError:
            raise NoNutritionInfoFound
        except Exception as e:
            raise NutritionEnricherError

        new_dish_id = max([x.ID for x in fake_db]) + \
            1 if len(fake_db) > 0 else 1
        new_dish = Dish(ID=new_dish_id, name=data.name, cal=nutrition_info.calories,
                        size=nutrition_info.serving_size_g, sodium=nutrition_info.sodium_mg, sugar=nutrition_info.sugar_g)
        fake_db.append(new_dish)
        return new_dish_id

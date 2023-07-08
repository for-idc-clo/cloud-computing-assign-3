import requests
from common.errors.NotFound import NotFoundError
from .models.NutritionInfo import NutritionInfo
from .models.NutritionInfoSum import NutritionInfoSum

API_KEY = 'W7+/GTq80cr/PIeUvyWmPw==rNaA0JDPgZhSBk2c'


class NutritionEnricherService():

    def get_nutrition_info_sum_for_dish(dish_name: str) -> NutritionInfoSum:
        resp = requests.get(
            f"https://api.api-ninjas.com/v1/nutrition?query={dish_name}", headers={'X-Api-Key': API_KEY}).json()
        if len(resp) == 0:
            raise NotFoundError
        nutritionInfos = map(lambda x: NutritionInfo(**x), resp)
        return NutritionInfoSum.sum_nutrition_info(nutritionInfos)

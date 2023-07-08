from typing import List
from .NutritionInfo import NutritionInfo
from pydantic import BaseModel


class NutritionInfoSum(BaseModel):
    calories: float = 0.0
    serving_size_g: int = 0
    fat_total_g: float = 0.0
    fat_saturated_g: int = 0
    protein_g: float = 0.0
    sodium_mg: int = 0
    potassium_mg: int = 0
    cholesterol_mg: int = 0
    carbohydrates_total_g: float = 0.0
    fiber_g: float = 0.0
    sugar_g: float = 0

    def sum_nutrition_info(nutrition_info_list: List[NutritionInfo]):
        nutrition_info_sum = NutritionInfoSum()

        for nutrition_info in nutrition_info_list:
            nutrition_info_sum.calories += nutrition_info.calories
            nutrition_info_sum.serving_size_g += nutrition_info.serving_size_g
            nutrition_info_sum.fat_total_g += nutrition_info.fat_total_g
            nutrition_info_sum.fat_saturated_g += nutrition_info.fat_saturated_g
            nutrition_info_sum.protein_g += nutrition_info.protein_g
            nutrition_info_sum.sodium_mg += nutrition_info.sodium_mg
            nutrition_info_sum.potassium_mg += nutrition_info.potassium_mg
            nutrition_info_sum.cholesterol_mg += nutrition_info.cholesterol_mg
            nutrition_info_sum.carbohydrates_total_g += (
                nutrition_info.carbohydrates_total_g
            )
            nutrition_info_sum.fiber_g += nutrition_info.fiber_g
            nutrition_info_sum.sugar_g += nutrition_info.sugar_g

        return nutrition_info_sum

from pydantic import BaseModel


class NutritionInfo(BaseModel):
    name: str
    calories: float
    serving_size_g: int
    fat_total_g: float
    fat_saturated_g: int
    protein_g: float
    sodium_mg: int
    potassium_mg: int
    cholesterol_mg: int
    carbohydrates_total_g: float
    fiber_g: float
    sugar_g: float

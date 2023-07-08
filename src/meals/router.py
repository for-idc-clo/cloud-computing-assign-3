from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from .MealsService import MealsService
from .models.Meal import Meal
from .models.CreateMealDto import CreateMealDto
from .models.UpdateMealDto import UpdateMealDto
from common.errors.NotFound import NotFoundError
from common.errors.Conflict import ConflictError
from .errors.NonExistingDishInMeal import NonExistingDishInMeal

router = APIRouter()


NOT_FOUND_RESPONSE = PlainTextResponse("-5", status.HTTP_404_NOT_FOUND)


@router.get("/")
async def get_meals():
    meals = MealsService.get_meals()
    resp = {}
    for meal in meals:
        resp[meal.ID] = meal
    return resp


@router.post("/")
async def create_meal(data: CreateMealDto):
    try:
        dish_id = MealsService.create_meal(data)
        return PlainTextResponse(f"{dish_id}", status.HTTP_201_CREATED)
    except ConflictError:
        return PlainTextResponse("-2", status.HTTP_422_UNPROCESSABLE_ENTITY)
    except NonExistingDishInMeal:
        return PlainTextResponse("-6", status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.delete("/")
async def delete_all():
    return PlainTextResponse("This method is not allowed for the requested URL", status.HTTP_405_METHOD_NOT_ALLOWED)


@router.get("/{identifier}", response_model=Meal)
async def get_meal(identifier: int | str):
    try:
        if (type(identifier) == int):
            return MealsService.get_meal_by_id(identifier)
        return MealsService.get_meal_by_name(identifier)
    except NotFoundError:
        return NOT_FOUND_RESPONSE


@router.delete("/{identifier}")
async def delete_meal(identifier: int | str):
    try:
        if (type(identifier) == int):
            return MealsService.delete_meal_by_id(identifier)
        return MealsService.delete_meal_by_name(identifier)
    except NotFoundError:
        return NOT_FOUND_RESPONSE


@router.put("/{id}")
async def update_meal(id: int, data: UpdateMealDto):
    try:

        return MealsService.update_meal(id, data)
    except NotFoundError:
        return NOT_FOUND_RESPONSE

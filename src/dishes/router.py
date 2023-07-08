from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from meals.MealsService import MealsService
from common.errors.NotFound import NotFoundError
from common.errors.Conflict import ConflictError
from .DishesService import DishesService
from .models.Dish import Dish
from .models.CreateDishDto import CreateDishDto
from .errors.NoNutritionInfoFound import NoNutritionInfoFound
from .errors.NutritionEnricherError import NutritionEnricherError

router = APIRouter()


NOT_FOUND_RESPONSE = PlainTextResponse("-5", status.HTTP_404_NOT_FOUND)


@router.get("/")
async def get_dishes():
    dishes = DishesService.get_dishes()
    resp = {}
    for dish in dishes:
        resp[dish.ID] = dish
    return resp


@router.post("/")
async def create_dish(data: CreateDishDto):
    try:
        dish_id = DishesService.submit_dish(data)
        return PlainTextResponse(f"{dish_id}", status.HTTP_201_CREATED)
    except ConflictError:
        return PlainTextResponse("-2", status.HTTP_422_UNPROCESSABLE_ENTITY)
    except NoNutritionInfoFound:
        return PlainTextResponse("-3", status.HTTP_422_UNPROCESSABLE_ENTITY)
    except NutritionEnricherError:
        return PlainTextResponse("-4", status.HTTP_504_GATEWAY_TIMEOUT)


@router.delete("/")
async def delete_all():
    return PlainTextResponse("This method is not allowed for the requested URL", status.HTTP_405_METHOD_NOT_ALLOWED)


@router.get("/{identifier}", response_model=Dish)
async def get_dish(identifier: int | str):
    try:
        if (type(identifier) == int):
            return DishesService.get_dish_by_id(identifier)
        return DishesService.get_dish_by_name(identifier)
    except NotFoundError:
        return NOT_FOUND_RESPONSE


@router.delete("/{identifier}")
async def delete_dish(identifier: int | str):
    try:
        if (type(identifier) == int):
            result = DishesService.delete_dish_by_id(identifier)
        else:
            result = DishesService.delete_dish_by_name(identifier)

        MealsService.notify_deleted_dish(result)
        return result.ID
    except NotFoundError:
        return NOT_FOUND_RESPONSE

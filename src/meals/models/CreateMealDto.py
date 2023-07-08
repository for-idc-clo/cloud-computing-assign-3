from pydantic import BaseModel


class CreateMealDto(BaseModel):
    name: str
    appetizer: int
    main: int
    dessert: int

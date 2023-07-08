from pydantic import BaseModel


class UpdateMealDto(BaseModel):
    name: str
    appetizer: int
    main: int
    dessert: int

from pydantic import BaseModel


class Dish(BaseModel):
    ID: int
    name: str
    cal: float
    size: float
    sodium: int
    sugar: float

from pydantic import BaseModel


class Meal(BaseModel):
    ID: int
    name: str
    appetizer: int | None
    main: int | None
    dessert: int | None
    cal: float
    sodium: int
    sugar: float

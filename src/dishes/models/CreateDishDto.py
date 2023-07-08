from pydantic import BaseModel


class CreateDishDto(BaseModel):
    name: str

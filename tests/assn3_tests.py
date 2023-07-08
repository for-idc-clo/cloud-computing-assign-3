import pytest
import requests
import json

base_url = "http://localhost:8000"


def get_list_from_response(response):
    return [response[key] for key in response]


def test_dishes_post():
    dish_names = ["orange", "spaghetti", "apple pie"]
    ids = []
    for dish_name in dish_names:
        response = requests.post(f"{base_url}/dishes", json={"name": dish_name})
        assert response.status_code == 201
        dish_id = response.json()
        assert dish_id not in ids
        ids.append(dish_id)


def test_dishes_get_orange():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    dishes = get_list_from_response(response.json())
    orange_id = next(dish["ID"] for dish in dishes if dish["name"] == "orange")
    response = requests.get(f"{base_url}/dishes/{orange_id}")
    assert response.status_code == 200
    sodium = response.json()["sodium"]
    assert 0.9 <= sodium <= 1.1


def test_dishes_get():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_dishes_post_blah():
    response = requests.post(f"{base_url}/dishes", json={"name": "blah"})
    assert response.status_code in [400, 404, 422]
    assert response.json() == -3


def test_dishes_post_duplicate():
    response = requests.post(f"{base_url}/dishes", json={"name": "orange"})
    assert response.status_code in [400, 404, 422]
    assert response.json() == -2


def test_meals_post():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    dishes = get_list_from_response(response.json())
    dish_ids = {dish["name"]: dish["ID"] for dish in dishes}
    response = requests.post(
        f"{base_url}/meals",
        json={
            "name": "delicious",
            "appetizer": dish_ids["orange"],
            "main": dish_ids["spaghetti"],
            "dessert": dish_ids["apple pie"],
        },
    )
    assert response.status_code == 201
    assert response.json() > 0


def test_meals_get():
    response = requests.get(f"{base_url}/meals")
    assert response.status_code == 200
    meals = get_list_from_response(response.json())
    assert len(meals) == 1
    assert 400 <= meals[0]["cal"] <= 500


def test_meals_post_duplicate():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    dishes = get_list_from_response(response.json())
    dish_ids = {dish["name"]: dish["ID"] for dish in dishes}
    response = requests.post(
        f"{base_url}/meals",
        json={
            "name": "delicious",
            "appetizer": dish_ids["orange"],
            "main": dish_ids["spaghetti"],
            "dessert": dish_ids["apple pie"],
        },
    )
    assert response.status_code in [400, 422]
    assert response.json() == -2

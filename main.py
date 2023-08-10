import models
import peewee
from typing import List
from peewee import fn, JOIN

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def main():
    # cheapest_dish()
    vegetarian_dishes()
    # best_average_rating()


def cheapest_dish() -> models.Dish:
    """You want to get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    # Query to find the dish with the lowest price_in_cents
    query = models.Dish.select().order_by(models.Dish.price_in_cents).limit(1)

    # Execute the query and get the cheapest dish
    cheapest_dish = query.get()

    return cheapest_dish


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    # Filter vegetarian ingredients
    # vegetarian_ingredients = []
    # for ingredient in models.Ingredient.select().where(
    #     models.Ingredient.is_vegetarian == True
    # ):
    #     vegetarian_ingredients.append(ingredient.name)

    # Select all dishes that only have vegetarian ingredients
    # vegetarian_dishes = []
    # for dish in models.Dish:
    #     ingredients_per_dish = []
    #     for ingredient in dish.ingredients:
    #         ingredients_per_dish.append(ingredient.name)
    #     if set(ingredients_per_dish).issubset(set(vegetarian_ingredients)):
    #         vegetarian_dishes.append(dish.name)
    # print(vegetarian_dishes)
    # return vegetarian_dishes

    # Get list of names of vegetarian ingredients
    vegetarian_ingredients = []
    for ingredient in models.Ingredient.select().where(
        models.Ingredient.is_vegetarian == True
    ):
        vegetarian_ingredients.append(ingredient.name)

    # Query to retrieve dishes with vegetarian ingredients
    query = (
        models.Dish.select(models.Dish.name)
        .join(models.DishIngredient)
        .join(
            vegetarian_ingredients,
            on=(models.DishIngredient.ingredient == vegetarian_ingredients),
        )
        .group_by(models.Dish)
    )

    vegetarian_dish_list = query.execute()

    print("Vegetarian Dishes:")

    for dish in vegetarian_dish_list:
        print(f"- {dish.name}")
    return vegetarian_dish_list


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    # Define an alias for the average rating column
    avg_rating = fn.AVG(models.Rating.rating).alias("average_rating")

    # Query to join Restaurant and Rating models, calculate average ratings,
    # and order by average rating in descending order
    query = (
        models.Restaurant.select(models.Restaurant, avg_rating)
        .join(models.Rating)
        .group_by(models.Restaurant)
        .order_by(avg_rating.desc())
        .limit(1)
    )

    # Execute the query and get the restaurant with the highest average rating
    highest_rated_restaurant = query.get()
    print("Restaurant with Highest Average Rating:")
    print(
        f"ID: {highest_rated_restaurant.id}, Name: {highest_rated_restaurant.name}, Average Rating: {highest_rated_restaurant.average_rating}"
    )
    return highest_rated_restaurant


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    ...


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    ...


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ...


if __name__ == "__main__":
    main()

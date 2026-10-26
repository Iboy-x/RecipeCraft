"""Coordinate recipe loading, scaling, dietary checks, and substitutions."""
from .recipe_loader import load_recipe
from .recipe_scaler import scale_ingredients
from .dietary_checker import check_dietary_restrictions
from .substitution_engine import find_substitute


def prepare_recipe_result(filename, target_servings, restrictions=None, recipes_dir=None):
    """Prepare the single result dictionary used by the Flask result template."""
    recipe = load_recipe(filename, recipes_dir)
    if target_servings < 1:
        raise ValueError("Target serving count must be at least 1.")
    ingredients = scale_ingredients(recipe["ingredients"], recipe["original_servings"], target_servings)
    dietary_result = check_dietary_restrictions(ingredients, restrictions or [])
    substitutions = []
    for ingredient in ingredients:
        substitution = find_substitute(
            ingredient["name"], restrictions=restrictions,
            available=ingredient["substitute_available"],
        )
        substitutions.append({"ingredient": ingredient["name"], **substitution})
    return {
        "recipe": recipe,
        "target_servings": target_servings,
        "ingredients": ingredients,
        "dietary": dietary_result,
        "substitutions": substitutions,
    }

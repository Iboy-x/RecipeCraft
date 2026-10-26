"""Starter substitution lookup with a safe extension point for recursion."""

# Demonstration data only. These are not guaranteed to suit every recipe.
MOCK_SUBSTITUTIONS = {
    "yogurt": "plain unsweetened plant-based yogurt (check recipe compatibility)",
    "butter": "a suitable plant-based baking spread (check recipe compatibility)",
    "milk": "unsweetened plant-based milk (choose one suited to the recipe)",
}


def find_substitute(ingredient_name, restrictions=None, visited=None, available="Y"):
    """Return a mock substitute only when the file marks one as available.

    `visited` is a set of ingredient names reserved for a future recursive
    candidate-search implementation. The current starter lookup does not recurse.
    """
    restrictions = restrictions or []
    visited = set() if visited is None else set(visited)
    key = ingredient_name.strip().lower()
    if key in visited:
        return {"available": False, "substitute": None, "status": "cycle_prevented"}
    visited.add(key)
    if str(available).upper() != "Y":
        return {"available": False, "substitute": None, "status": "not_available_in_recipe"}
    substitute = MOCK_SUBSTITUTIONS.get(key)
    if not substitute:
        return {"available": True, "substitute": None, "status": "placeholder_no_mock_match"}
    return {
        "available": True,
        "substitute": substitute,
        "status": "mock_suggestion",
        "message": "Demonstration suggestion only; validate suitability before using it.",
    }

"""Discover and parse recipe text files."""
from pathlib import Path


def _display_name(filename):
    """Convert a filename such as Chicken_Biryani.txt to a readable name."""
    return Path(filename).stem.replace("_", " ").replace("-", " ").strip()


def discover_recipes(recipes_dir=None):
    """Return sorted recipe filenames for all .txt files in the recipe folder."""
    folder = Path(recipes_dir) if recipes_dir else Path(__file__).resolve().parent.parent / "recipes"
    if not folder.exists():
        return []
    return sorted(path.name for path in folder.glob("*.txt") if path.is_file())


def load_recipe(filename, recipes_dir=None):
    """Parse one recipe file into a dictionary, raising ValueError for bad format.

    Expected format: serving count, Ingredients heading, ingredient rows, Recipe
    heading, then one or more lines of cooking instructions. Ingredient rows use
    `quantity, ingredient name, Y/N`; commas inside fields are not supported.
    """
    folder = Path(recipes_dir) if recipes_dir else Path(__file__).resolve().parent.parent / "recipes"
    # Restrict reads to a plain filename in the configured recipe directory.
    if Path(filename).name != filename or Path(filename).suffix.lower() != ".txt":
        raise ValueError("Recipe must be a .txt filename inside the recipes folder.")
    path = folder / filename
    if not path.is_file():
        raise ValueError(f"Recipe file '{filename}' was not found.")

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        raise ValueError("The file is empty.")

    try:
        original_servings = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError("Line 1 must contain a positive whole-number serving count.") from exc
    if original_servings < 1:
        raise ValueError("Original serving count must be at least 1.")

    ingredients_heading = next((i for i, line in enumerate(lines) if line.strip().lower() == "ingredients"), None)
    recipe_heading = next((i for i, line in enumerate(lines) if line.strip().lower() == "recipe"), None)
    if ingredients_heading is None or recipe_heading is None or recipe_heading <= ingredients_heading:
        raise ValueError("Expected an 'Ingredients' heading followed by a 'Recipe' heading.")

    ingredients = []
    for line_number, line in enumerate(lines[ingredients_heading + 1:recipe_heading], start=ingredients_heading + 2):
        if not line.strip():
            continue
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3 or not parts[0] or not parts[1] or parts[2].upper() not in {"Y", "N"}:
            raise ValueError(
                f"Malformed ingredient row on line {line_number}: '{line}'. "
                "Expected: quantity, ingredient name, Y/N."
            )
        ingredients.append({
            "quantity": parts[0],
            "name": parts[1],
            "substitute_available": parts[2].upper(),
        })
    if not ingredients:
        raise ValueError("No ingredient rows were found between the headings.")

    instructions = [line.strip() for line in lines[recipe_heading + 1:] if line.strip()]
    if not instructions:
        raise ValueError("No cooking instructions were found after the 'Recipe' heading.")

    return {
        "filename": filename,
        "name": _display_name(filename),
        "original_servings": original_servings,
        "ingredients": ingredients,
        "instructions": instructions,
    }


def load_all_recipes(recipes_dir=None):
    """Return (valid_recipes, errors), skipping malformed files safely."""
    recipes, errors = [], []
    for filename in discover_recipes(recipes_dir):
        try:
            recipes.append(load_recipe(filename, recipes_dir))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append({"filename": filename, "message": str(exc)})
    return recipes, errors

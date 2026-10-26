"""Flask web application for the RecipeCraft student project."""
from pathlib import Path
from flask import Flask, render_template, request
from modules.recipe_loader import load_all_recipes
from modules.recipe_manager import prepare_recipe_result

BASE_DIR = Path(__file__).resolve().parent
RECIPES_DIR = BASE_DIR / "recipes"
app = Flask(__name__)


def get_recipe_data():
    """Load recipes and parse errors using paths relative to this file."""
    return load_all_recipes(RECIPES_DIR)


@app.get("/")
def index():
    recipes, errors = get_recipe_data()
    return render_template("index.html", recipes=recipes, errors=errors)


@app.post("/recipe")
def recipe_result():
    recipes, errors = get_recipe_data()
    filename = request.form.get("recipe", "").strip()
    restrictions = request.form.getlist("restrictions")
    serving_text = request.form.get("servings", "1").strip()

    try:
        servings = int(serving_text)
        if servings < 1:
            raise ValueError
    except (TypeError, ValueError):
        return render_template(
            "index.html", recipes=recipes, errors=errors,
            form_error="Serving count must be a whole number of at least 1.",
            selected_recipe=filename, selected_servings=serving_text,
            selected_restrictions=restrictions,
        ), 400

    if not filename:
        return render_template(
            "index.html", recipes=recipes, errors=errors,
            form_error="Please select a recipe.", selected_recipe=filename,
            selected_servings=servings, selected_restrictions=restrictions,
        ), 400

    # Only accept a filename discovered by the backend. Never trust arbitrary paths.
    available_names = {recipe["filename"] for recipe in recipes}
    if filename not in available_names:
        return render_template(
            "index.html", recipes=recipes, errors=errors,
            form_error="That recipe is unavailable or could not be parsed. Check the recipe list below.",
            selected_servings=servings, selected_restrictions=restrictions,
        ), 400

    try:
        result = prepare_recipe_result(filename, servings, restrictions, RECIPES_DIR)
    except (OSError, ValueError) as exc:
        return render_template(
            "index.html", recipes=recipes, errors=errors,
            form_error=f"Could not prepare this recipe: {exc}",
            selected_recipe=filename, selected_servings=servings,
            selected_restrictions=restrictions,
        ), 400

    return render_template("result.html", result=result)


if __name__ == "__main__":
    # Debug mode is convenient for local coursework. Do not use it for deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)

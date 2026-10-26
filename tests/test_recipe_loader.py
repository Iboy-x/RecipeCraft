"""Small unit tests for the recipe loader; run with `python -m unittest discover -s tests`."""
import tempfile
import unittest
from pathlib import Path
from modules.recipe_loader import discover_recipes, load_recipe, load_all_recipes

VALID_RECIPE = """1
Ingredients
200 g, Chicken, Y
1/2 tsp, Salt, N
Recipe
1. Prepare the ingredients.
2. Cook until ready.
"""


class RecipeLoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_discover_recipes_finds_txt_files_only(self):
        (self.folder / "Pasta.txt").write_text(VALID_RECIPE, encoding="utf-8")
        (self.folder / "notes.md").write_text("not a recipe", encoding="utf-8")
        self.assertEqual(discover_recipes(self.folder), ["Pasta.txt"])

    def test_load_recipe_parses_fields(self):
        (self.folder / "Chicken_Biryani.txt").write_text(VALID_RECIPE, encoding="utf-8")
        recipe = load_recipe("Chicken_Biryani.txt", self.folder)
        self.assertEqual(recipe["name"], "Chicken Biryani")
        self.assertEqual(recipe["original_servings"], 1)
        self.assertEqual(recipe["ingredients"][1]["quantity"], "1/2 tsp")
        self.assertEqual(recipe["ingredients"][1]["substitute_available"], "N")
        self.assertEqual(len(recipe["instructions"]), 2)

    def test_malformed_file_is_reported_not_crashed(self):
        (self.folder / "Bad.txt").write_text("1\nIngredients\nwrong row\nRecipe\nCook it", encoding="utf-8")
        recipes, errors = load_all_recipes(self.folder)
        self.assertEqual(recipes, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("Malformed ingredient row", errors[0]["message"])

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            load_recipe("../secret.txt", self.folder)


if __name__ == "__main__":
    unittest.main()

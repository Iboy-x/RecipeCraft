# RecipeCraft: Smart Recipe Scaling and Substitution System

A beginner-friendly Flask skeleton for a Computational Thinking project. It loads recipe `.txt` files from `recipes/`, lets a user select a recipe and serving count, and displays scaled ingredients, instructions, and clearly labelled dietary/substitution placeholders.

## Project structure

```text
RecipeCraft/
├── app.py
├── recipes/                 # Put your ten existing .txt files here
├── modules/
│   ├── __init__.py
│   ├── recipe_loader.py
│   ├── recipe_scaler.py
│   ├── dietary_checker.py
│   ├── substitution_engine.py
│   └── recipe_manager.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
├── tests/
│   └── test_recipe_loader.py
├── requirements.txt
└── README.md
```

## 1. Add your existing recipe files

Copy your ten existing `.txt` recipe files into the `recipes/` folder. Keep their contents unchanged. The app discovers files dynamically; it does not need a hardcoded recipe list. This starter package intentionally does not create replacement recipe files. If the folder is empty, the home page displays a helpful message and the submit button is disabled.

The parser expects:

1. First non-empty line: a positive integer for original servings.
2. A line containing `Ingredients`.
3. Ingredient rows in `quantity, ingredient name, Y/N` format.
4. A line containing `Recipe`.
5. One or more instruction lines after `Recipe`.

For example, `1/2 tsp, Salt, N` is accepted. Ingredient names and quantities must not contain commas in this simple format. Blank lines between ingredient rows or instructions are ignored. The filename becomes the displayed recipe name, with underscores and hyphens converted to spaces.

## 2. Set up and run

Open a terminal in the `RecipeCraft` folder.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks virtual-environment activation, use Command Prompt instead:

```bat
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the server with `Ctrl+C` in the terminal.

## 3. Run tests

From the project folder, with the same Python environment activated:

```bash
python -m unittest discover -s tests -v
```

## How the components connect

1. `app.py` serves the home page and gets recipes from `recipe_loader.py`.
2. The Jinja template displays the discovered recipe filenames in a dropdown.
3. Submitting the form sends the selected filename, servings, and dietary choice to Flask's `/recipe` route.
4. `recipe_manager.py` loads the selected recipe, calls the scaler and dietary checker, and gathers substitution status.
5. Flask sends the structured result to `result.html` for rendering.

## Functional vs. placeholder features

- **Functional:** dynamic `.txt` discovery; filename-based names; file parsing; malformed-file error reporting; serving input validation; scaling of leading integers, decimals, and simple fractions; ingredient and instruction display; `Y/N` substitution availability; form submission; responsive basic styling; loader unit tests.
- **Placeholder:** dietary restriction matching is not implemented. The result explicitly warns users not to rely on it for allergies or medical dietary needs.
- **Placeholder:** substitution examples are mock data only. Ingredients marked `N` never receive a substitute suggestion. Unmatched `Y` ingredients report that no mock suggestion is configured.
- **Not implemented yet:** comprehensive unit conversion, ranges such as `1-2`, mixed fractions such as `1 1/2`, natural-language quantities such as `to taste`, allergen detection, and recursive substitution candidate search. Unsupported quantities remain unchanged and are marked unscaled.

## Computational Thinking concepts

- **Lists:** ingredient records and instruction lines.
- **Dictionaries:** recipe records, ingredient records, dietary status, and substitution mapping.
- **Strings:** parsing text lines and formatting quantity labels.
- **Nested iteration:** dietary-check extension point compares each ingredient against each selected restriction.
- **Recursion design:** `find_substitute()` accepts a `visited` set and prevents repeated ingredient names. The current mock lookup does not recurse; a future candidate graph search can recurse through alternatives and stop when it finds a valid candidate or reaches a visited node.
- **Modular functions:** loading, scaling, dietary checking, substitution, coordination, and web routing are separated.

## Troubleshooting

- **No recipes appear:** check that `.txt` files are inside `RecipeCraft/recipes/` and that their extension is `.txt`.
- **A file is listed as invalid:** verify the first non-empty line is a positive integer, the two headings are spelled `Ingredients` and `Recipe`, and each ingredient row has exactly three comma-separated fields ending in `Y` or `N`.
- **Scaling leaves a quantity unchanged:** the quantity format is unsupported. Check the note shown beside the ingredient; do not assume it was scaled.
- **Port 5000 is busy:** stop the other server, or change `port=5000` in the final `app.run(...)` line of `app.py` to another available port, such as `5001`, then open the matching local URL.
- **Flask is not found:** activate the virtual environment and run `pip install -r requirements.txt` again.

## Safety and project scope

This is a coursework skeleton, not a production recipe or food-safety system. Dietary checks and substitutions are not validated and must not be relied on for allergies or medical needs. The Flask development server's debug mode is intended only for local development, not deployment.

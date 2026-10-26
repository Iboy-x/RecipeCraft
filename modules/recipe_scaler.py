"""Conservative ingredient quantity scaling helpers."""
import re
from fractions import Fraction

_NUMBER = re.compile(r"^\s*(\d+(?:\.\d+)?|\d+\s*/\s*\d+)\s*(.*)$")


def scale_quantity(quantity, original_servings, target_servings):
    """Scale a leading decimal/integer/fraction and preserve the remaining unit.

    Supported examples: '200 g', '1.5 cups', '1/2 tsp', '2'. Unsupported
    formats (ranges, words such as 'to taste', mixed fractions) are preserved
    unchanged and flagged as unscaled rather than guessed.
    """
    text = str(quantity).strip()
    if original_servings < 1 or target_servings < 1:
        raise ValueError("Serving counts must be at least 1.")
    match = _NUMBER.match(text)
    if not match:
        return {"quantity": text, "scaled": False, "note": "Quantity format not supported; original kept."}
    number_text, remainder = match.groups()
    try:
        amount = float(Fraction(number_text.replace(" ", "")))
    except (ValueError, ZeroDivisionError):
        return {"quantity": text, "scaled": False, "note": "Quantity format not supported; original kept."}
    scaled_amount = amount * target_servings / original_servings
    if scaled_amount.is_integer():
        rendered = str(int(scaled_amount))
    else:
        rendered = f"{scaled_amount:.3f}".rstrip("0").rstrip(".")
    return {"quantity": f"{rendered}{(' ' + remainder) if remainder else ''}", "scaled": True, "note": ""}


def scale_ingredients(ingredients, original_servings, target_servings):
    """Return copied ingredient records with scaled quantities and status."""
    scaled = []
    for ingredient in ingredients:
        quantity_result = scale_quantity(ingredient["quantity"], original_servings, target_servings)
        scaled.append({**ingredient, **quantity_result})
    return scaled

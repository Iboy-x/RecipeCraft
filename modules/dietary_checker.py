"""Placeholder for future dietary restriction checks."""


def check_dietary_restrictions(ingredients, restrictions):
    """Return a structured placeholder; this is not a real safety check."""
    selected = [item for item in restrictions if item]
    # Extension point: compare each ingredient against rules for each restriction.
    comparisons_made = 0
    for ingredient in ingredients:
        for restriction in selected:
            comparisons_made += 1
            # Real ingredient classification and rule matching belong here.
    return {
        "status": "PLACEHOLDER",
        "is_placeholder": True,
        "restrictions": selected,
        "message": "Dietary checks are not implemented yet. Do not rely on this result for allergies or medical dietary needs.",
        "comparisons_planned": comparisons_made,
    }

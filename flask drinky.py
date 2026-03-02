from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder="web")


def _split_instructions(text):
    if not isinstance(text, str):
        return []

    normalized = text.replace("\r", "\n").replace(".", "\n")
    steps = [step.strip(" -\t") for step in normalized.split("\n") if step.strip()]
    return steps


def _extract_ingredients(drink):
    ingredients = []

    if isinstance(drink.get("ingredients"), list):
        for item in drink["ingredients"]:
            if isinstance(item, dict):
                name = item.get("name") or item.get("ingredient") or item.get("title")
                amount = item.get("amount") or item.get("measure") or item.get("quantity")
                if name and amount:
                    ingredients.append(f"{amount} {name}".strip())
                elif name:
                    ingredients.append(str(name).strip())
            elif isinstance(item, str) and item.strip():
                ingredients.append(item.strip())

    if not ingredients:
        for key, value in drink.items():
            if not isinstance(key, str):
                continue
            key_lower = key.lower()
            if "ingredient" in key_lower and value:
                ingredients.append(str(value).strip())

    return ingredients


def _extract_steps(drink):
    instruction_keys = [
        "instructions",
        "method",
        "preparation",
        "recipe",
        "description",
    ]

    for key in instruction_keys:
        value = drink.get(key)
        if isinstance(value, list):
            return [str(step).strip() for step in value if str(step).strip()]
        if isinstance(value, str) and value.strip():
            return _split_instructions(value)

    return []


def _build_cocktail_view(drink):
    ingredients = _extract_ingredients(drink)
    steps = _extract_steps(drink)

    return {
        "name": drink.get("name", "Unknown drink"),
        "image": drink.get("image"),
        "ingredients": ingredients,
        "steps": steps,
    }


@app.route('/')
def hello():
    response = requests.get("https://boozeapi.com/api/v1/cocktails")

    if response.status_code == 200:
        raw = response.json()
        cocktails = [_build_cocktail_view(drink) for drink in raw.get("data", [])]

        return render_template("index.html", cocktails=cocktails)

    return "Error loading cocktails"


if __name__ == "__main__":
    app.run(debug=True)

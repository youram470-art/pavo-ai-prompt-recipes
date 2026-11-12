#!/usr/bin/env python3
"""Render prompt recipes into finished prompts.

    python3 render.py recipes/food.json --set subject="miso ramen"
    python3 render.py recipes/food.json --set subject="miso ramen" --style editorial --json

A recipe is a small JSON file: a base template with {placeholders}, named
style modifiers, and the negative prompt that goes with it.
"""

import argparse
import json
import sys

REQUIRED = ("name", "template", "styles", "negative")


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        raise ValueError("%s is missing: %s" % (path, ", ".join(missing)))
    return data


def placeholders(template):
    """Names used like {subject} in a template, in order of appearance."""
    names = []
    start = template.find("{")
    while start != -1:
        end = template.find("}", start)
        if end == -1:
            break
        name = template[start + 1:end]
        if name not in names:
            names.append(name)
        start = template.find("{", end)
    return names


def render(recipe, values, style=None):
    needed = placeholders(recipe["template"])
    missing = [k for k in needed if k not in values]
    if missing:
        raise ValueError("missing placeholders: %s (need: %s)"
                         % (", ".join(missing), ", ".join(needed)))
    prompt = recipe["template"]
    for key in needed:
        prompt = prompt.replace("{%s}" % key, values[key])

    parts = [prompt.strip()]
    if style:
        if style not in recipe["styles"]:
            raise ValueError("unknown style %r (have: %s)"
                             % (style, ", ".join(sorted(recipe["styles"]))))
        parts.append(recipe["styles"][style])

    return {
        "name": recipe["name"],
        "style": style,
        "prompt": ", ".join(p for p in parts if p),
        "negative": recipe["negative"],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("recipe", help="path to a recipe JSON file")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="fill a placeholder; repeatable")
    ap.add_argument("--style", help="named style modifier from the recipe")
    ap.add_argument("--list-styles", action="store_true", help="list styles and exit")
    ap.add_argument("--json", action="store_true", help="print JSON instead of plain text")
    args = ap.parse_args(argv)

    recipe = load(args.recipe)

    if args.list_styles:
        for name in sorted(recipe["styles"]):
            print("%-12s %s" % (name, recipe["styles"][name]))
        return 0

    values = {}
    for pair in args.set:
        if "=" not in pair:
            raise SystemExit("--set expects KEY=VALUE, got %r" % pair)
        key, value = pair.split("=", 1)
        values[key] = value

    result = render(recipe, values, args.style)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["prompt"])
        print("negative: %s" % result["negative"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

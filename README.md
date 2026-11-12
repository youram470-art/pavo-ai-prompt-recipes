# pavo-ai-prompt-recipes

Prompt recipes for image and video generation, plus a tiny renderer that fills
the placeholders and appends a named style modifier.

The point is to keep the *structure* of a good prompt in a file instead of in
someone's head, so a team produces the same look from a one-line subject.

```bash
python3 render.py recipes/food.json --set subject="miso ramen" --style editorial
```

```
miso ramen, steam rising, shot in a home kitchen, shallow depth of field, 50mm, soft window light from the left, muted colour palette, film grain
negative: plastic texture, oversaturated, text, watermark, extra utensils
```

## Recipes

| file | what it is for |
| --- | --- |
| `recipes/food.json` | food close-ups: editorial, menu, documentary looks |
| `recipes/interior.json` | wide interior establishing shots |

List the styles a recipe offers:

```bash
python3 render.py recipes/interior.json --list-styles
```

Machine-readable output, for a batch job:

```bash
python3 render.py recipes/food.json --set subject="cold soba" --style menu --json
```

```json
{
  "name": "food-closeup",
  "style": "menu",
  "prompt": "cold soba, steam rising, ...",
  "negative": "plastic texture, oversaturated, text, watermark, extra utensils"
}
```

## Recipe format

```json
{
  "name": "food-closeup",
  "template": "{subject}, steam rising, shot in a home kitchen, 50mm",
  "styles": { "editorial": "soft window light, film grain" },
  "negative": "text, watermark",
  "notes": "free text for humans"
}
```

Placeholders are written `{like-this}`; every one in `template` must be passed
with `--set`. Unknown placeholders and unknown style names fail loudly rather
than producing a half-filled prompt.

## Notes on writing recipes

- One hero subject per template. Two subjects and the model averages them.
- Put camera and lens after the subject: they read as modifiers.
- Keep the negative prompt short; long lists of negatives tend to remove
  details that belong in the frame.

The recipes here were written against the prompt format of
[Pavo AI](https://pavoai.app/), which generates images and short video clips.

## License

MIT

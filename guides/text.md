---
title: Drawing text
summary: Load fonts, place and measure text, fill it with any brush, wrap it to a box, and scroll it — everything you need for menus, labels, and messages.
icon: text_fields
---

# Introduction

Almost every app needs to say something — a label, a score, a menu, a clock. Badgeware draws text with a single call, `screen.text()`, using whatever font and brush you've set. The same call works on the screen or on any image, so everything here applies equally to off-screen drawing.

Two things decide how your text looks: the **font** you pick, and the **brush** you draw it with. We'll cover both, then wrapping, scrolling, and inline styling.

# Pixel fonts and vector fonts

Badgeware has two kinds of font, and it's worth knowing which you're reaching for:

| | Pixel fonts | Vector fonts |
|---|---|---|
| Loaded with | `font.<name>` or `font.load()` | `font.load()` |
| Stored as | `.ppf` — bitmaps | `.af` — scalable outlines |
| Sizing | native size, or an integer scale (2×, 3×…) | any pixel size you ask for |
| Character | crisp, retro, pixel-exact | smooth, scales to any size |
| Best for | small screens, UI, that pixel look | headings and large or unusual sizes |

There are over thirty pixel fonts baked into ROM — browse them in the [font gallery](/api/font.md#font-gallery) — plus three vector fonts preloaded under `/system/assets/fonts/`. You load a font once and assign it to `screen.font`; swapping between fonts is just another assignment.

# Drawing text

Set a font, set a pen, and call `screen.text(message, x, y)`. The `x, y` is the **top-left** corner of the text. A pixel font draws at its native size; a vector font takes a size, in pixels, as a fourth argument:

```python
mona = font.load("/system/assets/fonts/MonaSans-Medium.af")
screen.antialias = image.X4     # smooth vector font edges

while True:
  screen.pen = color.navy
  screen.clear()

  screen.pen = color.white

  # a pixel font: crisp, drawn at its native size
  screen.font = font.smart
  screen.text("Pixel perfect", 10, 14)

  # a vector font: pass a size in pixels and it scales cleanly
  screen.font = mona
  screen.text("Any size", 10, 44, 30)

  badge.update()
```

Loading a font is a little expensive, so do it **once** at the start — never inside the loop. Assigning `screen.font` afterwards is cheap.

Pixel fonts can be scaled too, by passing an integer as that fourth argument — `screen.text("BIG", 10, 40, 3)` draws at 3× size, staying pixel-crisp.

For smooth edges on vector fonts, turn on antialiasing with `screen.antialias = image.X2` or `image.X4` (as in the example above). It applies to all vector drawing; pixel fonts are already pixel-exact, so it leaves them untouched.

# The text cursor

Every `screen.text()` call also moves an invisible **cursor** to the start of the next line — so, just like Python's `print()`, you can keep calling `screen.text()` with no coordinates and each line stacks below the last:

```python
screen.font = font.smart

lines = ["Shopping list:", "- lemons", "- olive oil", "- a nice hat"]

while True:
  screen.pen = color.navy
  screen.clear()

  screen.pen = color.white
  screen.cursor = vec2(12, 12)   # where the first line goes
  for line in lines:
    screen.text(line)            # no x, y — each falls on the next line

  badge.update()
```

`screen.cursor` is a `vec2` you can read or set at any time; assigning it positions the *next* `screen.text()`. A `\n` inside a string does the same thing mid-string, dropping to a new line at the x the line started at:

```python
screen.text("two\nlines", 10, 10)   # draws "two", then "lines" below it
```

Give `screen.text()` an explicit `x, y` whenever you want to jump somewhere; leave it off to keep flowing from the cursor.

# Placing and measuring

To centre or right-align text you need to know how wide it is. `measure_text()` returns the width and height the string *would* take with the current font — pass the size too for a vector font:

```python
mona = font.load("/system/assets/fonts/MonaSans-Medium.af")
screen.font = mona
screen.antialias = image.X4     # smooth vector font edges

while True:
  screen.pen = color.rgb(20, 24, 40)
  screen.clear()

  message = "Centred"
  w, h = screen.measure_text(message, 34)
  x = (screen.width - w) // 2
  y = (screen.height - h) // 2

  screen.pen = color.white
  screen.text(message, x, y, 34)

  badge.update()
```

The same trick right-aligns text (`x = screen.width - w`) or lets you draw a background box exactly the size of the words inside it.

# Colour, shadows and outlines

Text is drawn with the current brush — whatever you last assigned to `screen.pen`. That's usually a solid colour, but any brush works, so you can fill letters with gradients or patterns. It also means effects like shadows and outlines are just the *same string drawn more than once*: draw it offset and dark underneath, then draw it again on top.

```python
screen.font = font.smart

def outline_text(message, x, y):
  # draw the text shifted in eight directions for a solid outline
  screen.pen = color.black
  for ox, oy in ((-1, -1), (0, -1), (1, -1), (-1, 0),
                 (1, 0), (-1, 1), (0, 1), (1, 1)):
    screen.text(message, x + ox, y + oy)
  # then the fill, once, on top
  screen.pen = color.yellow
  screen.text(message, x, y)

while True:
  screen.pen = color.rgb(40, 80, 40)
  screen.clear()
  outline_text("Outlined!", 34, 52)
  badge.update()
```

A drop shadow is the same idea with a single offset — draw the string once in a dark, semi-transparent colour a pixel down and right, then the real text on top.

# Wrapping text to fit

Given an `x, y`, `screen.text()` draws a single line and lets it run off the edge. Give it a `rect` instead and it flows the string into that rectangle, breaking it onto new lines as it fills the width:

```python
screen.font = font.sins

message = ("Badgeware wraps long text for you: hand screen.text a "
           "rectangle and it flows the words onto as many lines "
           "as it needs to fit the width.")

while True:
  screen.pen = color.navy
  screen.clear()

  screen.pen = color.white
  screen.text(message, rect(10, 10, 140, 100))

  badge.update()
```

The `rect` is the area to fill; text that runs past the bottom is clipped. You can also tune the line and word spacing, covered in the [`text` API](/api/text.md#text-in-a-box).

# Aligning a block

Drawing into a `rect` positions the block for you, so you rarely need to measure by hand. Pass `align` a pair of constants, one for the horizontal and one for the vertical:

```python
screen.font = font.sins

message = "Badgeware lines this text up for you, horizontally and vertically, inside the box."

while True:
  screen.pen = color.navy
  screen.clear()

  # a faint box so you can see the bounds it aligns within
  screen.pen = color.rgb(30, 40, 70)
  screen.shape(shape.rectangle(10, 10, 140, 100))

  screen.pen = color.white
  screen.text(message, rect(10, 10, 140, 100), align=(image.CENTER, image.MIDDLE))

  badge.update()
```

The horizontal constant is `image.LEFT` (the default), `image.CENTER` or `image.RIGHT`; the vertical one is `image.TOP`, `image.MIDDLE` or `image.BOTTOM`. Pass `overflow=image.ELLIPSES` and text that's too tall to fit is cut off with a trailing `...` rather than clipped mid-line. `screen.text()` also returns the `rect` it filled, which is handy for placing something right after it.

# Scrolling text

A single line sweeping across the screen suits a small display well, and there's no special trick to it: measure the text, then move it a little further left each frame based on the clock. Drawing a second copy one text-width behind makes it loop seamlessly:

```python
screen.font = font.smart

message = "Now showing on Badgeware... "
w, h = screen.measure_text(message)
period = w + 20     # the text width plus a gap before it repeats
y = (screen.height - h) // 2

while True:
  screen.pen = color.grape
  screen.clear()

  # scroll left at 40 px/s; two copies a period apart wrap seamlessly
  off = badge.ticks * 40 // 1000 % period
  screen.pen = color.white
  screen.text(message, -off, y)
  screen.text(message, period - off, y)

  badge.update()
```

Because the motion comes from `badge.ticks`, the speed stays a true pixels-per-second whatever the framerate. Widen the `+ 20` to space the repeats further apart, or draw into a [`window()`](/api/image.md#window) to scroll within just part of the screen.

# Rich text

For styling *within* a string — a word in a different colour, an inline icon — Badgeware has **glyph renderers**. You call one inline with `[name]` or `[name:arguments]`. Two come built in: `[pen:r,g,b]` recolours the text that follows, and `[sprite:name]` drops in an image you've registered. So changing colour mid-string needs no code at all:

```python
screen.font = font.sins

message = "Written in [pen:220,80,80]red[pen:230,240,230] and white."

while True:
  screen.pen = color.navy
  screen.clear()
  screen.pen = color.rgb(230, 240, 230)
  screen.text(message, rect(10, 40, 140, 60))
  badge.update()
```

Markup is read only when you draw into a `rect`. Pass an `x, y` and the brackets appear on screen as written.

To make your own, write a function taking `(image, parameters, measure)` and register it with `add_glyph()` under the name you'll call it by. Layout runs it twice. When `measure` is `True` it returns the width it occupies and draws nothing. Otherwise it draws, reading `image.cursor`, a `vec2`, for the position the text has reached:

```python
screen.font = font.sins

# an inline [box] that draws a small square where the text has got to
def box(image, parameters, measure):
  if measure:
    return 10                    # the width we take up in the line
  image.pen = color.yellow
  image.shape(shape.rectangle(image.cursor.x, image.cursor.y, 8, 8))
  return None

add_glyph("box", box)
message = "tick the [box] and carry on"

while True:
  screen.pen = color.navy
  screen.clear()
  screen.pen = color.white

  screen.text(message, rect(10, 40, 140, 60))

  badge.update()
```

A renderer can do anything — draw an image, a shape, adjust spacing — which makes it easy to mix icons and coloured highlights into a line of text. The [`text` API](/api/text.md#glyph-renderers) covers the full set of parameters and more examples.

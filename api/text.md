---
title: text
summary: Wrap and align text inside a box, style it inline with glyph renderers, and scroll it across the screen.
icon: format_align_left
publish: true
---
# Introduction
[`image.text()`](/api/image.md#text) draws a single run of text wherever you point it. Hand it a `rect` instead and it does rather more: wrapping the words onto new lines, aligning the block, truncating what doesn't fit, and rendering inline `[markup]`. This page covers those features, plus the `text` module, which adds a scrolling helper.

# Text in a box
Pass a `rect` as the position and the text is laid out inside it, breaking onto a new line each time it fills the width. Anything that runs past the bottom is clipped.

### Usage
`.text(message, bounds, size, align, overflow, line_height, word_spacing)`

| Parameter | Type | Description |
|---|---|---|
| `message` | `string` | The text to draw |
| `bounds` | `rect` | The area to lay the text out within |
| `size` | `int` | *Optional.* Point size for a vector font, or integer scale for a pixel font. See [font size](/api/font.md#introduction). As a keyword it's spelled `font_size` |
| `align` | `tuple` | *Optional.* Keyword only. Horizontal and vertical alignment, as a pair of constants. Defaults to `(image.LEFT, image.TOP)` |
| `overflow` | `int` | *Optional.* Keyword only. `image.CLIP` (default) or `image.ELLIPSES` |
| `line_height` | `float` | *Optional.* Keyword only. Line height multiplier. Defaults to `1` |
| `word_spacing` | `float` | *Optional.* Keyword only. Space width multiplier. Defaults to `1` |

### Returns
A `rect` describing the bounding box that was drawn, handy for laying out further content beneath or beside the text.

```python
screen.font = font.sins
screen.pen = color.rgb(0, 0, 255)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Well hello there, world! This is a nice long message that's designed to split over several lines, so I'm just going to ramble on for a little while."
    screen.text(message, bounds)

run(update)
```

## Alignment
`align` takes a pair: a horizontal constant and a vertical one. The horizontal one positions each line within the width, the vertical one positions the block as a whole within the height.

| Constant | Use |
|---|---|
| `image.LEFT`, `image.CENTER`, `image.RIGHT` | Horizontal alignment |
| `image.TOP`, `image.MIDDLE`, `image.BOTTOM` | Vertical alignment |

Pass a single constant on its own to set the horizontal alignment and leave the vertical at `image.TOP`.

```python
screen.font = font.sins
screen.pen = color.rgb(0, 0, 255)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Well hello there, world! This is a nice long message that's designed to split over several lines."
    screen.text(message, bounds, align=(image.CENTER, image.MIDDLE))

run(update)
```

## Overflow
By default text taller than `bounds` is clipped wherever it happens to fall. Pass `overflow=image.ELLIPSES` and the last line that fits is truncated with a trailing `...` instead.

```python-raw
screen.text(message, bounds, overflow=image.ELLIPSES)
```

# Glyph renderers
You can customise text to a great extent by using glyph renderers - these are little functions which make something happen at a specific point in the text, whether that is inserting an image, changing the colour, or anything else you can think of. Glyph renderers are invoked from within the text using square brackets containing the renderer's name along with any parameters it takes, such as `[pen:255,0,0]` to change the pen to red, or just `[square]` for one that takes no parameters.

To include a literal `[` in your text, write it twice: `[[`.

Markup is only read when you draw into a `rect`. Give `text()` a point instead and the brackets are drawn as written.

## Built-in glyph renderers
A couple of renderers are always available, with no setup required:

| Markup | Effect |
|---|---|
| `[pen:r,g,b]` | Sets the pen colour for the following text, e.g. `[pen:255,0,0]`. Takes up no space |
| `[sprite:name]` | Draws a sprite registered with `add_sprite(name, image)`, taking up the sprite's width |

```python
screen.font = font.sins

def update():
    screen.pen = color.rgb(0, 0, 255)
    bounds = rect(10, 10, 140, 110)
    message = "I'm written in blue... [pen:255,0,0]or am I?"
    screen.text(message, bounds)

run(update)
```

To use `[sprite:name]`, register an image against a name first. A cell pulled from a [spritesheet](/api/spritesheet.md) works, since `sprite()` hands back an ordinary `image`:

```python
screen.font = font.sins

cards = image.load("/system/assets/cards.png").spritesheet(13, 6)

# row picks the suit, column picks the rank
add_sprite("ace", cards.sprite(0, 0))     # ace of spades
add_sprite("king", cards.sprite(12, 1))   # king of hearts

def update():
    bounds = rect(10, 10, 140, 110)
    screen.text("Dealt [sprite:ace] and [sprite:king]", bounds)

run(update)
```

A sprite reserves horizontal space only, so one taller than the font overlaps the line below. Raise `line_height` to make room for it.

## Defining your own
A glyph renderer is a function defined as follows:

```python-raw
def XXXXX_glyph_renderer(image, parameters, measure):
    # contents of the glyph renderer
```

The parameters are always defined the same way, but some may not be used in your particular renderer.
- `image` - The image being drawn into.
- `parameters` - A list of the parameters passed in the markup, always as strings (e.g. `[pen:255,0,0]` gives `["255", "0", "0"]`). Convert them as needed.
- `measure` - `True` when the renderer is being asked how wide it is, `False` when it should actually draw. Layout calls it both ways, so draw nothing in the measure pass.

To find out *where* to draw, read `image.cursor`, a `vec2` holding the pen position at the point your renderer was reached.

Your renderer must **return the advance width** (how many pixels of horizontal space it takes) when `measure` is `True`, and do its drawing and return `None` otherwise.

Register it with `add_glyph(name, renderer)`, where `name` is what you'll call it by in the text. Registration is global and lasts for the life of the app; re-registering a name replaces it, and `add_glyph(name, None)` removes one.

Registering a renderer is not enough on its own: draw with a `rect`, as the example below does. A registered `[square]` drawn at an `x, y` still comes out as the literal text `[square]`.

Here's one called with `[square]`:

```python
screen.font = font.sins
screen.pen = color.rgb(255, 255, 0)

def square_glyph_renderer(image, parameters, measure):
    if measure:
        return 12

    image.shape(shape.rectangle(image.cursor.x, image.cursor.y, 12, 12))
    return None

add_glyph("square", square_glyph_renderer)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Come on, man, don't be a [square] all your life..."
    screen.text(message, bounds)

run(update)
```

This draws a 12px × 12px square in the current pen colour. `parameters` isn't used here. `image.cursor` gives the position we're 'at' in the text, which we use as the top-left of the square. When `measure` is `True` we return the width we occupy - `12`.

# Scrolling text
We've included a scrolling function to make this common activity quicker and easier.

## scroll()
This generates a closure, a function which you can call every `update()` to scroll the specified text from right to left. This closure will draw the scrolling text to a target image, and advance the scroll, as well as returning a float which denotes how far through the scroll cycle it is.

The text is always drawn scrolling between both edges of the target image. To position the scrolling text within a larger image, use `image.window()` to make a window onto that image in the right place, and pass that as your target.

### Usage
`text.scroll(text, font_face, font_size, target, speed, gap, align)`

| Parameter | Type | Description |
|---|---|---|
| `text` | `string` | The text to scroll |
| `font_face` | `font` | *Optional.* The font to use for the scrolling text. Default is `font.sins` |
| `font_size` | `int` | *Optional.* The size for the scrolling text. **Required** for vector fonts (point size); for pixel fonts it's the integer scale, defaulting to `1` |
| `target` | `image` | *Optional.* The image the scrolling text should be drawn to. Default is `screen` |
| `speed` | `int` | *Optional.* The speed at which to scroll the text, in pixels per second. Default is `25` |
| `gap` | `int` | *Optional.* The space between each repetition of the scrolling text, in pixels. `None` means the next repetition will appear as the previous one leaves the image. Default is `None` |
| `align` | `string` \| `int` | *Optional.* The vertical alignment of the text on the target. Options are `top`, `middle`, `bottom` or a y-coordinate. Default is `middle` |

```python
my_text = "Hello world! Once again, this is a long piece of text which is supposed to scroll outside its area! Whoop whoop!"

# Now we set up the scrolling text itself, very simple.
my_scroll = text.scroll(my_text)

# This window is 10px within the screen boundaries.
text_window = screen.window(10, 10, screen.width - 20, screen.height - 20)

# This scroll is set up with a few more parameters.
my_other_scroll = text.scroll(my_text, font_face=font.ark, target=text_window, gap=20, align="bottom")

def update():
    # We call the closures we made every frame.
    my_scroll()
    # For this one we're taking the return value
    # to see how far along the scroll it is.
    progress = my_other_scroll()

    # And then we'll show that number.
    screen.text(str(progress), 10, 10)

run(update)
```

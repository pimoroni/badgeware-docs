---
title: text
summary: Provides methods for advanced drawing of text to the screen.
icon: format_align_left
publish: true
---
# Introduction
While `image.text()` will provide basic functionality to draw text onto the screen, more advanced features can be found in the text class — word wrapping, alignment, inline markup and scrolling.

## A note on size
Everywhere in this article the optional `size` argument works the same way, and it depends on the kind of font you've assigned to `image.font`:

- **Vector fonts** (`.af`, loaded with `font.load()`) take a **point size** — any value you like. The default is `12`.
- **Pixel fonts** (the ROM fonts, e.g. `font.sins`) take an **integer scale** — `1` (default) is native size, `2` doubles every glyph pixel, `3` triples it, and so on.

Leaving `size` at its default (`0`) uses the font's own size. Always measure and draw with the *same* `size` so your layout matches what's rendered.

# Drawing text
In its simplest form, text can be drawn to the screen at a specific location using `image.text()`. But this has several limitations - the text will extend out of the screen area, and it does not wrap. The `text` class offers more functionality.

## draw()
This method writes text into a specified area, wrapping onto new lines when it reaches the boundary of that area. It can align each line, align the whole block vertically, and truncate overflowing text with an ellipsis. It accepts either a plain string or the output of `tokenise()`, so inline `[glyph]` markup (see [glyph renderers](#glyph-renderers)) is rendered either way.

### Usage
`text.draw(image, text, bounds, line_spacing, word_spacing, size, align, valign, ellipsis)`

| Parameter | Type | Description |
|---|---|---|
| `image` | `image` | The `image` to draw the text onto |
| `text` | `list` \| `string` | The text to draw. This can be the output of `tokenise()`, or a simple string |
| `bounds` | `rect` | *Optional.* A rectangle describing the area in which the text is drawn. Defaults to the whole image |
| `line_spacing` | `float` | *Optional.* Line height multiplier. Defaults to `1` |
| `word_spacing` | `float` | *Optional.* Space width multiplier. Defaults to `1` |
| `size` | `int` | *Optional.* Point size for a vector font (default `12`), or integer scale for a pixel font (default `1`). See [A note on size](#a-note-on-size) |
| `align` | `string` \| `int` | *Optional.* Horizontal alignment of each line: `"left"` (default), `"center"`, `"right"`, or an x offset in pixels |
| `valign` | `string` \| `int` | *Optional.* Vertical alignment of the block within `bounds`: `"top"` (default), `"middle"`, `"bottom"`, or a y offset in pixels |
| `ellipsis` | `bool` | *Optional.* When `True`, text that overflows `bounds` vertically is truncated with a trailing `"..."`. Defaults to `False` |

### Returns
A `rect` describing the bounding box that was actually drawn — handy for laying out further content beneath or beside the text.

```python
screen.font = font.sins
screen.pen = color.rgb(0, 0, 255)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Well hello there, world! This is a nice long message that's designed to split over several lines, so I'm just going to ramble on for a little while."
    text.draw(screen, message, bounds, align="center", valign="middle")

run(update)
```

## tokenise()
This method breaks down a string into its component parts, allowing the `draw()` method to draw it to the screen. If you pass a raw string straight into `draw()`, it'll actually use `tokenise()` behind the scenes before rendering the text.

Tokenising up front is worth doing when you want to reuse the same text across many frames (so it isn't re-parsed each time), or when you're supplying custom glyph renderers.

`tokenise()` returns a list of tokens.

### Usage
`text.tokenise(image, text, glyph_renderers, size)`

| Parameter | Type | Description |
|---|---|---|
| `image` | `image` | The `image` the tokenised text will be drawn onto |
| `text` | `string` | The string to be tokenised |
| `glyph_renderers` | `dict` | *Optional.* Extra glyph renderers (see below), merged on top of the built-in ones for this call |
| `size` | `int` | *Optional.* The size to measure glyphs at — point size for a vector font, integer scale for a pixel font. See [A note on size](#a-note-on-size) |

### Returns
A `list` containing the individual text tokens.

```python
screen.font = font.sins
screen.pen = color.rgb(0, 0, 255)

# tokenise once, outside update(), so the string is only parsed a single time
message = "Well hello there, world!"
tokens = text.tokenise(screen, message)

def update():
    bounds = rect(10, 10, 140, 110)
    text.draw(screen, tokens, bounds)

run(update)
```

# Glyph renderers
You can customise text to a great extent by using glyph renderers - these are little functions which make something happen at a specific point in the text, whether that is inserting an image, changing the colour, or anything else you can think of. Glyph renderers are invoked from within the text using square brackets containing the renderer's name along with any parameters it takes, such as `[pen:255,0,0]` to change the pen to red, or just `[square]` for one that takes no parameters.

To include a literal `[` in your text, write it twice: `[[`.

## Built-in glyph renderers
A couple of renderers are always available, with no setup required:

| Markup | Effect |
|---|---|
| `[pen:r,g,b]` | Sets the pen colour for the following text, e.g. `[pen:255,0,0]`. Takes up no space |
| `[sprite:name]` | Draws a sprite previously registered with `register_sprite(name, image)`, taking up the sprite's width |

Because these are built in, they work even when you pass a plain string straight to `draw()`:

```python
screen.font = font.sins

def update():
    screen.pen = color.rgb(0, 0, 255)
    bounds = rect(10, 10, 140, 110)
    message = "I'm written in blue... [pen:255,0,0]or am I?"
    text.draw(screen, message, bounds)

run(update)
```

To use `[sprite:name]`, register an image against a name first:

```python
screen.font = font.sins

heart = image.load("/system/assets/heart.png")
register_sprite("heart", heart)

def update():
    bounds = rect(10, 10, 140, 110)
    text.draw(screen, "I [sprite:heart] Badgeware!", bounds)

run(update)
```

## Defining your own
A glyph renderer is a function defined as follows:

```python-raw
def XXXXX_glyph_renderer(image, parameters, measure):
    # contents of the glyph renderer
```

The parameters are always defined the same way, but some may not be used in your particular renderer.
- `image` - The image the renderer draws onto. **When `measure` is `True` this is `None`** (nothing is being drawn, only measured), so don't touch it in the measure branch.
- `parameters` - A list of the parameters passed in the markup, always as strings (e.g. `[pen:255,0,0]` gives `["255", "0", "0"]`). Convert them as needed.
- `measure` - `True` when the renderer is being asked how wide it is, `False` when it should actually draw.

To find out *where* to draw, read `image.cursor` — a `vec2` that `draw()` sets to the current pen position just before calling your renderer.

Your renderer must **return the advance width** (how many pixels of horizontal space it takes) when `measure` is `True`, and do its drawing and return `None` otherwise.

Here's one called with `[square]`:

```python
screen.font = font.sins
screen.pen = color.rgb(255, 255, 0)

def square_glyph_renderer(image, parameters, measure):
    if measure:
        return 12

    image.shape(shape.rectangle(image.cursor.x, image.cursor.y, 12, 12))
    return None

glyph_renderers = {
    "square": square_glyph_renderer
}

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Come on, man, don't be a [square] all your life..."
    tokens = text.tokenise(screen, message, glyph_renderers)
    text.draw(screen, tokens, bounds)

run(update)
```

This draws a 12px × 12px square in the current pen colour. `parameters` isn't used here. `image.cursor` gives the position we're 'at' in the text, which we use as the top-left of the square. When `measure` is `True` we return the width we occupy - `12`.

The keys of the `glyph_renderers` dictionary are the names you call from within the text, so `square_glyph_renderer` is invoked by placing `[square]` in the string.

## Registering renderers globally
Passing a `glyph_renderers` dict to `tokenise()` adds those renderers for that call only. If you'd rather make one available everywhere - including in plain strings passed straight to `draw()` - register it once against the built-in set:

```python-raw
register_glyph_renderer("square", square_glyph_renderer)
register_sprite("heart", heart)   # for use as [sprite:heart]
```

# Scrolling text
We've included a scrolling function to make this common activity quicker and easier.

## scroll()
This generates a closure, a function which you can call every `update()` to scroll the specified text from right to left. This closure will draw the scrolling text to a target image, and advance the scroll, as well as returning a float which denotes how far through the scroll cycle it is.

The text will always be drawn scrolling between both edges of the target image, so if you want to position the scrolling text within a larger image, you'll want to use `image.window()` to make a window onto that image in the appropriate place, and use that as your target image.

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

---
title: text
summary: Provides methods for advanced drawing of text to the screen.
icon: build
publish: true
---
# Introduction
While `image.text()` will provide basic functionality to draw text onto the screen, more advanced features can be found in the text class.

# Drawing text
In its simplest form, text can be drawn to the screen at a specific location and size using `image.text()`. But this has several limitations - the text will extend out of the screen area, it does not wrap - the `text` class offers more functionality.

## draw()
This method will write text into a specified area, wrapping onto new lines if it reaches the boundary of that area. It will accept the output of `tokenise()` as its text, meaning that inline code can be executed using glyph renderers as described below.

### Usage
- `text.draw(image, text, bounds, line_spacing, word_spacing, size)`
	- `image` - The `image` to draw the text onto.
    - `text` - The text to draw. This can be the output of `tokenise()`, or a simple string.
    - `bounds` (Optional) - A `rect` describing the area in which the text is to be drawn. Defaults to None.
    - `line_spacing` (Optional) - The spacing between lines. Defaults to 1.
    - `word_spacing` (Optional) - The spacing between words. Defaults to 1.
    - `size` (Optional) - The height to render the text when using a vector font. Defaults to 24px.

### Returns
`None`.

### Example
```python
screen.font = rom_font.sins
screen.pen = color.rgb(0, 0, 255)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Well hello there, world! This is a nice long message that's designed to split over several lines, so I'm just going to ramble on for a little while."
    text.draw(screen, message, bounds)
```

## tokenise()
This method breaks down a string into its component parts, allowing the `draw()` method to draw it to the screen. If you pass a raw string straight into `draw()`, it'll actually use `tokenise()` behind the scenes before rendering the text.

`tokenise()` returns a list of tokens.

### Usage
- `text.tokenise(image, text, glyph_renderers, size)`
    - `image` - 
    - `text` - The string to be tokenised.
    - `glyph_renderers` (Optional) - a dictionary of glyph renderers (see below) to be applied to the text.
    - `size` (Optional) - the text size to render, if you're using a vector font.

### Returns
A `list` containing the individual text tokens.

### Example
```python
screen.font = rom_font.sins
screen.pen = color.rgb(0, 0, 255)

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Well hello there, world!"
    tokens = text.tokenise(screen, message)
    text.draw(screen, tokens, bounds)
```

# Glyph renderers
You can customise text to a great extent by using glyph renderers - these are essentially little functions which you define, which will make something happen at a specific point in the text string, whether that is inserting an image, changing the colour or anything else you can think of. Glyph renderers are called in the text by using square brackets containing the name of the glyph renderer along with any parameters it takes, such as `[pen:255, 0, 0]` to change the pen to red.

## Defining glyph renderers
A glyph renderer should be defined as follows:

```python-raw
def XXXXX_glyph_renderer(image, parameters, cursor, measure):
    # contents of the glyph renderer
```

These parameters are always defined the same way but some may not be used in your particular glyph renderer.
- `image` - The image the glyph renderer applies to.
- `parameters` - A list of parameters that can be passed in as part of the string given to the text tokeniser the glyph is used in.
- `cursor` - A vec2 describing the current position in the text.
- `measure` - A bool supplied when the glyph width needs to be calculated.

Within the definition of your glyph renderer, you can specify code to be executed when that point in the text is reached.

You have to create a dictionary of glyph renderers once you've created them - it's the keys of this dictionary that give you the renderer names that you call from within the text.

For example, the following changes the pen colour in the middle of drawing text:
```python
screen.font = rom_font.sins

def pen_glyph_renderer(_image, parameters, _cursor, measure):
    if measure:
        return 0

    r = int(parameters[0])
    g = int(parameters[1])
    b = int(parameters[2])
    screen.pen = color.rgb(r, g, b)
    return None

glyph_renderers = {
    "pen": pen_glyph_renderer
}

def update():
    screen.pen = color.rgb(0, 0, 255)
    bounds = rect(10, 10, 140, 110)
    message = "I'm written in blue... [pen:255,0,0]or am I?"
    tokens = text.tokenise(screen, message, glyph_renderers)
    text.draw(screen, tokens, bounds)
```
So, `pen_glyph_renderer()` is called by placing `[pen:r, g, b]` in the middle of the text, as its key in the `glyph_renderers` dictionary is `pen`.

It doesn't use the `image` or `cursor` parameters, so they have an underscore before them to discard them. Changing the colour doesn't use up any space in the text, so if `measure` is set (which happens when the software is asking for the width of this glyph), it just returns zero.

Otherwise, it takes in the list provided by `parameters`, which for this example will be a list containing 255, 0 and 0, and it changes the pen to the appropriate colour.

Here's another example, called simply with `[square]`.

```python
screen.font = rom_font.sins
screen.pen = color.rgb(255, 255, 0)

def square_glyph_renderer(image, _parameters, cursor, measure):
    if measure:
        return 12

    image.shape(shape.rectangle(cursor.x, cursor.y, 12, 12))
    return None

glyph_renderers = {
    "square": square_glyph_renderer
}

def update():
    bounds = rect(10, 10, 140, 110)
    message = "Come on, man, don't be a [square] all your life..."
    tokens = text.tokenise(screen, message, glyph_renderers)
    text.draw(screen, tokens, bounds)
```
Here you can see that this draws a 12px x 12px square in the current pen colour. This time round, `parameters` isn't used. `cursor` gives us the position we're 'at' in the text - we're using that as the coordinates of the top left of the square. If `measure` is true, we should return the width of what we're drawing, which in this case is 12.

# Scrolling text
We've included a scrolling function to make this common activity quicker and easier.

## scroll()
This generates a closure, a function which you can call every `update()` to scroll the specified text from right to left. This closure will draw the scrolling text to a target image, and advance the scroll, as well as returning a float which denotes how far through the scroll cycle it is.

The text will always be drawn scrolling between both edges of the target image, so if you want to position the scrolling text within a larger image, you'll want to use `image.window()` to make a window onto that image in the appropriate place, and use that as your target image.

### Usage
- `text.scroll(text, font_face, font_size, target, speed, gap, align)`
    - `text` - The text to scroll.
    - `font_face` (Optional) - The font to use for the scrolling text. Default is `rom_font.sins`.
    - `font_size` (Optional) - The font size if you are using a vector font. Default is `None`.
    - `target` (Optional) - the image the scrolling text should be drawn to. Default is `screen`.
    - `speed` (Optional) - The speed at which to scroll the text, in pixels per second. Default is `25`.
    - `gap` (Optional) - The space between each repetition of the scrolling text, in pixels. `None` means the next repetition will appear as the previous one leaves the image. Default is `None`.
    - `align` (Optional) - The vertical alignment of the text on the target. Options are `top`, `middle`, `bottom` or a y-coordinate. Default is `middle`.

### Returns
`None`.

### Example
```python

text = "Hello world! Once again, this is a long piece of text which is supposed to scroll outside its area! Whoop whoop!"

# Now we set up the scrolling text itself, very simple.
my_scroll = text.scroll(text)

# This window is 10px within the screen boundaries.
text_window = screen.window(10, 10, screen.width - 20, screen.height - 20)

# This scroll is set up with a few more parameters.
my_other_scroll = text.scroll(text, font_face=rom_font.ark, target=text_window, gap=20, align="bottom")

update():
    # We call the closures we made every frame.
    my_scroll()
    # For this one we're taking the return value
    # to see how far along the scroll it is.
    progress = my_other_scroll()

    # And then we'll show that number.
    screen.text(my_scroll, 10, 10)
```

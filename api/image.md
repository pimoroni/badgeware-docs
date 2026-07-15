---
title: image
summary: Provides functions for loading images, drawing shapes and text, and blitting sprites to the screen.
icon: image
publish: true
---
# Introduction
The `image` type is the core graphics primitive in Badgeware: a true colour (RGBA) pixel buffer you can draw shapes, text, and sprites onto.

The display is itself an image — a global instance called `screen` that maps to the device framebuffer, so anything you draw to `screen` appears on the badge. You can also create your own images to hold loaded artwork and sprites, or to render off-screen before compositing the result onto the display.

# Creating images

## image()
Returns an `image` with the specified width and height.

### Usage
`image(w, h)`

| Parameter | Type | Description |
|---|---|---|
| `w`, `h` | `int` | Width and height of the image to create |

### Returns
`image`

## load()
Loads an image from the specified file path and returns it as a new `image` object. To use it as a spritesheet, call [`spritesheet()`](#spritesheet) on the result.

### Usage
`image.load(path)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | Path to the image file to load |

### Returns
An `image` object the dimensions of the file.

```python
sprite = image.load("/system/assets/skull.png")

def update():
  screen.blit(sprite, vec2(10, 10))

run(update)
```

# Spritesheets

A spritesheet is a single image containing a grid of smaller images — frames of an animation, tiles for a map, or a set of icons. Packing them into one file keeps related artwork together and only needs a single load.

Turn an image into a spritesheet by calling [`spritesheet(cols, rows)`](#spritesheet) on it. Once it has a grid, [`sprite(x, y)`](#sprite) returns any cell as a lightweight view onto the sheet, ready to blit. Cells are addressed by column (`x`) and row (`y`), counting from `(0, 0)` in the top-left — column first, then row.

![A grid of sprite cells, with column numbers along the top and row numbers down the side, showing the cell at column 3 row 1 pulled out with sprite(3, 1)](/guides/assets/sprite-grid.svg)

## spritesheet()
Turns the image into a spritesheet by dividing it into a grid of `cols` × `rows` equally-sized cells, ready to pull sprites from with [`sprite()`](#sprite). Making the grid explicit this way is clearer than baking it into `load()` or the constructor.

### Usage
`.spritesheet(cols, rows)`

| Parameter | Type | Description |
|---|---|---|
| `cols` | `int` | Number of columns the image is divided into |
| `rows` | `int` | Number of rows the image is divided into |

### Returns
The image itself, so the call can be chained straight onto `load()`:

```python
deck = image.load("/system/assets/cards.png").spritesheet(13, 6)
```

## sprite()
Returns a single sprite from the image's grid as a new `image` that is a view onto the sheet. The grid is set by [`spritesheet()`](#spritesheet); a normal image with no grid behaves as a 1 × 1 sheet, so `sprite(0, 0)` is the whole image.

### Usage
`.sprite(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x` | `int` | The column of the sprite, counting from 0 |
| `y` | `int` | The row of the sprite, counting from 0 |

### Returns
An `image` viewing the requested grid cell. As it shares the sheet's pixel data, it's cheap to create — you can call `sprite()` every frame without copying any image data.

```python
# an 8x4 spritesheet of 16x16 tiles
tiles = image.load("/system/assets/tiles.png").spritesheet(8, 4)

def update():
  # draw the tile in column 2, row 1
  screen.blit(tiles.sprite(2, 1), vec2(10, 10))

run(update)
```

# Properties

| Property | Type | Description |
|---|---|---|
| `width` | `int` | Width of the image in pixels (read-only) |
| `height` | `int` | Height of the image in pixels (read-only) |
| `clip` | `rect` | Clipping rectangle — all drawing is restricted to its bounds |
| `antialias` | `int` | Antialiasing level for vector drawing. One of `image.OFF`, `image.X2`, or `image.X4` |
| `alpha` | `int` | Global alpha for drawing, 0–255 (0 = transparent, 255 = opaque) |
| `pen` | `color` \| `brush` | Colour or brush used for drawing operations |
| `font` | `pixel_font` \| `vector_font` | Font used for drawing text |

# Drawing
The drawing API provides a collection of fast, low-level primitives for rendering simple shapes directly into an image’s pixel buffer. These methods are designed for speed and simplicity, making them suitable for real-time graphics, UI elements, and procedural drawing. They round position and dimension values to the nearest pixel for speed, and are not antialiased.

All drawing operations use the currently selected brush/colour unless otherwise stated. For smooth shapes with sub-pixel positioning and antialiasing, see [Vector drawing](#vector-drawing) below.

## clear()
Fills the entire image or drawing surface with the current brush.

```python
def update():
  screen.pen = color.orange
  screen.clear()

run(update)
```

> Note: the canvas will be cleared by default each frame. You can disable this, or set the clear colour, using `badge.default_clear()`.

## get()
Returns the `color` of a single pixel.

### Usage
`.get(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` | Pixel coordinate |

### Returns
A `color` representing the pixel.

## put()
Draws a single pixel using the current brush.

### Usage
`.put(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` | Pixel coordinate |

```python
import random

def update():
  screen.pen = color.smoke

  # set a new random seed every 250ms
  random.seed(badge.ticks // 250)

  # using full coordinates
  for i in range(0, 1000):
    x = random.randint(0, 160)
    y = random.randint(0, 160)
    screen.put(x, y)

run(update)
```

## rectangle()
Draws a filled rectangle using the current brush.

### Usage
`.rectangle(x, y, w, h)` \
`.rectangle(rect)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` | Coordinates of the top-left corner |
| `w`, `h` | `int` | Width and height |
| `rect` | `rect` | A rectangle object |

```python
def update():
  # using full coordinates
  screen.pen = color.lime
  screen.rectangle(20, 30, 20, 20)

  # using a rect object
  r = rect(70, 50, 40, 40)
  screen.pen = color.red
  screen.rectangle(r)

run(update)
```

## circle()
Draws a filled circle using the current brush.

### Usage
`.circle(x, y, radius)` \
`.circle(point, radius)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` | Coordinates of the centre point |
| `point` | `vec2` | Centre point |
| `radius` | `int` | Radius in pixels |

```python
def update():
  # using full coordinates
  screen.pen = color.orange
  screen.circle(50, 60, 20)

  # or a point type
  screen.pen = color.blue
  p = vec2(110, 60)
  screen.circle(p, 20)

run(update)
```

## line()
Draws a straight line between two points.

`line` can be called in two ways: by passing a start and end `vec2` or by specifying the positions as individual values.

### Usage
`.line(x0, y0, x1, y1)` \
`.line(start, end)`

| Parameter | Type | Description |
|---|---|---|
| `x0`, `y0` | `int` | Start point of the line |
| `x1`, `y1` | `int` | End point of the line |
| `start`, `end` | `vec2` | Start and end points of the line |

```python
def update():
  # using full coordinates
  screen.pen = color.latte
  screen.line(10, 10, 100, 50)

  # or point types
  screen.pen = color.yellow
  p1 = vec2(10, 30)
  p2 = vec2(50, 100)
  screen.line(p1, p2)

run(update)
```

## triangle()
Draws a filled triangle defined by three vertices.

`triangle` can be called in two ways: by passing three `vec2` values or by specifying the positions as individual values.

### Usage
`.triangle(x0, y0, x1, y1, x2, y2)` \
`.triangle(p0, p1, p2)`

| Parameter | Type | Description |
|---|---|---|
| `x0`, `y0` | `int` | First vertex of the triangle |
| `x1`, `y1` | `int` | Second vertex of the triangle |
| `x2`, `y2` | `int` | Third vertex of the triangle |
| `p0`, `p1`, `p2` | `vec2` | Coordinates of the triangle vertices |

```python
def update():
  # using full coordinates
  screen.pen = color.red
  screen.triangle(10, 10, 80, 20, 20, 50)

  # or point types
  screen.pen = color.cyan
  p0 = vec2(110, 10)
  p1 = vec2(130, 50)
  p2 = vec2(100, 100)
  screen.triangle(p0, p1, p2)

run(update)
```

# Vector drawing
Unlike the raster primitives above, vector shapes can be positioned and dimensioned with sub-pixel accuracy and are antialiased, at a slight speed cost. A shape is created with one of the helper methods on the `shape` type (or built manually), then rendered with `shape()`.

Vector drawing uses the currently selected brush for both stroke and fill unless otherwise stated.

## shape()
Draws a vector shape (see `shape`) to the image using the current brush and antialiasing settings.

### Usage
`.shape(s)`

| Parameter | Type | Description |
|---|---|---|
| `s` | `shape` | The shape to draw |

```python
def update():
  screen.antialias = image.X4

  screen.pen = color.lime
  squircle = shape.squircle(50, 40, 20)
  screen.shape(squircle)

  screen.pen = color.orange
  star = shape.star(110, 40, 7, 10, 25)
  screen.shape(star)

  screen.pen = color.red
  arc = shape.arc(80, 70, 30, 40, 130, 260)
  screen.shape(arc)

run(update)
```

## Antialiasing
The `antialias` property sets the antialiasing level applied to vector drawing. It also applies to text drawn with vector fonts, but has no effect on the raster primitives or pixel fonts.

Compare `image.OFF`, `image.X2`, and `image.X4`:

```python
def update():
  screen.pen = color.red

  screen.antialias = image.OFF
  screen.shape(shape.circle(30, 60, 20))

  screen.antialias = image.X2
  screen.shape(shape.circle(80, 60, 20))

  screen.antialias = image.X4
  screen.shape(shape.circle(130, 60, 20))

run(update)
```

# Text
The text drawing API provides methods for rendering text to an image.

Text is positioned relative to the top-left corner of its bounding box, and all text rendering operations use the current font and brush unless otherwise stated.

## text()
Writes text to the image using the current font and brush at the specified position.

The `text()` method can be called in two forms: by passing a `vec2` that defines the position, or by specifying the position as individual `x` and `y` values.

### Usage
`.text(message, x, y, size)` \
`.text(message, p, size)`

| Parameter | Type | Description |
|---|---|---|
| `message` | `string` | The text to write |
| `x`, `y` | `int` | Position of the top-left corner of the text |
| `p` | `vec2` | Position of the top-left corner of the text |
| `size` | `int` | *Optional.* For a vector font, the text size. For a pixel font, an integer scale factor — e.g. `3` draws the font at 3× its native size. |

```python
def update():
  screen.pen = color.yellow

  # using full coordinates
  screen.text("Hello, Badgeware!", 5, 5)

run(update)
```

## measure_text()
Returns a tuple containing the width and height of the given text, when rendered using the current font.

### Usage
`.measure_text(message, size)`

| Parameter | Type | Description |
|---|---|---|
| `message` | `string` | The text to measure |
| `size` | `int` | *Optional.* The font size, if the current font is a vector font |

### Returns
A `tuple` containing x and y dimensions in pixels

```python
def update():
  screen.pen = color.yellow

  # centre the message on screen
  message = "Hello, Badgeware!"
  w, h = screen.measure_text(message)
  x = (screen.width / 2) - (w / 2)
  y = (screen.height / 2) - (h / 2)
  screen.text(message, x, y)

run(update)
```

# Filters
Filters are applied to an entire image's clipping area.

## blur()
Blurs the contents of the image.

### Usage
`.blur(radius)`

| Parameter | Type | Description |
|---|---|---|
| `radius` | `int` | The radius of the blur filter (higher = stronger) |

```python
import math

sprite = image.load("/system/assets/skull.png")

def update():
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.blur((math.sin(badge.ticks / 500) + 1) * 5)

run(update)
```

## dither()
Performs an ordered dither on the image.

```python
sprite = image.load("/system/assets/skull.png")

def update():
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.dither()

run(update)
```

## onebit()
Reduces the image to black and white.

```python
sprite = image.load("/system/assets/skull.png")

def update():
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.onebit()

run(update)
```

## monochrome()
Reduces the image to greyscale.

```python
sprite = image.load("/system/assets/skull.png")

def update():
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.monochrome()

run(update)
```

# Blitting
Functions for copying image data from one image to another. These operations are optimised for fast pixel transfer and are commonly used for drawing sprites, compositing images, and rendering pre-rendered graphics.

## blit()
Blits a source image onto this image.

Depending on the parameters provided, `blit` can:

- draw the source at 1:1 size at a specified position
- scale/stretch it into a destination rectangle
- or crop from a source rectangle and scale into a destination rectangle

### Usage
`.blit(source, x, y)` \
`.blit(source, p)` \
`.blit(source, rect)` \
`.blit(source, source_rect, dest_rect)`

| Parameter | Type | Description |
|---|---|---|
| `source` | `image` | The source image to blit |
| `x`, `y` | `int` | Coordinates of the top-left corner of the destination |
| `p` | `vec2` | Coordinates of the top-left corner of the destination |
| `rect` | `rect` | Destination rectangle to blit into — the source image is scaled to fit |
| `source_rect` | `rect` | Source rectangle to blit from (crop region) |
| `dest_rect` | `rect` | Destination rectangle to blit into — if a different size to `source_rect`, the blit is scaled |

> Note: If the width and height of the destination rectangle are negative then the blit will flip vertically and/or horizontally!

```python
sprite = image.load("/system/assets/skull.png")

def update():
  # 1:1 blit
  screen.blit(sprite, vec2(10, 10))

  # scale sprite to 64x64 and flip it horizontally
  screen.blit(sprite, rect(60, 10, -64, 64))

  # crop a 16x16 tile and scale it up to 32x32
  screen.blit(sprite, rect(0, 0, 16, 16), rect(10, 60, 32, 32))

run(update)
```

## blit_vspan() / blit_hspan()
Blit (copy) a single span from a source image into this image, sampling along the way using UV texture coordinates. These are low-level helpers mainly used for scaled or warped texture rendering, where an image is drawn one line at a time — `blit_vspan()` draws a vertical span (column), `blit_hspan()` a horizontal one (row).

### Usage
`.blit_vspan(source, x, y, c, u0, v0, u1, v1)` \
`.blit_hspan(source, x, y, c, u0, v0, u1, v1)`

| Parameter | Type | Description |
|---|---|---|
| `source` | `image` | The source image to blit |
| `x`, `y` | `int` | Coordinates of the top-left corner of the destination |
| `c` | `int` | The length of the span (number of pixels) to draw |
| `u0`, `v0` | `float` | The start UV coordinate for sampling |
| `u1`, `v1` | `float` | The end UV coordinate for sampling |

UV coordinates are expressed in the range 0..1 across the width/height of the source image.

For example:
- u = 0.0 is the left edge
- u = 1.0 is the right edge
- v = 0.0 is the top edge
- v = 1.0 is the bottom edge

UV coordinates may fall outside the 0..1 range. If they do, the source texture will wrap around automatically, making this useful for tiled textures or repeating patterns.

```python
import math

sprite = image.load("/system/assets/skull.png")

def update():

  for i in range(160):
    # create a sine wave offset for drawing
    o = abs(math.sin((badge.ticks + i * 5) / 500) * 30) + 2

    # calculate the u coordinate to sample from
    u = (i + (badge.ticks / 50)) / sprite.width

    # blit the span!
    screen.blit_vspan(sprite, i, 60 - o, 2 * o, u, 0, u, 1)

run(update)
```

# Other

## window()
Returns an `image` which is a view onto a rectangular subsection of the image.

The returned image shares its underlying data with the original image. All drawing operations performed on the window are clipped to the specified area, and the window’s origin `(0, 0)` is relative to its top-left corner, not the original image.

### Usage
`.window(x, y, w, h)` \
`.window(rect)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` | Coordinates of the top-left corner |
| `w`, `h` | `int` | Width and height of the window |
| `rect` | `rect` | A rectangle defining the position and size of the window |

### Returns
An `image` object representing the contents of the window.

## raw
A bytearray that references the start of the image’s backing buffer (advanced/unsafe). Don’t write past the end! (for experts only!)

### Format

- Pixels are stored as 4 bytes per pixel: R, G, B, A
- Values are premultiplied alpha (i.e. R/G/B have already been multiplied by A)

> Note: Accessing pixels via the `raw` buffer from MicroPython can be slow. If you need per-pixel work, consider MicroPython’s @micropython.viper or @micropython.native decorators for a substantial speed boost. 🚀

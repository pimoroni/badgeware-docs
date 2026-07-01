---
title: image
summary: Provides functions for loading images, drawing shapes and text, and blitting sprites to the screen.
icon: image
publish: true
---
# Introduction
The `image` type is the core graphics primitive in Badgeware. Images are true colour (RGBA) pixel buffers that support drawing shapes, text, and blitting sprites.

A global image instance called `screen` represents the device framebuffer. All rendering to the display is done by drawing to `screen` — whether using primitives like `screen.circle()`, rendering text with `screen.text()`, or compositing sprites with `screen.blit()`.

# Creating images

## image()
Returns an `image` with the specified width and height. A fresh buffer is allocated for you. Advanced users can wrap an existing buffer instead by passing it as the third argument — this is how `screen` is created around the display framebuffer.

### Usage
- `image_name = image(w, h)`
    - `w, h`: Width and height of the image to create.
- `image_name = image(w, h, buffer)`
    - `buffer`: An existing buffer (for example a `memoryview`) to wrap instead of allocating a new one.

### Returns
`image`

## load()
Loads a PNG or JPEG image and returns it as a new `image` object. The source can be a file path or a buffer of image data already in memory (for example bytes downloaded over WiFi).

### Usage
- `image_name = image.load(path)`
    - `path`: Path to the image file to load.
- `image_name = image.load(data)`
    - `data`: A buffer (`bytes`/`bytearray`) containing PNG or JPEG data.

### Returns
An `image` object the dimensions of the file.

### Example
```python
sprite = image.load("/system/assets/skull.png")

while True:
  screen.blit(sprite, vec2(10, 10))

  badge.update()
```

## load_into()
Loads a PNG or JPEG into an **existing** image buffer, in place, reusing its memory. This is handy when you want to swap the contents of an image without allocating a new one each time.

### Usage
- `image_name.load_into(path_or_data)`
    - `path_or_data`: A file path, or a buffer of PNG/JPEG data.

### Returns
`None`

# Properties

## width
The width of the image, measured in pixels. This property is read-only and returns an integer value.

## height
The height of the image, measured in pixels. This property is read-only and returns an integer value.

## clip
The current clipping rectangle for this image. Once set, all subsequent drawing operations are clipped to the bounds of the rectangle. This property is of type `rect`.

## antialias
The current antialiasing level for vector drawing operations performed on this image. Valid values are `image.OFF`, `image.X2`, and `image.X4`.

```python
while True:
  screen.pen = color.red

  screen.antialias = image.OFF
  screen.shape(shape.circle(30, 60, 20))

  screen.antialias = image.X2
  screen.shape(shape.circle(80, 60, 20))

  screen.antialias = image.X4
  screen.shape(shape.circle(130, 60, 20))

  badge.update()
```

## fill_rule
The winding rule used when filling vector shapes with overlapping or self-intersecting contours. Valid values are `image.NON_ZERO` (the default) and `image.EVEN_ODD`. The even-odd rule is what creates a "hole" where two contours overlap, which is how `shape.custom()` cuts holes.

## has_palette
Read-only. `True` if this image is palettised (stores palette indices rather than full RGBA pixels), otherwise `False`.

## alpha
A global alpha blending value used for all drawing operations. When set on an image (or the screen), future drawing operations will be alpha blended using this value.

Valid values are 0–255, where 0 is fully transparent and 255 is fully opaque.

```python
import math

sprite = image.load("/system/assets/skull.png")

while True:
  # set global alpha for drawing operations to the screen
  screen.alpha = 127

  # draw ten ghostly (ghastly?!) skulls
  for i in range(0, 10):
    # swirling animation
    step = (badge.ticks + i * 250) / 500
    x = math.sin(step) * (i * 5)
    y = math.cos(step) * (i * 5)

    # centre on screen
    x += screen.width / 2 - sprite.width / 2
    y += screen.height / 2 - sprite.height / 2

    # blit the sprite
    screen.blit(sprite, x, y)

  badge.update()
```

## pen
The color or brush used for drawing operations. This can be set to a `brush` or `color` object.

```python
while True:
  screen.pen = color.taupe
  screen.circle(40, 60, 30)

  screen.pen = color.brown
  screen.circle(80, 60, 30)

  screen.pen = color.grape
  screen.circle(120, 60, 30)

  badge.update()
```

## font
The font used for drawing text. This can be either a `pixel_font` or a `vector_font`.

```python
import math

# load a built in font - see pixel_font for list
screen.font = rom_font.nope

while True:
  # use width of the text to centre on the screen
  w, _ = screen.measure_text("hey badgeware!")
  x = (screen.width / 2) - (w / 2)

  # create a side to side bounce offset
  x += math.sin(badge.ticks / 250) * 20

  # draw the text
  screen.text("hey badgeware!", x, 55)

  badge.update()
```

> Note: Badgeware comes with thirty pre-loaded fonts, check out the `pixel_font` article for a full list!

# Drawing
The drawing API provides a collection of fast, low-level primitives for rendering simple shapes directly into an image’s pixel buffer. These methods are designed for speed and simplicity, making them suitable for real-time graphics, UI elements, and procedural drawing. These methods round position and dimension values to the nearest pixel for speed.

You can also render vector shapes using the `shape()` method. Vector shapes support sub-pixel positioning. Vector drawing supports antialiasing, controlled by the current antialiasing setting, and uses the currently selected brush for stroke and fill operations unless otherwise stated.

All drawing operations use the currently selected brush/colour unless otherwise stated.

## clear()
Fills the entire image or drawing surface with the current brush.

### Example

```python
while True:
  screen.pen = color.orange
  screen.clear()

  badge.update()
```

> Note: the canvas will be cleared by default each frame. You can disable this, or set the clear colour, using `badge.default_clear()`.

## get()
Returns the `color` of a single pixel.

### Usage
- `image_name.get(x, y)`
    - `x, y` — Pixel coordinate

### Returns
A `color` representing the pixel.

## put()
Draws a single pixel using the current brush.

### Usage
- `image_name.put(x, y)`
    - `x, y` — Pixel coordinate

### Returns
`None`

### Example
```python
import random

while True:
  screen.pen = color.smoke

  # set a new random seed every 250ms
  random.seed(badge.ticks // 250)

  # using full coordinates
  for i in range(0, 1000):
    x = random.randint(0, 160)
    y = random.randint(0, 160)
    screen.put(x, y)

  badge.update()
```

## rectangle()
Draws a filled rectangle using the current brush.

### Usage
- `image_name.rectangle(x, y, w, h)`
    - `x, y` — Coordinates of the top-left corner
    - `w, h` — Width and height
- `image_name.rectangle(rect)`
    - `rect` - A `rect` object

### Returns
`None`

### Example

```python
while True:
  # using full coordinates
  screen.pen = color.lime
  screen.rectangle(20, 30, 20, 20)

  # using a rect object
  r = rect(70, 50, 40, 40)
  screen.pen = color.red
  screen.rectangle(r)

  badge.update()
```

## circle()
Draws a filled circle using the current brush.

### Usage
- `image_name.circle(point, radius)`
  - `point` — A `vec2` object containing the centre point
  - `radius` - Radius in pixels
- `image_name.circle(x, y, radius)`
  - `x, y` — Coordinates of the centre point
  - `radius` - Radius in pixels

### Returns
`None`

### Example
```python
while True:
  # using full coordinates
  screen.pen = color.orange
  screen.circle(50, 60, 20)

  # or a point type
  screen.pen = color.blue
  p = vec2(110, 60)
  screen.circle(p, 20)

  badge.update()
```

## line()
Draws a straight line between two points.

`line` can be called in two ways: by passing a start and end `vec2` or by specifying the positions as individual values.

### Usage
- `image_name.line(start, end)`
    - `start, end` — Start and end points (`vec2`) of the line
- `image_name.line(x0, y0, x1, y1)`
    - `x0, y0` — Start point of the line
    - `x1, y1` — End point of the line

### Returns
`None`

### Example
```python
while True:
  # using full coordinates
  screen.pen = color.latte
  screen.line(10, 10, 100, 50)

  # or point types
  screen.pen = color.yellow
  p1 = vec2(10, 30)
  p2 = vec2(50, 100)
  screen.line(p1, p2)

  badge.update()
```

## triangle()
Draws a filled triangle defined by three vertices.

`triangle` can be called in two ways: by passing three `vec2` values or by specifying the positions as individual values.

### Usage
- `image_name.triangle(p0, p1, p2)`
    - `p0, p1, p2` — Coordinates of the triangle vertices
- `image_name.triangle(x0, y0, x1, y1, x2, y2)`
    - `x0, y0` — First vertex of the triangle
    - `x1, y1` — Second vertex of the triangle
    - `x2, y2` — Third vertex of the triangle

### Returns
`None`

### Example
```python
while True:
  # using full coordinates
  screen.pen = color.red
  screen.triangle(10, 10, 80, 20, 20, 50)

  # or point types
  screen.pen = color.cyan
  p0 = vec2(110, 10)
  p1 = vec2(130, 50)
  p2 = vec2(100, 100)
  screen.triangle(p0, p1, p2)

  badge.update()
```

## shape()
Draws a vector shape (see `shape`) to the image using the current brush and antialiasing settings.

Vector shapes are created using one of the predefined helper methods on the shape type, or by constructing your own custom shapes manually. Unlike the raster drawing above, vector shapes can be dimensioned and positioned with subpixel accuracy at a slight speed cost.

### Usage
- `image_name.shape(s)`
    - `s`: The shape to draw, or a list of shapes to draw with the current pen.

### Returns
`None`

### Example
```python
while True:
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

  badge.update()
```

## shapes()
Draws a batch of shapes in one call, each with its own colour or brush. This is faster than a Python loop of `shape()` calls when you have many shapes, because the iteration happens in native code.

Each entry in the list is either a `shape` (drawn with the current pen) or a `(shape, brush_or_color)` tuple (drawn with the supplied brush/colour).

### Usage
- `image_name.shapes(entries)`
    - `entries`: A list of shapes, or `(shape, brush/color)` tuples.

### Returns
`None`

### Example
```python
while True:
  entries = [
    (shape.circle(50, 60, 25), color.red),
    (shape.circle(80, 60, 25), color.green),
    (shape.circle(110, 60, 25), color.blue),
  ]
  screen.shapes(entries)

  badge.update()
```

# Text
The text drawing API provides methods for rendering text to an image.

Text is positioned relative to the top-left corner of its bounding box, and all text rendering operations use the current font and brush unless otherwise stated.

## text()
Writes text to the image using the current font and brush at the specified position.

The `text()` method can be called in two forms: by passing a `vec2` that defines the position, or by specifying the position as individual `x` and `y` values.

### Usage
- `image_name.text(message, p, size)`
    - `message`: The text to write
    - `p`: Position of the top-left corner of the text as a `vec2`
    - `size` (Optional) - the size of the text for vector fonts. Using this parameter with pixel fonts will cause an error.
- `image_name.text(message, x, y, size)`
    - `message`: The text to write
    - `x, y`: Position of the top-left corner of the text
    - `size` (Optional) - the size of the text for vector fonts. Using this parameter with pixel fonts will cause an error.

### Returns
`None`

### Example
```python
while True:
  screen.pen = color.yellow

  # using full coordinates
  screen.text("Hello, Badgeware!", 5, 5)

  badge.update()
```

## measure_text()
Returns a tuple containing the width and height of the given text, when rendered using the current font.

### Usage
- `image_name.measure_text(message, size)`
    - `message`: The text to measure
    - `size` (Optional): The font size, if the current font is a vector font.

### Returns
A `tuple` containing x and y dimensions in pixels

### Example
```python
while True:
  screen.pen = color.yellow

  # centre the message on screen
  message = "Hello, Badgeware!"
  w, h = screen.measure_text(message)
  x = (screen.width / 2) - (w / 2)
  y = (screen.height / 2) - (h / 2)
  screen.text(message, x, y)

  badge.update()
```

# Filters
Filters are applied to an entire image's clipping area.

## blur()
Blurs the contents of the image.

### Usage
- `image_name.blur(radius)`
    - `radius`: The radius of the blur filter (higher = stronger)

### Returns
`None`

### Example
```python
import math

sprite = image.load("/system/assets/skull.png")

while True:
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.blur((math.sin(badge.ticks / 500) + 1) * 5)

  badge.update()
```

## dither()
Performs an ordered dither on the image.

### Example
```python
sprite = image.load("/system/assets/skull.png")

while True:
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.dither()

  badge.update()
```

## onebit()
Reduces the image to black and white.

### Example
```python
sprite = image.load("/system/assets/skull.png")

while True:
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.onebit()

  badge.update()
```

## monochrome()
Reduces the image to greyscale.

### Example
```python
sprite = image.load("/system/assets/skull.png")

while True:
  screen.circle(80, 60, 20)
  screen.blit(sprite, vec2(40, 50))
  screen.monochrome()

  badge.update()
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
- `image_name.blit(source, x, y)`
    - `source`: The source `image` to blit
    - `x, y`: Coordinates of the top-left corner of the destination
- `image_name.blit(source, p)`
    - `source`: The source `image` to blit
    - `p`: `vec2` containing the coordinates of the top-left corner of the destination
- `image_name.blit(source, rect, filter)`
    - `source`: The source `image` to blit
    - `rect`: Destination rectangle to blit into - the source image is scaled to fit rect
    - `filter` (Optional): The texture filter used when scaling. Defaults to `image.NEAREST`.
- `image_name.blit(source, source_rect, dest_rect, filter)`
    - `source`: The source `image` to blit
    - `source_rect`: Source rectangle to blit from (crop region)
    - `dest_rect`: Destination rectangle to blit into - if dest_rect is a different size to source_rect, the blit is scaled
    - `filter` (Optional): The texture filter used when scaling. Defaults to `image.NEAREST`.

> Note: When a blit is scaled you can choose how it's sampled with the `filter` argument: `image.NEAREST` (fastest, blocky), `image.BILINEAR` (smooth) or `image.BICUBIC` (highest quality). The point and `vec2` forms always copy 1:1, so they don't take a filter.

> Note: If the width and height of the destination rectangle are negative then the blit will flip vertically and/or horizontally!

### Returns
`None`

### Example
```python
sprite = image.load("/system/assets/skull.png")

while True:
  # 1:1 blit
  screen.blit(sprite, vec2(10, 10))

  # scale sprite to 64x64 and flip it horizontally
  screen.blit(sprite, rect(60, 10, -64, 64))

  # crop a 16x16 tile and scale it up to 32x32
  screen.blit(sprite, rect(0, 0, 16, 16), rect(10, 60, 32, 32))

  badge.update()
```

## blit_vspan()
Blit (copy) a vertical span from source into this image. This is a low-level helper mainly used for scaled or warped texture rendering, where an image is drawn one column at a time.

The span is sampled from the source image using UV texture coordinates.

### Usage
- `image_name.blit_vspan(source, x, y, c, u0, v0, u1, v1)`
    - `source`: The source `image` to blit
    - `x, y`: Coordinates of the top-left corner of the destination
    - `c`: The length of the span (number of pixels) to draw
    - `u0`, `v0`: The start UV coordinate for sampling.
    - `u1`, `v1`: The end UV coordinate for sampling.

UV coordinates are expressed in the range 0..1 across the width/height of the source image.

For example:
- u = 0.0 is the left edge
- u = 1.0 is the right edge
- v = 0.0 is the top edge
- v = 1.0 is the bottom edge

UV coordinates may fall outside the 0..1 range. If they do, the source texture will wrap around automatically, making this useful for tiled textures or repeating patterns.

### Returns
`None`

### Example
```python
import math

sprite = image.load("/system/assets/skull.png")

while True:
  for i in range(160):
    # create a sine wave offset for drawing
    o = abs(math.sin((badge.ticks + i * 5) / 500) * 30) + 2

    # calculate the u coordinate to sample from
    u = (i + (badge.ticks / 50)) / sprite.width

    # blit the span!
    screen.blit_vspan(sprite, i, 60 - o, 2 * o, u, 0, u, 1)

  badge.update()
```

## blit_hspan()
Functionally identical to `blit_vspan()`, but renders a horizontal span of pixels instead of a vertical one.

See `blit_vspan()` above for full parameter and coordinate details.

# Other

## window()
Returns an `image` which is a view onto a rectangular subsection of the image.

The returned image shares its underlying data with the original image. All drawing operations performed on the window are clipped to the specified area, and the window’s origin `(0, 0)` is relative to its top-left corner, not the original image.

### Usage
- `window_name = image_name.window(r)`
    - `r` — A `rect` defining the position and size of the window
- `window_name = image.window(x, y, w, h)`
    - `x, y` — Coordinates of the top-left corner
    - `w, h` — Width and height of the window

### Returns
An `image` object representing the contents of the window.

## batch()
Runs a list of draw commands in a single native loop, avoiding the per-call overhead of MicroPython. Each command is a `(method_name, *args)` tuple, where `method_name` is the name of an `image` drawing method such as `"circle"` or `"rectangle"`.

This is an advanced optimisation — for most drawing you can just call the methods directly.

### Usage
- `image_name.batch(commands)`
    - `commands`: A list of `(method_name, *args)` tuples.

### Returns
`None`

## raw
A bytearray that references the start of the image’s backing buffer (advanced/unsafe). Don’t write past the end! (for experts only!)

### Format

- Pixels are stored as 4 bytes per pixel: R, G, B, A
- Values are premultiplied alpha (i.e. R/G/B have already been multiplied by A)

> Note: Accessing pixels via the `raw` buffer from MicroPython can be slow. If you need per-pixel work, consider MicroPython’s @micropython.viper or @micropython.native decorators for a substantial speed boost. 🚀

# Reference

## Constructor
```python-raw
image(w: int, h: int) -> image
image(w: int, h: int, buffer) -> image
```

## Constants
```python-raw
image.OFF   image.X2   image.X4                # anti-aliasing
image.NON_ZERO   image.EVEN_ODD                # fill rule
image.NEAREST   image.BILINEAR   image.BICUBIC # texture filter
```

## Properties
```python-raw
alpha: int
antialias: image.OFF | image.X2 | image.X4
clip: rect
fill_rule: image.NON_ZERO | image.EVEN_ODD
font: pixel_font | font
has_palette: bool
height: int
pen: color | brush
raw: bytearray
width: int
```

## Static Methods
```python-raw
image.load(path: string) -> image
image.load(data: buffer) -> image
```

## Methods
```python-raw
image.batch(commands: list) -> None
image.blit(source: image, x: int, y: int) -> None
image.blit(source: image, p: vec2) -> None
image.blit(source: image, dst: rect, filter: int=image.NEAREST) -> None
image.blit(source: image, source_rect: rect, dest_rect: rect, filter: int=image.NEAREST) -> None
image.blit_hspan(source: image, p: vec2, c: int, uv0: vec2, uv1: vec2, filter: int=image.NEAREST) -> None
image.blit_vspan(source: image, p: vec2, c: int, uv0: vec2, uv1: vec2, filter: int=image.NEAREST) -> None
image.blur(radius: int|float) -> None
image.circle(point: vec2, radius: int|float) -> None
image.circle(x: int|float, y: int|float, radius: int|float) -> None
image.clear() -> None
image.dither() -> None
image.get(p: vec2) -> color
image.get(x: int|float, y: int|float) -> color
image.line(start: vec2, end: vec2) -> None
image.line(x0: int|float, y0: int|float, x1: int|float, y1: int|float) -> None
image.load_into(path_or_data) -> None
image.measure_text(message: string, size: int|float=0) -> tuple
image.monochrome() -> None
image.onebit() -> None
image.put(p: vec2) -> None
image.put(x: int|float, y: int|float) -> None
image.rectangle(x: int|float, y: int|float, w: int|float, h: int|float) -> None
image.rectangle(rect: rect) -> None
image.shape(s: shape | list) -> None
image.shapes(entries: list) -> None
image.text(message: string, p: vec2, size: int|float=12) -> None
image.text(message: string, x: int|float, y: int|float, size: int|float=12) -> None
image.triangle(a: vec2, b: vec2, c: vec2) -> None
image.triangle(x0: int|float, y0: int|float, x1: int|float, y1: int|float, x2: int|float, y2: int|float) -> None
image.window(r: rect) -> image
image.window(x: int|float, y: int|float, w: int|float, h: int|float) -> image
```
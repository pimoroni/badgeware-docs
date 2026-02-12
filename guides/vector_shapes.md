---
title: Vector Shapes
summary: Vector shapes make it easy to build and edit detailed geometry, then reuse and animate it smoothly. Ideal for UI elements, animations, and generative art.
icon: shapes
---

# Introduction
Vector shapes let you build and manipulate complex geometry, including multi-path forms and self-intersecting polygons. Once defined, a shape can be transformed, reused, and animated efficiently. They are a great fit for user-interface elements, animations, and generative art.

Unlike raster drawing operations, vector shapes can be antialiased, producing smooth, high-quality edges and curves.

# Custom shapes

To define a custom shape, call the `shape.custom` static method with one or more lists of points. Each list represents a single path within the shape, allowing you to create complex geometry, including holes or self-intersecting outlines.

Each point must be provided as a two-value tuple containing the point’s x and y coordinates.

```python {len=6}
import math

screen.antialias = image.X4

def update():
  # create a flower shape
  path1 = [] # outline of the flower petals
  path2 = [] # outline of the flower centre
  for i in range(0, 360, 5):
    # create the petal shape
    scale = (math.sin(((i + io.ticks / 50)) * 5 * math.pi / 180) * 10) + 30
    x = math.sin(i * math.pi / 180) * scale
    y = math.cos(i * math.pi / 180) * scale
    path1.append(vec2(x + 80, y + 60))

    # create the centre
    x = math.sin(i * math.pi / 180) * 10
    y = math.cos(i * math.pi / 180) * 10
    path2.append(vec2(x + 80, y + 60))

  # construct a custom shape from the two paths
  custom_shape = shape.custom(path1, path2)

  # draw the shape to the display
  screen.pen = color.orange
  screen.shape(custom_shape)
```

> Creating shapes can be an expensive process, if possible define the shape once and keep a reference to it for future use.

# Primitives

For common shapes, a set of convenience methods is available. These methods let you create standard geometry by specifying only their key parameters (for example, the radius for a circle). Each method constructs the corresponding shape and returns it.

```python
screen.antialias = image.X4

def update():
  # draw the circle
  screen.pen = color.red
  circle = shape.circle(30, 30, 20)
  screen.shape(circle)

  screen.pen = color.lime
  pie = shape.pie(80, 30, 20, 90, 270)
  screen.shape(pie)

  screen.pen = color.orange
  line = shape.line(115, 15, 145, 45, 4)
  screen.shape(line)

  screen.pen = color.cyan
  polygon = shape.regular_polygon(30, 90, 22, 7)
  screen.shape(polygon)

  screen.pen = color.yellow
  squircle = shape.squircle(80, 90, 20)
  screen.shape(squircle)

  screen.pen = color.latte
  arc = shape.arc(130, 90, 10, 20, 90, 270)
  screen.shape(arc)
```

See the built in primitives for a full list of supported shapes.



To learn more about shapes [click here for full documentation of the `shapes` module](api/modules/shapes.md).

# Transforming vector shapes


Shapes can also be given a transformation matrix to adjust their scale, rotation, and skew - this is very useful for creating smooth animations. [Click here for full documentation of the `Matrix` class](api/mat3.md).

```python {len=3}
import math

def update():
  # create a rectangle
  rectangle = shapes.rectangle(-20, -20, 40, 40)

  offset = math.sin(io.ticks / 1000) * 50
  # transform and draw the transformed rectangle
  rectangle.transform = Matrix().translate(80 + offset, 60).rotate(offset)
  screen.draw(rectangle)
```

To learn more about transformations [click here for the Transforms guide](guides/transforms.md).

# Stroking vector shapes
The shape-creation functions produce closed paths with a single outline. To draw a “thick” version of a shape, you need to stroke that outline, expanding it outward and inward by a chosen width. This effectively generates two offset copies of the original path, one larger and one smaller, which are then combined to form a new stroked shape.

```python {len=5}
import math

def update():
  # create a circle with a radius of ten pixels
  squircle = shapes.squircle(80, 60, 40, 4)

  # create a stroked copy of the circle two pixels thick
  thickness = (math.sin(io.ticks / 1000) * 5) + 6
  squircle.stroke(thickness)

  screen.draw(squircle)
```

# Styling
Shapes are drawn using the currently assigned brush.

# Antialiasing
Antialiasing is a technique that smooths out the jagged, stair-step edges that appear when drawing lines or curves on a pixel grid. It works by gently blending the edge into the background, making shapes look cleaner and more natural without harsh pixelation. It’s a small touch that makes graphics feel much smoother and easier on the eyes.

Vector shapes and text both support antialiasing which can be enabled and disabled at any time:

```python
# 4x4 sample grid for antialiasing, best quality, slowest
screen.antialias = Image.X4

# 2x2 sample grid for antialiasing, good quality, faster
screen.antialias = Image.X2

# disable antialiasing
screen.antialias = Image.OFF
```

> Antialiasing can be pretty expensive so you should reserve its use for places where it really makes a difference!

# Built-in primitives

Currently supported shapes are:

## Rectangle
A rectangle with top left corner at `x, y` and size `w x h`.
```python
shapes.rectangle(x, y, w, h)
```

## Circle
A circle of radius `r` centered at point `x, y`.
```python
circle(x, y, r)
```

## Arc
An arc that spans the angles `t1` and to `t2` (theta, in degrees) with a radius of `r` centered at point `x, y`.
```python
arc(x, y, r, t1, t2)
```

## Pie
A pie slice (think pacman) that spans the angles `t1` and to `t2` (theta, in degrees) with a radius of `r` centered at point `x, y`.
```python
pie(x, y, r, t1, t2)
```

## Line
A line starting at `x1, y1` and ending at `x2, y2` with thickness `t`.
```python
line(x1, y1, x2, y2, t)
```

## Rounded Rectangle
A rectangle with rounded corners with top left corner at `x, y` and size `w x h`. corner radii are defined by `r1` (top left) and going clockwise.
If `r2, r3, r4` are not specified then `r1` is used for all corners.
```python
rounded_rectangle(x, y, w, h, r1[, r2, r3, r4])
```

## Regular Polygon
A regular polygon of radius `r` centered at point `x, y` with `s` sides.
```python
regular_polygon(x, y, r, s)
```

## Squircle
A squircle of radius `r` centered at point `x, y`, `n` defines how rounded the end shape is.
```python
squircle(x, y, r, n=4)
```

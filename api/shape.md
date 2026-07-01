---
title: shape
summary: Easily create primitive vector shapes as well as custom shapes, then modify them to build more complex vector graphics.
icon: shapes
publish: true
---

# Introduction
Unlike pixel-based graphics, vector shapes are described using geometry rather than fixed pixels. This allows them to be scaled, transformed, and positioned with much greater precision.

Shapes are defined by paths — a collection of points that make up the outline. Even with this simple representation, vector shapes are extremely useful for drawing clean UI elements, icons, and geometric artwork. All of the methods below all create the same type, the `shape` type, but they create different sets of points to go within it.

Because shapes are resolution-independent, they can be drawn at different sizes without becoming blocky or distorted. When combined with antialiasing, they allow you to create crisp, smooth graphics that would be difficult to achieve with bitmap drawing alone.

# Primitives
The following static methods all return new `shape` objects.

## circle()
Creates a new `shape` representing a circle.

### Usage
- `shape_name = shape.circle(centre, radius)`
    - `centre`: Position of the centre point (`vec2`)
    - `radius`: Radius of the circle in pixels
- `shape_name = shape.circle(x, y, radius)`
    - `x, y`: Position of the centre point
    - `radius`: Radius of the circle in pixels

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  screen.pen = color.taupe
  circle = shape.circle(80, 60, 40)
  screen.shape(circle)

  badge.update()
```

## rectangle()
Creates a new `shape` representing a rectangle.

### Usage
- `shape_name = shape.rectangle(x, y, width, height)`
    - `x, y`: Coordinates of the top-left corner
    - `width, height`: Width and height of the rectangle

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  screen.pen = color.blue
  rectangle = shape.rectangle(30, 30, 100, 60)
  screen.shape(rectangle)

  badge.update()
```

## regular_polygon()
Creates a new shape representing a regular polygon — a closed shape with evenly spaced sides and equal angles (for example: triangles, squares, pentagons, and so on).

### Usage
- `shape_name = shape.regular_polygon(x, y, radius, sides)`
    - `x, y`: Position of the centre point
    - `radius`: Radius of the polygon (distance from the centre to each corner)
    - `sides`: Number of sides (must be 3 or greater)

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  sides = ((badge.ticks // 500) % 10) + 3

  polygon = shape.regular_polygon(80, 60, 40, sides)
  screen.pen = color.red
  screen.shape(polygon)

  screen.pen = color.white
  screen.text(f"{sides} sides", 5, 5)

  badge.update()
```

## rounded_rectangle()
Creates a new `shape` representing a rectangle with rounded corners.
Rounded rectangles are especially useful for modern UI elements such as buttons, panels, dialog boxes, and badges.
You can specify either a single corner radius for all corners, or provide individual radii to create asymmetric shapes.

### Usage
- `shape_name = shape.rounded_rectangle(x, y, width, height, radius)`
    - `x, y`: Coordinates of the top-left corner
    - `width, height`: Width and height
    - `radius`: Corner radius applied to all corners
- `shape_name = shape.rounded_rectangle(x, y, width, height, r1, r2, r3, r4)`
    - `x, y`: Coordinates of the top-left corner
    - `width, height`: Width and height
    - `r1, r2, r3, r4`: Corner radii (top-left, top-right, bottom-right, bottom-left)

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  screen.pen = color.yellow
  rounded_rectangle = shape.rounded_rectangle(15, 10, 60, 60, 10)
  screen.shape(rounded_rectangle)

  screen.pen = color.navy
  rounded_rectangle = shape.rounded_rectangle(85, 50, 60, 60, 0, 20, 0, 20)
  screen.shape(rounded_rectangle)

  badge.update()
```

## ellipse()
Creates a new `shape` representing an ellipse, with independent horizontal and vertical radii.

### Usage
- `shape_name = shape.ellipse(centre, rx, ry)`
    - `centre`: Position of the centre point (`vec2`)
    - `rx`: Horizontal radius in pixels
    - `ry`: Vertical radius in pixels
- `shape_name = shape.ellipse(x, y, rx, ry)`
    - `x, y`: Position of the centre point
    - `rx, ry`: Horizontal and vertical radii in pixels

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  screen.pen = color.grape
  ellipse = shape.ellipse(80, 60, 60, 30)
  screen.shape(ellipse)

  badge.update()
```

## squircle
Creates a new shape representing a squircle — a smooth shape that sits somewhere between a square and a circle.

Squircles are useful for UI elements like icons and buttons, producing corners that feel softer and more natural than a standard rounded rectangle.

The optional squareness factor controls the shape: lower values are more circular, higher values more square-like.

### Usage
- `shape_name = shape.squircle(x, y, s[, n])`
    - `x, y`: Position of the centre point
    - `s`: Size of the squircle
    - `n`: Optional squareness factor (default 4)

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  screen.pen = color.orange
  squircle = shape.squircle(80, 60, 40)
  screen.shape(squircle)

  badge.update()
```

## arc
Creates a new shape representing an arc segment.
Arcs are useful for gauges, progress indicators, rings, and other circular UI elements. The arc is defined by an inner and outer radius, producing a curved band between two angles.
Angles are measured in degrees, where 0° points straight up, and values increase clockwise.

### Usage
- `shape_name = shape.arc(x, y, inner, outer, from, to)`
    - `x, y`: Position of the centre point
    - `inner`: Inner radius
    - `outer`: Outer radius
    - `from`: Start angle (degrees)
    - `to`: End angle (degrees)

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  angle = badge.ticks / 10
  arc = shape.arc(80, 60, 30, 40, angle + 30, angle + 150)
  screen.pen = color.cyan
  screen.shape(arc)

  badge.update()
```

## pie
Creates a new shape representing a pie slice (think Pacman).
The slice is defined by an inner and outer radius.
Angles are measured in degrees, where 0° points straight up, and values increase clockwise.

### Usage
- `shape_name = shape.pie(x, y, r, f, t)`
    - `x, y`: Position of the centre point
    - `r`: Radius of the pie slice
    - `f`: Start angle
    - `t`: End angle

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  a = badge.ticks / 10
  p = shape.pie(80, 60, 40, a + 30, a + 150)
  screen.pen = color.green
  screen.shape(p)

  badge.update()
```

## star
Creates a new shape representing a star.

### Usage
- `shape_name = shape.star(x, y, s, ro, ri)`
    - `x, y`: Position of the centre point
    - `s`: Number of points
    - `ro`: Outer radius (tip distance from centre)
    - `ri`: Inner radius (indent distance from centre)

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  star = shape.star(80, 60, 7, 25, 40)
  screen.pen = color.latte
  screen.shape(star)

  badge.update()
```

## line
Creates a new `shape` representing a line segment.

### Usage
- `shape_name = shape.line(x1, y1, x2, y2, w)`
    - `x1, y1`: Start position
    - `x2, y2`: End position
    - `w`: Line width

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  line = shape.line(30, 30, 120, 80, 10)
  screen.pen = color.smoke
  screen.shape(line)

  badge.update()
```

## custom()
Creates a `shape` from one or more lists of points, letting you build completely arbitrary geometry. The first list is the outer contour. Any further lists are treated as holes cut out of the shape.

### Usage
- `shape_name = shape.custom(paths)`
    - `paths`: A list of contours. Each contour is a list of `vec2` points. Pass a single list for a simple shape, or several for a shape with holes.

### Returns
A `shape` representing the created shape.

### Example
```python
while True:
  # an outer triangle with a triangular hole
  outer = [vec2(80, 15), vec2(140, 110), vec2(20, 110)]
  hole = [vec2(80, 55), vec2(110, 100), vec2(50, 100)]

  screen.pen = color.lime
  screen.shape(shape.custom([outer, hole]))

  badge.update()
```

# Properties

## transform
A matrix transformation applied to this shape when it is drawn.
This allows shapes to be translated, rotated, scaled, or skewed without modifying the underlying path data. The transform is applied at render time, making it useful for animation and repositioning shapes efficiently.

# Methods

## stroke()
Replaces this shape with its **stroked outline** — the shape is modified **in place** and the method returns the shape itself, so calls can be chained. This turns a filled shape into a hollow outline of a given thickness, useful for borders, rings, and line art.

Because `stroke()` mutates the shape, keep a separate copy if you also want the filled version. Since it returns the shape, you can create and stroke in one line: `outline = shape.circle(80, 60, 40).stroke(4)`.

The optional `flags` argument controls how the outline is built. OR together one value from each group (every default is the `0` value, so you only need to include the ones you want to change):

- **Alignment** — where the stroke sits relative to the original edge: `shape.ALIGN_OUTER` (default, grows outward), `shape.ALIGN_INNER` (grows inward), `shape.ALIGN_CENTER` (straddles the edge).
- **Path** — `shape.PATH_CLOSED` (default, a closed loop) or `shape.PATH_OPEN` (an open line, which adds end caps).
- **Joins** — how corners are drawn: `shape.JOIN_MITER` (default, sharp), `shape.JOIN_ROUND`, `shape.JOIN_BEVEL`.
- **Caps** — how the ends of an open path are drawn: `shape.CAP_BUTT` (default), `shape.CAP_ROUND`, `shape.CAP_SQUARE`.

### Usage
- `shape_name.stroke(width, flags, miter_limit)`
    - `width`: Thickness of the stroke in pixels.
    - `flags` (Optional): OR of the alignment/path/join/cap constants above. Defaults to `0`.
    - `miter_limit` (Optional): Limit at which sharp mitre joins are clipped to bevels. Defaults to `4.0`.

### Returns
The `shape`, replaced by its stroked outline.

### Example
```python
while True:
  a = badge.ticks / 20

  # a rounded, outlined star
  star = shape.star(80, 60, 6, 20, 45)
  star.transform = mat3().rotate(a).translate(80, 60)
  star.stroke(6, shape.JOIN_ROUND)

  screen.pen = color.yellow
  screen.shape(star)

  badge.update()
```

## bounds()
Returns the device-space bounding box of the shape as a `rect`. This is the shape's local bounding box run through its current transform, so it accounts for any rotation, scale or translation applied via `transform`.

### Returns
A `rect` describing the shape's bounds on screen.

# Reference

## Constructors
```python-raw
shape.arc(x: int|float, y: int|float, inner: int|float, outer: int|float, from: int|float, to: int|float) -> shape
shape.circle(centre: vec2, radius: int|float) -> shape
shape.circle(x: int|float, y: int|float, radius: int|float) -> shape
shape.custom(paths: list) -> shape
shape.ellipse(centre: vec2, rx: int|float, ry: int|float) -> shape
shape.ellipse(x: int|float, y: int|float, rx: int|float, ry: int|float) -> shape
shape.line(x1: int|float, y1: int|float, x2: int|float, y2: int|float, w: int|float) -> shape
shape.pie(x: int|float, y: int|float, r: int|float, f: int|float, t: int|float) -> shape
shape.rectangle(x: int|float, y: int|float, width: int|float, height: int|float) -> shape
shape.regular_polygon(x: int|float, y: int|float, radius: int|float, sides: int) -> shape
shape.rounded_rectangle(x: int|float, y: int|float, width: int|float, height: int|float, radius: int|float) -> shape
shape.rounded_rectangle(x: int|float, y: int|float, width: int|float, height: int|float, r1: int|float, r2: int|float, r3: int|float, r4: int|float) -> shape
shape.squircle(x: int|float, y: int|float, s: int|float, n: int|float=4) -> shape
shape.star(x: int|float, y: int|float, s: int, ro: int|float, ri: int|float) -> shape
```

## Constants
```python-raw
shape.ALIGN_OUTER   shape.ALIGN_INNER   shape.ALIGN_CENTER
shape.PATH_CLOSED   shape.PATH_OPEN
shape.JOIN_MITER    shape.JOIN_ROUND    shape.JOIN_BEVEL
shape.CAP_BUTT      shape.CAP_ROUND     shape.CAP_SQUARE
```

## Properties
```python-raw
shape.transform -> mat3
```

## Methods
```python-raw
shape.stroke(width: int|float, flags: int=0, miter_limit: int|float=4.0) -> shape
shape.bounds() -> rect
```
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
```python-raw
shape.circle(x, y, radius)
shape.circle(centre, radius)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `centre` | `vec2` | Position of the centre point |
| `radius` | `int` \| `float` | Radius of the circle in pixels |

### Returns
A `shape` representing the created shape.

```python
def update():
  screen.pen = color.taupe
  circle = shape.circle(80, 60, 40)
  screen.shape(circle)

run(update)
```

## rectangle()
Creates a new `shape` representing a rectangle.

### Usage
```python-raw
shape.rectangle(x, y, width, height)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Coordinates of the top-left corner |
| `width`, `height` | `int` \| `float` | Width and height of the rectangle |

### Returns
A `shape` representing the created shape.

```python
def update():
  screen.pen = color.blue
  rectangle = shape.rectangle(30, 30, 100, 60)
  screen.shape(rectangle)

run(update)
```

## regular_polygon()
Creates a new shape representing a regular polygon — a closed shape with evenly spaced sides and equal angles (for example: triangles, squares, pentagons, and so on).

### Usage
```python-raw
shape.regular_polygon(x, y, radius, sides)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `radius` | `int` \| `float` | Radius of the polygon (distance from the centre to each corner) |
| `sides` | `int` | Number of sides (must be 3 or greater) |

### Returns
A `shape` representing the created shape.

```python
def update():
  sides = ((badge.ticks // 500) % 10) + 3

  polygon = shape.regular_polygon(80, 60, 40, sides)
  screen.pen = color.red
  screen.shape(polygon)

  screen.pen = color.white
  screen.text(f"{sides} sides", 5, 5)

run(update)
```

## rounded_rectangle()
Creates a new `shape` representing a rectangle with rounded corners.
Rounded rectangles are especially useful for modern UI elements such as buttons, panels, dialog boxes, and badges.
You can specify either a single corner radius for all corners, or provide individual radii to create asymmetric shapes.

### Usage
```python-raw
shape.rounded_rectangle(x, y, width, height, radius)
shape.rounded_rectangle(x, y, width, height, r1, r2, r3, r4)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Coordinates of the top-left corner |
| `width`, `height` | `int` \| `float` | Width and height |
| `radius` | `int` \| `float` | Corner radius applied to all corners |
| `r1`, `r2`, `r3`, `r4` | `int` \| `float` | Corner radii (top-left, top-right, bottom-right, bottom-left) |

### Returns
A `shape` representing the created shape.

```python
def update():
  screen.pen = color.yellow
  rounded_rectangle = shape.rounded_rectangle(15, 10, 60, 60, 10)
  screen.shape(rounded_rectangle)

  screen.pen = color.navy
  rounded_rectangle = shape.rounded_rectangle(85, 50, 60, 60, 0, 20, 0, 20)
  screen.shape(rounded_rectangle)

run(update)
```

## squircle()
Creates a new shape representing a squircle — a smooth shape that sits somewhere between a square and a circle.

Squircles are useful for UI elements like icons and buttons, producing corners that feel softer and more natural than a standard rounded rectangle.

The optional squareness factor controls the shape: lower values are more circular, higher values more square-like.

### Usage
```python-raw
shape.squircle(x, y, s, n)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `s` | `int` \| `float` | Size of the squircle |
| `n` | `int` \| `float` | *Optional.* Squareness factor (default 4). Lower values are more circular, higher values more square-like. |

### Returns
A `shape` representing the created shape.

```python
def update():
  screen.pen = color.orange
  squircle = shape.squircle(80, 60, 40)
  screen.shape(squircle)

run(update)
```

## arc()
Creates a new shape representing an arc segment.
Arcs are useful for gauges, progress indicators, rings, and other circular UI elements. The arc is defined by an inner and outer radius, producing a curved band between two angles.
Angles are measured in degrees, where 0° points straight up, and values increase clockwise.

### Usage
```python-raw
shape.arc(x, y, inner, outer, from, to)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `inner` | `int` \| `float` | Inner radius |
| `outer` | `int` \| `float` | Outer radius |
| `from` | `int` \| `float` | Start angle (degrees) |
| `to` | `int` \| `float` | End angle (degrees) |

### Returns
A `shape` representing the created shape.

```python
def update():
  angle = badge.ticks / 10
  arc = shape.arc(80, 60, 30, 40, angle + 30, angle + 150)
  screen.pen = color.cyan
  screen.shape(arc)

run(update)
```

## pie()
Creates a new shape representing a pie slice (think Pacman).
The slice is defined by an inner and outer radius.
Angles are measured in degrees, where 0° points straight up, and values increase clockwise.

### Usage
```python-raw
shape.pie(x, y, r, f, t)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `r` | `int` \| `float` | Radius of the pie slice |
| `f` | `int` \| `float` | Start angle (degrees) |
| `t` | `int` \| `float` | End angle (degrees) |

### Returns
A `shape` representing the created shape.

```python
def update():
  a = badge.ticks / 10
  p = shape.pie(80, 60, 40, a + 30, a + 150)
  screen.pen = color.green
  screen.shape(p)

run(update)
```

## star()
Creates a new shape representing a star.

### Usage
```python-raw
shape.star(x, y, s, ro, ri)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `s` | `int` | Number of points |
| `ro` | `int` \| `float` | Outer radius (tip distance from centre) |
| `ri` | `int` \| `float` | Inner radius (indent distance from centre) |

### Returns
A `shape` representing the created shape.

```python
def update():
  star = shape.star(80, 60, 7, 25, 40)
  screen.pen = color.latte
  screen.shape(star)

run(update)
```

## line()
Creates a new `shape` representing a line segment.

### Usage
```python-raw
shape.line(x1, y1, x2, y2, w)
```

| Parameter | Type | Description |
|---|---|---|
| `x1`, `y1` | `int` \| `float` | Start position |
| `x2`, `y2` | `int` \| `float` | End position |
| `w` | `int` \| `float` | Line width |

### Returns
A `shape` representing the created shape.

```python
def update():
  line = shape.line(30, 30, 120, 80, 10)
  screen.pen = color.smoke
  screen.shape(line)

run(update)
```

# Properties

| Property | Type | Description |
|---|---|---|
| `transform` | `mat3` | Matrix transformation applied to this shape when it is drawn |

The transform allows shapes to be translated, rotated, scaled, or skewed without modifying the underlying path data. It is applied at render time, making it useful for animation and repositioning shapes efficiently.

# Methods

## stroke()
Returns a new shape representing the outline (stroke) of this shape.

Stroking is useful for drawing borders around filled shapes, creating hollow outlines, or generating thicker versions of existing geometry. The original shape is not modified — instead, `stroke()` produces a new shape that can be drawn like any other.

The supplied thickness controls where the outline is placed:

- If the thickness is positive, the stroke expands outward from the shape’s edge.
- If the thickness is negative, the stroke is applied inward, shrinking into the shape’s interior.

This makes it possible to create both outer borders and inset outlines depending on the effect you want.

### Usage
```python-raw
.stroke(thickness)
```

| Parameter | Type | Description |
|---|---|---|
| `thickness` | `int` | Thickness of the stroke in pixels |

### Returns
A `shape` representing the stroke of the previous shape.

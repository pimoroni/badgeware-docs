---
title: shape
summary: Create primitive vector shapes as well as custom shapes, then modify them to build more complex vector graphics.
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
`shape.circle(x, y, radius)` \
`shape.circle(centre, radius)`

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

## ellipse()
Creates a new `shape` representing an ellipse, with a radius per axis.

### Usage
`shape.ellipse(x, y, rx, ry)` \
`shape.ellipse(centre, rx, ry)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Position of the centre point |
| `centre` | `vec2` | Position of the centre point |
| `rx`, `ry` | `int` \| `float` | Radius across and down, in pixels |

### Returns
A `shape` representing the created shape.

```python
def update():
  screen.pen = color.cyan
  screen.shape(shape.ellipse(80, 60, 60, 25))

run(update)
```

## rectangle()
Creates a new `shape` representing a rectangle.

### Usage
`shape.rectangle(x, y, width, height)`

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
`shape.regular_polygon(x, y, radius, sides)`

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
`shape.rounded_rectangle(x, y, width, height, radius)` \
`shape.rounded_rectangle(x, y, width, height, r1, r2, r3, r4)`

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
`shape.squircle(x, y, s, n)`

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
`shape.arc(x, y, inner, outer, from, to)`

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
`shape.pie(x, y, r, f, t)`

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
`shape.star(x, y, s, ro, ri)`

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
`shape.line(x1, y1, x2, y2, w)`

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

## custom()
Creates a new `shape` from points you supply, for geometry none of the primitives covers. Each argument is one contour, and the first is the outline: any that follow punch holes in it.

A contour is either a list of `vec2`, or an `array('f')` of flat `x, y` pairs, which allocates no `vec2` objects and suits geometry you rebuild every frame. Points are joined in the order given and the contour closes itself, so there's no need to repeat the first point at the end.

Holes rely on the even-odd fill rule, which is the default; see [`fill_rule`](/api/image.md#properties).

### Usage
`shape.custom(contour)` \
`shape.custom(outline, hole, ...)`

| Parameter | Type | Description |
|---|---|---|
| `contour` | `list` \| `array` | A list of `vec2`, or an `array('f')` of `x, y` pairs |

### Returns
A `shape` representing the created shape.

```python
from array import array

# an arrow as one contour, and a square hole in the middle of it
arrow = [vec2(20, 50), vec2(90, 50), vec2(90, 30), vec2(140, 60),
         vec2(90, 90), vec2(90, 70), vec2(20, 70)]
hole = array("f", [60, 55, 75, 55, 75, 65, 60, 65])

def update():
  screen.pen = color.orange
  screen.shape(shape.custom(arrow, hole))

run(update)
```

# Properties

| Property | Type | Description |
|---|---|---|
| `transform` | `mat3` | Matrix transformation applied to this shape when it is drawn |

The transform allows shapes to be translated, rotated, scaled, or skewed without modifying the underlying path data. It is applied at render time, making it useful for animation and repositioning shapes efficiently.

# Methods

## stroke()
Replaces this shape with a band along its outline, and returns the same shape so the call can be chained onto a factory. It's a **conversion, not a copy**: the filled shape you called it on is gone afterwards, so build a second one if you want the fill as well as the border.

Stroking is how you get borders around filled shapes, hollow outlines, and thicker versions of existing geometry. The thickness controls where the band sits relative to the outline:

- If the thickness is positive, the stroke expands outward from the shape's edge.
- If the thickness is negative, the stroke is applied inward, shrinking into the shape's interior.

`flags` picks the alignment, path closure, join and cap, one value from each group combined with the pipe symbol — see [stroke flags](#stroke-flags). `miter_limit` caps how far a mitred join may spike out at a sharp corner before it's cut off flat, as a multiple of the thickness.

The band is drawn as two contours filled even-odd, which is the default fill rule; if you've set [`fill_rule`](/api/image.md#properties) to `image.NON_ZERO` a stroke fills solid instead.

### Usage
`.stroke(thickness)` \
`.stroke(thickness, flags, miter_limit)`

| Parameter | Type | Description |
|---|---|---|
| `thickness` | `int` | Thickness of the stroke in pixels. Negative strokes inward |
| `flags` | `int` | *Optional.* One [stroke flag](#stroke-flags) per group, combined with the pipe symbol. Defaults to `0`, which is outer alignment, a closed path, mitre joins and butt caps |
| `miter_limit` | `float` | *Optional.* How far a mitred corner may extend, as a multiple of the thickness. Defaults to `4.0` |

### Returns
The same `shape`, now stroked.

```python
def update():
  screen.pen = color.navy
  screen.shape(shape.circle(50, 60, 30))

  # a rounded, centred outline over the filled circle
  screen.pen = color.cyan
  screen.shape(shape.circle(50, 60, 30).stroke(4, shape.ALIGN_CENTER | shape.JOIN_ROUND))

  # an open zigzag, capped round at both ends
  zigzag = shape.custom([vec2(90, 40), vec2(110, 80), vec2(130, 40), vec2(150, 80)])
  screen.pen = color.yellow
  screen.shape(zigzag.stroke(3, shape.PATH_OPEN | shape.CAP_ROUND | shape.JOIN_ROUND))

run(update)
```

## bounds()
Returns the box the shape occupies on the image, with its [`transform`](#properties) applied. Useful for hit-testing one shape's box against another, or for placing something beside a shape you've moved.

### Usage
`.bounds()`

### Returns
A `rect`.

```python-raw
dial = shape.star(80, 60, 5, 40, 18)
dial.transform = mat3().translate(20, 0).rotate(30)
box = dial.bounds()      # where it actually landed
```

# Stroke flags
[`stroke()`](#stroke) takes one flag from each of these groups, combined with the pipe symbol. Every group's default is its `0` value, so you only need to name the ones you're changing.

| Group | Constants | Effect |
|---|---|---|
| Alignment | `shape.ALIGN_OUTER` (default), `shape.ALIGN_INNER`, `shape.ALIGN_CENTER` | Whether the band grows outward from the outline, inward, or straddles it |
| Path closure | `shape.PATH_CLOSED` (default), `shape.PATH_OPEN` | Whether the outline is a closed loop, or an open line with two ends to cap |
| Join | `shape.JOIN_MITER` (default), `shape.JOIN_ROUND`, `shape.JOIN_BEVEL` | How the band turns a corner: a sharp point, an arc, or a flat cut |
| Cap | `shape.CAP_BUTT` (default), `shape.CAP_ROUND`, `shape.CAP_SQUARE` | How an open path's ends finish: flat on the endpoint, a semicircle past it, or squared off past it |

Joins and caps only show up where they apply: a closed shape has no ends to cap, and a curve approximated by enough short segments has no corner sharp enough to tell one join from another.

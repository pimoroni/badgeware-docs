---
title: rect
summary: Represents a 2D rectangle and provides helpful methods for manipulating and working with rectangular regions.
icon: check_box_outline_blank
publish: true
---
# Introduction
Represents a rectangular region defined by its top-left position (`x`, `y`) and size (`w` × `h`).

Although `x`, `y`, `w`, and `h` are stored as floating-point values, they represent pixel coordinates. This allows rectangles to be positioned with subpixel precision. For most basic drawing operations, these values are typically cast to integers before rendering.

# Constructor

## rect()
Returns a `rect` with the specified dimensions and position.

### Usage
`rect(x, y, w, h)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `float` | Pixel coordinates of the top-left corner of the `rect` |
| `w`, `h` | `float` | Width and height of the `rect` |

### Returns
`rect`

# Properties

| Property | Type | Description |
|---|---|---|
| `x` | `float` | The x-coordinate of the top-left corner of the rectangle |
| `y` | `float` | The y-coordinate of the top-left corner of the rectangle |
| `w` | `float` | The width of the rectangle |
| `h` | `float` | The height of the rectangle |
| `l` | `float` | The x-coordinate of the top-left corner of the rectangle |
| `r` | `float` | The x-coordinate of the bottom-right corner of the rectangle |
| `t` | `float` | The y-coordinate of the top-left corner of the rectangle |
| `b` | `float` | The y-coordinate of the bottom-right corner of the rectangle |

# Methods

## offset()
Returns a new rectangle offset by the specified amount.

### Usage
`.offset(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `float` | Amount to offset the rectangle by |

### Returns
A `rect` representing the offset rectangle.

## deflate()
Returns a new rectangle with its area reduced in size.

### Usage
`.deflate(a)` \
`.deflate(t, r, b, l)`

| Parameter | Type | Description |
|---|---|---|
| `a` | `float` | Amount to deflate each edge by |
| `t`, `r`, `b`, `l` | `float` | Amounts to deflate the top, right, bottom, and left edges |

### Returns
A `rect` representing the smaller rectangle.

## inflate()
Returns a new rectangle with its area increased in size.

### Usage
`.inflate(a)` \
`.inflate(t, r, b, l)`

| Parameter | Type | Description |
|---|---|---|
| `a` | `float` | Amount to inflate each edge by |
| `t`, `r`, `b`, `l` | `float` | Amounts to inflate the top, right, bottom, and left edges |

### Returns
A `rect` representing the larger rectangle.

## intersection()
Returns a new rectangle representing the overlapping area between this rectangle and another.
If the rectangles do not overlap, `None` is returned.

### Usage
`.intersection(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `rect` | The rectangle to intersect with |

### Returns
A `rect` representing the intersection of the two operands.

## intersects()
Returns `True` if this rectangle overlaps with another rectangle, otherwise `False`.

### Usage
`.intersects(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `rect` | The rectangle to test for intersection with |

### Returns
`bool`

## contains()
Returns `True` if this rectangle fully contains another rectangle, otherwise `False`.

### Usage
`.contains(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `rect` | The rectangle to test for containment |

### Returns
`bool`

## empty()
Returns `True` if this rectangle has a width or height of zero, otherwise `False`.

### Usage
`.empty()`

### Returns
`bool`

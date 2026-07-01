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
- `rect_name = rect()` - Creates an empty rectangle at the origin.
- `rect_name = rect(x, y, w, h)`
    - `x, y`: Pixel coordinates of the top left corner of the `rect`.
    - `w, h`: Width and height of the `rect`.
- `rect_name = rect(other)`
    - `other`: An existing `rect` to copy.

# Properties

## x
The x-coordinate of the top-left corner of the rectangle.

## y
The y-coordinate of the top-left corner of the rectangle.

## w
The width of the rectangle.

## h
The height of the rectangle.

## l
The left edge of the rectangle. This is an alias for `x`.

## r
The right edge of the rectangle (`x + w`). Assigning to it adjusts the width.

## t
The top edge of the rectangle. This is an alias for `y`.

## b
The bottom edge of the rectangle (`y + h`). Assigning to it adjusts the height.

# Methods

## offset()
Shifts the rectangle by the specified amount, **in place**, and returns the rectangle so calls can be chained.

### Usage
- `rect_name.offset(x, y)`
    - `x, y`: Amount to offset the rectangle by.
- `rect_name.offset(p)`
    - `p`: A `vec2` to offset by.

### Returns
The `rect`, modified in place.

## deflate()
Shrinks the rectangle inward on every side, **in place**, and returns the rectangle.

### Usage
- `rect_name.deflate(a)`
    - `a`: Amount to shrink every edge by.
- `rect_name.deflate(x, y)`
    - `x`: Amount to shrink the left and right edges by.
    - `y`: Amount to shrink the top and bottom edges by.

### Returns
The `rect`, modified in place.

## inflate()
Grows the rectangle outward on every side, **in place**, and returns the rectangle.

### Usage
- `rect_name.inflate(a)`
    - `a`: Amount to grow every edge by.
- `rect_name.inflate(x, y)`
    - `x`: Amount to grow the left and right edges by.
    - `y`: Amount to grow the top and bottom edges by.

### Returns
The `rect`, modified in place.

## intersection()
Returns a **new** rectangle representing the overlapping area between this rectangle and another. If the rectangles do not overlap, an empty rectangle (zero width and height) is returned — test the result with `empty()`.

### Usage
- `rect_name.intersection(other)`
    - `other`: The rectangle to intersect with.

### Returns
A `rect` representing the intersection of the two operands (empty if they are disjoint).

## intersects()
Returns `True` if this rectangle overlaps with another rectangle, otherwise `False`.

### Usage
- `rect_name.intersects(other)`
    - `other`: The rectangle to test for intersection with.

### Returns
`bool`

## contains()
Returns `True` if this rectangle fully contains another rectangle, or a point, otherwise `False`.

### Usage
- `rect_name.contains(other)`
    - `other`: The `rect` to test for containment.
- `rect_name.contains(point)`
    - `point`: A `vec2` to test.

### Returns
`bool`

## empty()
Returns `True` if this rectangle has a width or height of zero, otherwise `False`.

### Returns
`bool`

# Reference

## Constructor
```python-raw
rect() -> rect
rect(other: rect) -> rect
rect(x: int|float, y: int|float, w: int|float, h: int|float) -> rect
```

## Properties
```python-raw
rect.x -> float
rect.y -> float
rect.w -> float
rect.h -> float
rect.l -> float
rect.r -> float
rect.t -> float
rect.b -> float
```

## Methods
```python-raw
rect.contains(other: rect) -> bool
rect.contains(point: vec2) -> bool
rect.deflate(a: int|float) -> rect
rect.deflate(x: int|float, y: int|float) -> rect
rect.empty() -> bool
rect.inflate(a: int|float) -> rect
rect.inflate(x: int|float, y: int|float) -> rect
rect.intersection(other: rect) -> rect
rect.intersects(other: rect) -> bool
rect.offset(x: int|float, y: int|float) -> rect
rect.offset(p: vec2) -> rect
```
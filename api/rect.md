---
title: rect
summary: Represents a 2D rectangle and provides helpful methods for manipulating and working with rectangular regions.
icon: activity_zone
publish: true
---
# Introduction
Represents a rectangular region defined by its top-left position (`x`, `y`) and size (`w` × `h`).

Although `x`, `y`, `w`, and `h` are stored as floating-point values, they represent pixel coordinates. This allows rectangles to be positioned with subpixel precision. For most basic drawing operations, these values are typically cast to integers before rendering.

# Constructor

## rect()
Returns a `rect` with the specified dimensions and position.

### Usage
- `rect_name = rect(x, y, w, h)`
    - `x, y`: Pixel coordinates of the top left corner of the `rect`.
    - `w, h`: Width and height of the `rect`.

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
The x-cordinate of the top-left corner of the rectangle.

## r
The x-coordinate of the bottom-right corner of the rectangle.

## t
The y-cordinate of the top-left corner of the rectangle.

## b
The y-coordinate of the bottom-right corner of the rectangle.

# Methods

## offset()
Returns a new rectangle offset by the specified amount.

### Usage
- `rect_name.offset(x, y)`
    - `x, y`: Amount to offset the rectangle by.

### Returns
A `rect` representing the offset rectangle.

## deflate()
Returns a new rectangle with its area reduced in size.

### Usage
- `rect_name.deflate(a)`
    - `a`: Amount to deflate each edge by.
- `rect_name.deflate(t, r, b, l)`
    - `t, r, b, l`: Amounts to deflate the top, right, bottom, and left edges.

### Returns
A `rect` representing the smaller rectangle.

## inflate()
Returns a new rectangle with its area increased in size.

### Usage
- `rect_name.inflate(a)`
    - `a`: Amount to inflate each edge by.
- `rect_name.inflate(t, r, b, l)`
    - `t, r, b, l`: Amounts to inflate the top, right, bottom, and left edges.

### Returns
A `rect` representing the larger rectangle.

## intersection()
Returns a new rectangle representing the overlapping area between this rectangle and another.
If the rectangles do not overlap, `None` is returned.

### Usage
- `rect_name.intersection(other)`
    - `other`: The rectangle to intersect with.

### Returns
A `rect` representing the intersection of the two operands.

## intersects()
Returns `True` if this rectangle overlaps with another rectangle, otherwise `False`.

### Usage
- `rect_name.intersects(other)`
    - `other`: The rectangle to test for intersection with.

### Returns
`bool`

## contains()
Returns `True` if this rectangle fully contains another rectangle, otherwise `False`.

### Usage
- `rect_name.contains(other)`
    - `other`: The rectangle to test for containment.

### Returns
`bool`

## empty()
Returns `True` if this rectangle has a width or height of zero, otherwise `False`.

### Returns
`bool`

# Reference

## Constructor
```python-raw
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
rect.deflate(a: int|float) -> rect
rect.deflate(t: int|float, r: int|float, b: int|float, l: int|float) -> rect
rect.empty() -> bool
rect.inflate(a: int|float) -> rect
rect.inflate(t: int| float, r: int| float, b: int| float, l: int|float) -> rect
rect.intersection(other: rect) -> rect | None
rect.intersects(other: rect) -> bool
rect.offset(x: int|float, y: int|float) -> rect
```
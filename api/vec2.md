---
title: vec2
summary: Represents a 2D vector (point) with x and y coordinates, commonly used for positions and directions.
icon: polyline
publish: true
---
# Introduction
Represents a 2D vector/point with `x` and `y` coordinates.

Although x and y are stored as floating-point values, they represent pixel coordinates. This allows points to be positioned with subpixel precision. For most basic drawing operations, these values are typically cast to integers before rendering.

# Constructor

## vec2()
### Usage
- `point_name = vec2(x, y)`
        - `x, y` - The pixel coordinates.

### Returns
A `vec2` containing the specified coordinates.

# Properties

## x
The x coordinate measured in pixels.

## y
The y coordinate measured in pixels.

# Methods

## transform()
Returns a new `vec2` with the specified matrix transformation applied.

### Usage
- `point_name.transform(m)`
    - `m`: A transformation matrix

# Reference

## Constructor
```python-raw
vec2(x: int|float, y: int|float) -> vec2
```

## Properties
```python-raw
vec2.x -> float
vec2.y -> float
```

## Methods
```python-raw
vec2.transform(m: mat3) -> vec2
```
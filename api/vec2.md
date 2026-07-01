---
title: vec2
summary: Represents a 2D vector (point) with x and y coordinates, commonly used for positions and directions.
icon: diagonal_line
publish: true
---
# Introduction
Represents a 2D vector/point with `x` and `y` coordinates.

Although x and y are stored as floating-point values, they represent pixel coordinates. This allows points to be positioned with subpixel precision. For most basic drawing operations, these values are typically cast to integers before rendering.

A `vec2` is used both as a *point* (a position on screen) and as a *vector* (a direction and length). The methods below cover both uses — measuring lengths and distances, rotating and reflecting, and interpolating between points.

# Constructor

## vec2()
### Usage
- `point_name = vec2()` - Creates a zero vector `(0, 0)`.
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
Unless otherwise stated, these methods return a **new** `vec2` and leave the original unchanged.

## length()
Returns the magnitude (Euclidean length) of the vector.

## length_squared()
Returns the squared magnitude. This avoids a square root, so it's faster than `length()` when you only need to compare magnitudes.

## dot()
Returns the dot product with another vector.

### Usage
- `point_name.dot(other)`
    - `other`: The other `vec2`.

## cross()
Returns the cross product (the scalar z-component) with another vector.

### Usage
- `point_name.cross(other)`
    - `other`: The other `vec2`.

## distance()
Returns the Euclidean distance to another point.

### Usage
- `point_name.distance(other)`
    - `other`: The other `vec2`.

## distance_squared()
Returns the squared distance to another point — faster than `distance()` when you only need to compare distances.

### Usage
- `point_name.distance_squared(other)`
    - `other`: The other `vec2`.

## angle()
Returns the angle of the vector in radians (`atan2(y, x)`).

## angle_to()
Returns the angle from this vector to another, in radians.

### Usage
- `point_name.angle_to(other)`
    - `other`: The other `vec2`.

## normalized()
Returns a unit vector (length 1) pointing in the same direction.

## perpendicular()
Returns a vector perpendicular to this one (rotated 90°).

## abs()
Returns a vector with the absolute value of each component.

## rotated()
Returns this vector rotated by the given angle.

### Usage
- `point_name.rotated(angle)`
    - `angle`: The angle to rotate by, in radians.

## lerp()
Linearly interpolates towards another point. `t=0` returns this point, `t=1` returns the other.

### Usage
- `point_name.lerp(other, t)`
    - `other`: The target `vec2`.
    - `t`: The interpolation factor from 0 to 1.

### Example
```python
a = vec2(20, 20)
b = vec2(140, 100)

while True:
  # ping-pong t between 0 and 1
  t = (badge.ticks % 2000) / 1000
  if t > 1:
    t = 2 - t

  p = a.lerp(b, t)

  screen.pen = color.smoke
  screen.line(a, b)

  screen.pen = color.orange
  screen.circle(p, 6)

  badge.update()
```

## reflect()
Returns this vector reflected around the given normal.

### Usage
- `point_name.reflect(normal)`
    - `normal`: The `vec2` to reflect around.

## clamp_length()
Returns this vector clamped to a maximum magnitude, keeping its direction.

### Usage
- `point_name.clamp_length(max_length)`
    - `max_length`: The maximum length.

## transform()
Applies a matrix transformation to this vector **in place**. Unlike the other methods, this modifies the vector rather than returning a new one, and returns `None`.

### Usage
- `point_name.transform(m)`
    - `m`: A transformation `mat3`.

# Operators
`vec2` supports arithmetic with other vectors and with scalars:

- `a + b`, `a - b` — component-wise addition and subtraction.
- `a * b`, `a / b` — multiply/divide by a `vec2` (component-wise) or by a scalar.
- `a == b`, `a != b` — equality comparison.

### Example
```python
import math

while True:
  centre = vec2(80, 60)

  # a direction vector, scaled by a scalar
  angle = badge.ticks / 500
  direction = vec2(math.cos(angle), math.sin(angle)) * 40

  tip = centre + direction

  screen.pen = color.navy
  screen.line(centre, tip)

  screen.pen = color.yellow
  screen.circle(tip, 5)

  badge.update()
```

# Reference

## Constructor
```python-raw
vec2() -> vec2
vec2(x: int|float, y: int|float) -> vec2
```

## Properties
```python-raw
vec2.x -> float
vec2.y -> float
```

## Methods
```python-raw
vec2.abs() -> vec2
vec2.angle() -> float
vec2.angle_to(other: vec2) -> float
vec2.clamp_length(max_length: int|float) -> vec2
vec2.cross(other: vec2) -> float
vec2.distance(other: vec2) -> float
vec2.distance_squared(other: vec2) -> float
vec2.dot(other: vec2) -> float
vec2.length() -> float
vec2.length_squared() -> float
vec2.lerp(other: vec2, t: int|float) -> vec2
vec2.normalized() -> vec2
vec2.perpendicular() -> vec2
vec2.reflect(normal: vec2) -> vec2
vec2.rotated(angle: int|float) -> vec2
vec2.transform(m: mat3) -> None
```

## Operators
```python-raw
vec2 + vec2 -> vec2
vec2 - vec2 -> vec2
vec2 * (vec2 | int|float) -> vec2
vec2 / (vec2 | int|float) -> vec2
vec2 == vec2 -> bool
vec2 != vec2 -> bool
```

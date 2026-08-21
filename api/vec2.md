---
title: vec2
summary: Represents a 2D vector (point) with x and y coordinates, commonly used for positions and directions.
icon: diagonal_line
publish: true
---
# Introduction
Represents a 2D vector/point with `x` and `y` coordinates.

Although x and y are stored as floating-point values, they represent pixel coordinates. This allows points to be positioned with subpixel precision. For most basic drawing operations, these values are typically cast to integers before rendering.

# Constructor

## vec2()
Returns a `vec2` containing the specified coordinates.

### Usage
`vec2(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `float` | The pixel coordinates |

### Returns
A `vec2` containing the specified coordinates.

# Properties

| Property | Type | Description |
|---|---|---|
| `x` | `float` | The x coordinate measured in pixels |
| `y` | `float` | The y coordinate measured in pixels |

# Methods
Every method here returns a new value and leaves the vector it was called on alone, apart from `transform()`, which changes it in place.

Angles are in **radians** throughout, unlike [`mat3`](/api/mat3.md), which works in degrees. And because y counts downward on a screen, a positive angle turns clockwise as you look at the badge.

## length() / length_squared()
Returns the length of the vector: how far it reaches from the origin. `length_squared()` skips the square root, so when you only want to compare two lengths against each other it's the cheaper call.

### Usage
`.length()` \
`.length_squared()`

### Returns
A `float`.

```python-raw
speed = velocity.length()
if (target - position).length_squared() < 100:   # within 10 pixels
    arrived()
```

## dot()
Returns the dot product with another vector. It's positive when the two point roughly the same way, zero when they're at right angles, and negative when they oppose. That sign is the quick test for whether something is in front of you.

### Usage
`.dot(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `vec2` | The vector to take the dot product with |

### Returns
A `float`.

## cross()
Returns the 2D cross product, the z component of the 3D one. Its sign says which side of this vector `other` falls on, and so which way to turn to face it.

### Usage
`.cross(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `vec2` | The vector to take the cross product with |

### Returns
A `float`.

## distance() / distance_squared()
Returns the distance between two points. As with `length()`, the squared version skips the square root and is the one to reach for inside a loop that's only comparing distances.

### Usage
`.distance(other)` \
`.distance_squared(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `vec2` | The point to measure to |

### Returns
A `float`.

## angle()
Returns the direction the vector points, in radians, measured from the positive x axis.

### Usage
`.angle()`

### Returns
A `float` from `-pi` to `pi`.

## angle_to()
Returns the angle from this vector to another, in radians. It's signed, so the result tells you which way to turn as well as how far.

### Usage
`.angle_to(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `vec2` | The vector to measure to |

### Returns
A `float` from `-pi` to `pi`.

## normalized()
Returns a vector of length 1 pointing the same way: the direction with the distance thrown away. Multiply the result by a number and you have a step of exactly that many pixels. A zero-length vector has no direction to keep, and comes back as `vec2(0, 0)`.

### Usage
`.normalized()`

### Returns
A new `vec2`.

```python-raw
step = (target - position).normalized() * 2   # 2 pixels toward the target
```

## perpendicular()
Returns the vector turned a quarter turn, from `(x, y)` to `(-y, x)`. Useful for the sideways direction along a path — the normal of a wall, or the offset that gives a line its thickness.

### Usage
`.perpendicular()`

### Returns
A new `vec2`.

## abs()
Returns the vector with both components made positive.

### Usage
`.abs()`

### Returns
A new `vec2`.

## rotated()
Returns the vector rotated by an angle, about the origin. To turn a point about somewhere other than the origin, subtract that point first and add it back afterwards.

### Usage
`.rotated(angle)`

| Parameter | Type | Description |
|---|---|---|
| `angle` | `float` | The angle to rotate by, in radians |

### Returns
A new `vec2`.

## lerp()
Returns the point a fraction of the way from this one to another: `0` gives this vector, `1` gives `other`, `0.5` the midpoint. The fraction isn't clamped, so values outside 0 to 1 carry on past the ends.

### Usage
`.lerp(other, t)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `vec2` | The vector to interpolate toward |
| `t` | `float` | How far along, where `0` is this vector and `1` is `other` |

### Returns
A new `vec2`.

```python-raw
# ease the camera toward the player, a tenth of the gap each frame
camera = camera.lerp(player, 0.1)
```

## reflect()
Returns the vector bounced off a surface, given that surface's normal — the direction it faces. The normal must be a unit vector, so `normalized()` it first if it isn't one already.

### Usage
`.reflect(normal)`

| Parameter | Type | Description |
|---|---|---|
| `normal` | `vec2` | The unit normal of the surface to reflect off |

### Returns
A new `vec2`.

```python-raw
velocity = velocity.reflect(vec2(1, 0))   # bounce off a vertical wall
```

## clamp_length()
Returns the vector shortened to at most `max_length`, keeping its direction. Anything already shorter comes back unchanged. This is the usual way to cap a speed without flattening slow movement.

### Usage
`.clamp_length(max_length)`

| Parameter | Type | Description |
|---|---|---|
| `max_length` | `float` | The longest the result may be |

### Returns
A new `vec2`.

## transform()
Applies a matrix transformation to the vector **in place**, changing `x` and `y` and returning nothing. Every other method here returns a new vector. If you need the original afterwards, copy it first with `vec2(p.x, p.y)`.

### Usage
`.transform(m)`

| Parameter | Type | Description |
|---|---|---|
| `m` | `mat3` | A transformation matrix |

### Returns
Nothing. The vector is changed in place.

```python-raw
p = vec2(10, 0)
p.transform(mat3().rotate(90))   # p is now roughly vec2(0, 10)
```

# Operators
Vectors do arithmetic directly. Adding and subtracting work component by component; multiplying and dividing take either another vector, for a per-component scale, or a single number to scale both.

| Operator | Result |
|---|---|
| `a + b`, `a - b` | A new `vec2`, component by component |
| `a * b`, `a / b` | A new `vec2`, where `b` is a `vec2` or a number |
| `a == b`, `a != b` | A `bool` |
| `a += b`, `a -= b`, `a *= b`, `a /= b` | Changes `a` in place, allocating nothing |

In a loop that runs every frame, `position += velocity` updates the vector in place, while `position = position + velocity` builds a new one to throw away next frame.

```python
position = vec2(20, 60)
velocity = vec2(1.4, 0)

def update():
  global position, velocity

  screen.pen = color.black
  screen.clear()

  position += velocity

  # bounce off the sides, reflecting about the wall's normal
  if position.x < 6 or position.x > screen.width - 6:
    velocity = velocity.reflect(vec2(1, 0))

  screen.pen = color.lime
  screen.circle(position.x, position.y, 6)

run(update)
```

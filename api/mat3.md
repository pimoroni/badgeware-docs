---
title: mat3
summary: Defines 2D transformation matrices allowing shapes to be translated, rotated, scaled, or skewed during rendering.
icon: grid_3x3
publish: true
---
# Introduction
Matrices provide a unified way to handle transformations such as translation, rotation, scaling, and shearing. By combining these into a single matrix, you can apply complex transformations to vectors with a single operation.

Multiple transformations can also be chained together through matrix multiplication, making matrices both efficient and elegant tools for managing motion and geometry in 2D space.

Order matters, and the rule is that the **last** call in a chain is the first thing to happen to your geometry. `mat3().translate(80, 60).rotate(30)` turns a shape about the origin and then moves it to (80, 60), the order to use for a shape built around `(0, 0)`. To spin something that already sits somewhere, go to that point, turn, and come back:

```python-raw
spin = mat3().translate(p.x, p.y).rotate(angle).translate(-p.x, -p.y)
```

# Methods
`translate()`, `rotate()`, `scale()` and `multiply()` **change the matrix they're called on** and return the same one, so calls chain. A stored matrix therefore accumulates: calling `base.rotate(1)` each frame adds another degree every time. Build the transform from a fresh `mat3()` each frame, or from [`trs()`](#trs).

`inverse()` is the exception: it returns a new matrix and leaves the original alone.

## mat3()
Creates a new identity matrix: a transform that changes nothing.

### Usage
`mat3()`

### Returns
A `mat3` identity matrix.

## trs()
Builds a translate, rotate and scale in one call. The result matches `mat3().translate(t).rotate(degrees).scale(scale)`, worked out directly in a single allocation.

### Usage
`mat3.trs(x, y, degrees)` \
`mat3.trs(t, degrees, scale)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Amount to translate by |
| `t` | `vec2` | Amount to translate by |
| `degrees` | `int` \| `float` | Rotation angle in degrees |
| `scale` | `int` \| `float` | *Optional.* Uniform scale factor. Defaults to `1.0` |

### Returns
A new `mat3`.

```python
# built around the origin, so the rotation happens before it's placed
star = shape.star(0, 0, 5, 40, 18)

def update():
  screen.pen = color.black
  screen.clear()

  star.transform = mat3.trs(vec2(80, 60), badge.ticks / 10)

  screen.pen = color.yellow
  screen.shape(star)

run(update)
```

## translate()
Moves the transform by an offset.

### Usage
`.translate(x, y)` \
`.translate(p)`

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Amount to translate by |
| `p` | `vec2` | Amount to translate by |

### Returns
This same `mat3`, translated.

## rotate() / rotate_radians()
Rotates the transform. The angle is in degrees for `rotate()`; to work in radians, use `rotate_radians()`. Positive angles turn clockwise on the badge, since y counts downward.

### Usage
`.rotate(angle)` \
`.rotate_radians(angle)`

| Parameter | Type | Description |
|---|---|---|
| `angle` | `int` \| `float` | Rotation angle, in degrees for `rotate()` or radians for `rotate_radians()` |

### Returns
This same `mat3`, rotated.

## scale()
Scales the transform. Pass one value to scale both axes by it.

### Usage
`.scale(s)` \
`.scale(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `s` | `int` \| `float` | Scale factor for both axes |
| `x`, `y` | `int` \| `float` | Scale factors for the x and y axes |

### Returns
This same `mat3`, scaled.

## multiply()
Composes another matrix onto this one, the same way the methods above do. Use it to apply a transform you've built and kept, a camera for instance, to another.

### Usage
`.multiply(m)`

| Parameter | Type | Description |
|---|---|---|
| `m` | `mat3` | The matrix to compose onto this one |

### Returns
This same `mat3`, multiplied.

## inverse()
Returns a new matrix that undoes this one, leaving this one as it was. Use it to go from a position on screen back to a position in the space you transformed out of, turning a screen position into map coordinates.

A matrix that can't be inverted, which in practice means one that scales an axis to zero, comes back as a copy of itself.

### Usage
`.inverse()`

### Returns
A new `mat3`.

# Operators
| Operator | Result |
|---|---|
| `a * b` | A new `mat3`, the two composed, leaving both alone |

Use it when you want the product without changing either matrix; [`multiply()`](#multiply) would change `a`.

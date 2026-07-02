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

## transform()
Returns a new `vec2` with the specified matrix transformation applied.

### Usage
`.transform(m)`

| Parameter | Type | Description |
|---|---|---|
| `m` | `mat3` | A transformation matrix |

### Returns
A new `vec2` with the transformation applied.

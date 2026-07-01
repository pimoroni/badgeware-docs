---
title: algorithm
summary: High-performance algorithms for common games and graphics programming problems.
icon: function
publish: true
---

# Introduction

MicroPython is a fantastic environment for writing clear, expressive code quickly, but that convenience comes with a performance cost. Certain operations, especially tight loops or math-heavy routines, can become slow when implemented purely in Python.

This section provides fast, low-level implementations of common algorithms that you can drop into your projects whenever you need extra speed without sacrificing the ease of using MicroPython.

> Note: `algorithm` is available globally, so you can call `algorithm.dda(...)` directly — there's no need to import it.

## clip_line
Clips a line segment against a rectangle. The two endpoints (both `vec2`) are updated **in place** to the portion of the line that falls inside the rectangle. Returns `True` if any part of the line is visible, or `False` if the segment lies entirely outside the rectangle.

This is useful for trimming lines to a viewport before drawing them, avoiding wasted work on off-screen geometry.

### Parameters

`clip_line(p1, p2, bounds)`

- `p1` (vec2): Start of the line. Updated in place.
- `p2` (vec2): End of the line. Updated in place.
- `bounds` (rect): The rectangle to clip against.

### Returns

`True` if the (clipped) line is at least partially inside `bounds`, otherwise `False`.

### Example
```python
while True:
  bounds = rect(40, 30, 80, 60)

  # draw the clip region
  screen.pen = color.grey
  screen.shape(shape.rectangle(bounds.x, bounds.y, bounds.w, bounds.h).stroke(1))

  # a line that sweeps around, clipped to the box
  a = badge.ticks / 500
  p1 = vec2(80 + math.cos(a) * 90, 60 + math.sin(a) * 90)
  p2 = vec2(80 - math.cos(a) * 90, 60 - math.sin(a) * 90)

  if algorithm.clip_line(p1, p2, bounds):
    screen.pen = color.lime
    screen.line(p1, p2)

  badge.update()
```

> Note: `import math` is required at the top of the example above.

## DDA Grid Traversal
A fast method for stepping a ray through a uniform grid one cell at a time. Instead of sampling the ray at fixed intervals, the algorithm computes the exact points where the ray crosses the next vertical or horizontal grid line.

By comparing these crossing distances, it determines which neighbouring cell the ray will enter next. This produces a precise, ordered sequence of grid cells intersected by the ray, making the algorithm ideal for tilemaps, voxel engines, raycasting, and visibility systems where efficient cell-by-cell traversal is required.

Returns a list of tuples, each representing where the ray crosses a grid-cell edge.

### Parameters

`dda(point, angle, depth)`

- `point` (vec2): Starting point of the ray (in grid coordinates).
- `angle`: Ray angle in radians.
- `depth`: Maximum distance along the ray to traverse.

### Returns

A list of 5-element tuples containing:
-	`vec2`: The point at which the intersection occurred.
-	`vec2`: The coordinate of the grid square that was entered.
-	`int`: Which edge was crossed (0 = Top, 1 = Right, 2 = Bottom, 3 = Left).
-	`float`: The offset along the crossed edge where the intersection occurred.
-	`float`: The distance along the ray where the intersection occurred.

### Example

Here's an example that casts a short ray and prints all of the intersections:

```python
import math

# convert from grid coordinates to screen coordinates
scale = 16
def grid_to_screen(point):
  return vec2(point.x * scale, point.y * scale)

def draw_grid():
  screen.pen = color.grey
  for y in range(screen.height / scale):
    screen.line(vec2(0, y * scale), vec2(screen.width, y * scale))

  for x in range(screen.width / scale):
    screen.line(vec2(x * scale, 0), vec2(x * scale, screen.height))

while True:
  point = vec2(5.3, 3.4)
  angle = (badge.ticks / 50) * (math.pi / 180)
  depth = 10

  draw_grid()

  # calculate the view vector from the angle
  ray = vec2(math.cos(angle), math.sin(angle))
  ray *= depth

  # draw the ray
  screen.pen = color.taupe
  screen.line(grid_to_screen(point), grid_to_screen(point + ray))

  # draw the origin point
  screen.pen = color.white
  screen.circle(grid_to_screen(point), 3)

  # call the dda algorithm to get intersections
  intersections = algorithm.dda(point, angle, depth)

  # loop through intersections and highlight them
  screen.pen = color.lime
  for intersection in intersections:
    point, square, edge, offset, distance = intersection
    screen.circle(grid_to_screen(point), 2)

  badge.update()
```

## Raycasting
A complete 2D raycaster over a tile map, of the sort used by classic "2.5D" first-person games. It casts a fan of rays across a field of view and, for each ray, returns the walls it hit as it travels through the map. It builds on the same grid traversal as `dda()`, but does the whole per-ray sweep in native code for speed.

The map is a flat byte buffer of `width` × `height` tiles, where a non-zero byte is a solid wall (the value is the wall's texture/type) and `0` is empty space.

### Parameters

`raycast(origin, angle, fov, rays, max_dist, map, width, height, screen_width)`

- `origin` (vec2): The camera position, in tile coordinates.
- `angle`: The direction the camera is facing, in radians.
- `fov`: The field of view, in radians.
- `rays` (int): How many rays to cast across the field of view.
- `max_dist`: The furthest distance a ray will travel before giving up.
- `map` (buffer): A `width` × `height` byte buffer of tiles (`0` = empty, non-zero = wall).
- `width, height` (int): The dimensions of the map, in tiles.
- `screen_width` (int): The width of the screen the result will be drawn to, used to compute per-column positions.

### Returns

A tuple with one entry per ray. Each entry is a list of hit tuples along that ray (the same shape of data returned by `dda()`), letting you draw walls back-to-front for correct occlusion.

# Reference

## Static Methods
```python-raw
algorithm.clip_line(p1: vec2, p2: vec2, bounds: rect) -> bool
algorithm.dda(origin: vec2, angle: int|float, depth: int|float) -> list
algorithm.raycast(origin: vec2, angle: float, fov: float, rays: int, max_dist: float, map: buffer, width: int, height: int, screen_width: int) -> tuple
```
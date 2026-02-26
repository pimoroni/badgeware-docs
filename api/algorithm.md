---
title: algorithm
summary: High-performance algorithms for common games and graphics programming problems.
icon: function
publish: true
---

# Introduction

MicroPython is a fantastic environment for writing clear, expressive code quickly, but that convenience comes with a performance cost. Certain operations, especially tight loops or math-heavy routines, can become slow when implemented purely in Python.

This section provides fast, low-level implementations of common algorithms that you can drop into your projects whenever you need extra speed without sacrificing the ease of using MicroPython.

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
from picovector import algorithm

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

def update():
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

run(update)
```
---
title: algorithm
summary: High-performance algorithms for common games and graphics programming problems.
icon: function
publish: true
---

# Introduction

MicroPython is a fantastic environment for writing clear, expressive code quickly, but that convenience comes with a performance cost. Certain operations, especially tight loops or math-heavy routines, can become slow when implemented purely in Python.

This section provides fast, low-level implementations of common algorithms that you can drop into your projects whenever you need extra speed without sacrificing the ease of using MicroPython.

## clip_line()
Trims a line segment so it fits inside a rectangle. The two points are updated **in place**, so pass copies if you still need the originals.

A segment lying entirely outside the rectangle can't be trimmed to fit, so check the return value before drawing.

### Usage
`algorithm.clip_line(p1, p2, bounds)`

| Parameter | Type | Description |
|---|---|---|
| `p1` | `vec2` | Start of the segment. Updated in place |
| `p2` | `vec2` | End of the segment. Updated in place |
| `bounds` | `rect` | The rectangle to clip against |

### Returns
`True` if any part of the segment falls inside `bounds`, with `p1` and `p2` moved onto its edges. `False` if the segment misses the rectangle, in which case `p1` and `p2` are left alone.

```python
def update():
  bounds = rect(10, 10, 140, 100)

  screen.pen = color.grey
  screen.shape(shape.rectangle(bounds))

  p1 = vec2(0, 60)
  p2 = vec2(160, 20 + (badge.ticks // 20) % 80)

  screen.pen = color.lime
  if algorithm.clip_line(p1, p2, bounds):
    screen.line(p1, p2)

run(update)
```

## DDA Grid Traversal
A fast method for stepping a ray through a uniform grid one cell at a time. Instead of sampling the ray at fixed intervals, the algorithm computes the exact points where the ray crosses the next vertical or horizontal grid line.

By comparing these crossing distances, it determines which neighbouring cell the ray will enter next. This produces a precise, ordered sequence of grid cells intersected by the ray, making the algorithm ideal for tilemaps, voxel engines, raycasting, and visibility systems where efficient cell-by-cell traversal is required.

Returns a list of tuples, each representing where the ray crosses a grid-cell edge.

### Usage
`algorithm.dda(point, angle, depth)`

| Parameter | Type | Description |
|---|---|---|
| `point` | `vec2` | Starting point of the ray (in grid coordinates) |
| `angle` | `float` | Ray angle in radians |
| `depth` | `float` | Maximum distance along the ray to traverse |

### Returns

A list of 5-element tuples containing:
-	`vec2`: The point at which the intersection occurred.
-	`vec2`: The coordinate of the grid square that was entered.
-	`int`: Which edge was crossed (0 = Top, 1 = Right, 2 = Bottom, 3 = Left).
-	`float`: The offset along the crossed edge where the intersection occurred.
-	`float`: The distance along the ray where the intersection occurred.

Here's an example that casts a short ray and prints all of the intersections:

```python
import math

# convert from grid coordinates to screen coordinates
scale = 16
def grid_to_screen(point):
  return vec2(point.x * scale, point.y * scale)

def draw_grid():
  screen.pen = color.grey
  for y in range(screen.height // scale):
    screen.line(vec2(0, y * scale), vec2(screen.width, y * scale))

  for x in range(screen.width // scale):
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
    hit, square, edge, offset, distance = intersection
    screen.circle(grid_to_screen(hit), 2)

run(update)
```

## raycast()
Casts a fan of rays across a tilemap in one call, which is the heavy inner loop of a first-person raycaster. It runs `dda()` for every ray and reports only the cells that hold a non-zero tile.

Rays are spread to match screen columns rather than spaced evenly by angle, so ray `i` belongs to the vertical strip at `x = (i + 0.5) * screen_width / rays`. The distance it reports is already corrected for the fisheye distortion that an unadjusted ray distance would give you.

A tile value below `128` is recorded and the ray keeps going, which is how you get see-through tiles like glass or a grating. A value of `128` or above stops the ray.

### Usage
`algorithm.raycast(origin, angle, fov, rays, max_dist, map, width, height, screen_width)`

| Parameter | Type | Description |
|---|---|---|
| `origin` | `vec2` | The viewer's position, in grid coordinates |
| `angle` | `float` | The direction the viewer faces, in radians |
| `fov` | `float` | Field of view, in radians |
| `rays` | `int` | How many rays to cast. One per screen column is typical |
| `max_dist` | `int` | How far along each ray to travel before giving up |
| `map` | `bytearray` | The tilemap, one byte per cell, `width * height` bytes long. `0` is empty |
| `width`, `height` | `int` | The tilemap dimensions in cells |
| `screen_width` | `int` | Width the fan is projected across, used to place the rays |

### Returns
A `tuple` holding one list per ray, ordered left to right. Each list holds a 7-element tuple for every non-empty cell that ray passed through:

- `int`: The tile value found in the map.
- `vec2`: The point at which the ray entered the cell.
- `vec2`: The coordinate of the cell.
- `int`: Which edge was crossed (0 = Top, 1 = Right, 2 = Bottom, 3 = Left).
- `float`: The offset along the crossed edge, useful as a texture coordinate.
- `float`: The perpendicular distance, corrected for fisheye.
- `float`: The angle of this ray, in radians.

A ray that hits nothing gives an empty list.

```python
import math

MAP_W, MAP_H = 8, 8
world = bytearray(
  b'\x01\x01\x01\x01\x01\x01\x01\x01'
  b'\x01\x00\x00\x00\x00\x00\x00\x01'
  b'\x01\x00\x00\x01\x00\x00\x00\x01'
  b'\x01\x00\x00\x00\x00\x00\x00\x01'
  b'\x01\x00\x00\x00\x00\x01\x00\x01'
  b'\x01\x00\x00\x00\x00\x00\x00\x01'
  b'\x01\x00\x00\x00\x00\x00\x00\x01'
  b'\x01\x01\x01\x01\x01\x01\x01\x01')

fov = math.radians(60)
d_proj = (screen.width / 2) / math.tan(fov / 2)

def update():
  screen.pen = color.rgb(20, 24, 40)
  screen.clear()

  angle = badge.ticks / 1000
  rays = algorithm.raycast(vec2(4.5, 4.5), angle, fov, screen.width, 16,
                           world, MAP_W, MAP_H, screen.width)

  # one wall strip per screen column, nearer walls drawn brighter
  for x, ray in enumerate(rays):
    if not ray:
      continue

    # the first entry is the nearest wall this ray met
    tile, hit, cell, edge, offset, distance, ray_angle = ray[0]

    height = d_proj / distance
    shade = max(0, 255 - int(distance * 40))
    screen.pen = color.rgb(shade, shade, shade)
    screen.rectangle(x, (screen.height - height) / 2, 1, height)

run(update)
```
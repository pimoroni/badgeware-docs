---
title: Casting rays
summary: The DDA algorithm that finds where a ray hits a wall — built and shown from above.
sort: 2
publish: true
---
# One ray at a time

Everything a raycaster draws comes from one question, asked over and over: *starting at the player and heading in some direction, how far do I travel before I hit a wall?* Answer that, and the 3D view falls out almost for free. So this part is entirely about casting a single ray — and then a whole fan of them — while still looking down on the map from above, where we can actually watch it work.

The lazy way to find a wall would be to creep along the ray in tiny steps — `0.01` of a cell at a time — checking the map at each point until we land in a wall. It works, but it's wasteful (thousands of checks per ray) and it can miss a thin wall by stepping right over it. There's a much better way that takes advantage of the fact that walls always sit on a **grid**.

# Stepping along the grid

Here's the insight: a ray can only enter a new cell by crossing one of the grid lines — a vertical line (moving into the next column) or a horizontal one (moving into the next row). So instead of inching along, we jump straight from one grid line to the next, and at each jump check whether the cell we've entered is a wall. A ray crossing an 8-cell map hits a wall in a handful of jumps, not hundreds of tiny steps. This is the **DDA** — Digital Differential Analysis — and it's the classic raycasting workhorse.

To do it we track two races at once: how far along the ray to the **next vertical** grid line, and how far to the **next horizontal** one. Whichever is closer, we take that jump, step into the neighbouring cell, and then top that race back up. Repeat until the cell we step into is solid.

Two quantities set it all up. First, for a ray direction `(rayx, rayy)`, how far along the ray you travel to cross one *whole* cell horizontally is `abs(1 / rayx)`, and vertically `abs(1 / rayy)` — a shallow ray covers a lot of ground between vertical lines, a steep one very little:

```python-raw
ddx = abs(1 / rayx) if rayx != 0 else 1e30     # ray-distance to cross one column
ddy = abs(1 / rayy) if rayy != 0 else 1e30     # ray-distance to cross one row
```

(The `1e30` guards against a perfectly straight ray, where `rayx` or `rayy` is `0` and we'd divide by zero — we just call that distance "enormous".)

Second, the distance to the *first* grid line depends on where in the starting cell the player is standing, and which way the ray points. If the ray heads left (`rayx < 0`) the next vertical line is the left edge of the current cell; if it heads right, it's the right edge of the next one:

```python-raw
mapx, mapy = int(px), int(py)                  # the cell the player starts in

if rayx < 0:
  stepx = -1; sidex = (px - mapx) * ddx        # heading left
else:
  stepx = 1;  sidex = (mapx + 1 - px) * ddx    # heading right
if rayy < 0:
  stepy = -1; sidey = (py - mapy) * ddy        # heading up
else:
  stepy = 1;  sidey = (mapy + 1 - py) * ddy    # heading down
```

`sidex` and `sidey` are the running distances-to-the-next-line. `stepx`/`stepy` say which way to move through the grid (`+1` or `-1`). Now the loop itself: take whichever line is nearer, step, and top up that side's distance by one full cell's worth:

```python-raw
side = 0                                       # 0 = we crossed a vertical line, 1 = horizontal
while True:
  if sidex < sidey:
    sidex += ddx; mapx += stepx; side = 0      # the vertical line was closer — step in x
  else:
    sidey += ddy; mapy += stepy; side = 1      # the horizontal line was closer — step in y
  if MAP[mapy][mapx] != " ":                   # stepped into a wall? done.
    break
```

When it stops, we've walked into a wall cell — and the distance to it is simply whichever side-distance we *last* extended, minus the one cell we overshot by:

```python-raw
dist = (sidex - ddx) if side == 0 else (sidey - ddy)
```

That's the answer to our question. Notice we never touched a square root or a trig function inside the loop — DDA is all comparisons and additions, which is exactly why it's fast enough to run 160 times a frame.

# Finding the hit point

For the 3D view we'll only want `dist`, but to *draw* a ray from above we also want the actual point where it lands. Because our ray direction `(rayx, rayy)` is scaled so that travelling `dist` along it lands exactly on the wall, the hit point is just:

```python-raw
hx = px + rayx * dist
hy = py + rayy * dist
```

We'll bundle the DDA into a `cast(rayx, rayy)` function that returns `dist`, and let the caller work out the hit point.

# A fan of rays

Now, which directions do we cast in? A camera has a **field of view** — it sees a wedge of the world, not just straight ahead. We build that wedge from two vectors: the direction the player faces, `dir = (cos(angle), sin(angle))`, and a **camera plane** at right angles to it. Sweeping a value `camera` from `-1` (far left of view) to `+1` (far right) and mixing the two gives every ray across the screen:

```python-raw
dirx, diry = math.cos(angle), math.sin(angle)
planex, planey = -diry * 0.66, dirx * 0.66     # perpendicular to dir; 0.66 sets the ~66° FOV
# ...for a column from left (-1) to right (+1) of the view:
rayx = dirx + planex * camera
rayy = diry + planey * camera
```

Rotating a vector 90° is just `(x, y) → (-y, x)`, which is where `planex, planey = -diry, dirx` comes from; scaling it by `0.66` sets how wide the wedge opens — a bigger number is a wider, more fish-eyed field of view.

Here it is all together: the top-down map from Part 1, with a fan of rays cast across the field of view, each drawn from the player to the wall it strikes. Watch them stretch and shorten as the view slowly turns.

```python {expanded}
import math

MAP = [
  "########",
  "#      #",
  "#  ##  #",
  "#  ##  #",
  "#      #",
  "#    ###",
  "#      #",
  "########",
]
MW, MH = len(MAP[0]), len(MAP)
CELL = 14
OX = (screen.width - MW * CELL) // 2
OY = (screen.height - MH * CELL) // 2

px, py = 3.5, 4.5
angle = 0.0

RAYS = 48          # how many rays to draw across the field of view
FOV = 0.66         # camera-plane length; larger = wider view

# walk the grid line-to-line until we hit a wall, and return the distance
def cast(rayx, rayy):
  mapx, mapy = int(px), int(py)
  ddx = abs(1 / rayx) if rayx != 0 else 1e30
  ddy = abs(1 / rayy) if rayy != 0 else 1e30
  if rayx < 0:
    stepx = -1; sidex = (px - mapx) * ddx
  else:
    stepx = 1;  sidex = (mapx + 1 - px) * ddx
  if rayy < 0:
    stepy = -1; sidey = (py - mapy) * ddy
  else:
    stepy = 1;  sidey = (mapy + 1 - py) * ddy
  side = 0
  while True:
    if sidex < sidey:
      sidex += ddx; mapx += stepx; side = 0
    else:
      sidey += ddy; mapy += stepy; side = 1
    if MAP[mapy][mapx] != " ":
      break
  return (sidex - ddx) if side == 0 else (sidey - ddy)

while True:
  angle += 0.01                                # slowly turn so we can watch the fan sweep

  screen.pen = color.rgb(18, 20, 28); screen.clear()
  for my in range(MH):
    for mx in range(MW):
      screen.pen = color.rgb(78, 92, 128) if MAP[my][mx] != " " else color.rgb(32, 36, 48)
      screen.rectangle(OX + mx * CELL + 1, OY + my * CELL + 1, CELL - 2, CELL - 2)

  # build the field of view, then cast one ray per step across it
  dirx, diry = math.cos(angle), math.sin(angle)
  planex, planey = -diry * FOV, dirx * FOV
  for i in range(RAYS):
    camera = 2 * i / (RAYS - 1) - 1            # -1 at the left of view, +1 at the right
    rayx = dirx + planex * camera
    rayy = diry + planey * camera
    dist = cast(rayx, rayy)
    hx = px + rayx * dist                      # where this ray struck a wall
    hy = py + rayy * dist
    screen.pen = color.rgb(230, 170, 60)
    screen.line(OX + px * CELL, OY + py * CELL, OX + hx * CELL, OY + hy * CELL)

  screen.pen = color.orange
  screen.circle(OX + int(px * CELL), OY + int(py * CELL), 3)
  badge.update()
```

That fan *is* the raycaster — every ray already knows how far away its wall is. We're only drawing 48 of them here so the lines stay separate enough to see; in the real view we'll cast one per screen column, all 160 of them.

In the [next part](03_rendering_walls.md) comes the payoff: instead of drawing each ray flat on the map, we'll use its distance to draw a vertical slice of wall — and the map stands up into 3D.

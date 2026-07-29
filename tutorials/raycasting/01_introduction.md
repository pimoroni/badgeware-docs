---
title: Introduction
summary: The idea behind raycasting, and the map we'll walk around.
sort: 1
publish: true
---
# The big idea

A raycaster turns a flat 2D map into what looks like a 3D world. The trick is to think about the screen one **vertical column of pixels at a time**. For each column, we send out a single ray from the player, across the map, until it hits a wall. The *distance* the ray travelled tells us how tall to draw that column's slice of wall: a close wall fills the screen, a far one is just a sliver near the middle. Do that for all 160 columns and the slices line up into walls, corners and corridors.

That's the whole idea. There's no real 3D geometry anywhere — no polygons, no perspective matrices — just a grid, some rays, and a rule that says *nearer means taller*. It was the beating heart of *Wolfenstein 3D* in 1992, and it's still a brilliant thing to build today: fast enough for the badge, and satisfying at every step.

We'll get there in stages. Before any of the 3D, though, we need something to walk around in — so this part is about the map, and drawing it from above so we can see what we're dealing with.

# The map

Our world is a grid of cells. Each cell is either empty (you can stand there) or solid (a wall). The simplest way to write that down is as a list of strings — a `#` for a wall, a space for empty floor:

```python-raw
MAP = [
  "################",
  "#      #       #",
  "#  ##  #  ###  #",
  "#  ##  #  # #  #",
  "#      #  # #  #",
  "#         #    #",
  "####  ##  #  ###",
  "#     ##     # #",
  "#  ##     #    #",
  "#  ##  #  #  # #",
  "#      #      ##",
  "################",
]
```

Read as a grid, `MAP[y][x]` is the cell in row `y`, column `x`. So `MAP[0][0]` is the top-left corner (a wall), and `MAP[4][3]` is a bit of floor. The outer ring is solid so the player can never escape the world, and inside it there's a warren of little rooms, corridors and free-standing pillars — plenty of corners and doorways to send rays at.

Storing the map as text has a lovely side benefit: you can *see* the level right there in your code, and editing it is as easy as typing. Later on we'll only ever ask one question of the map — "is the cell at `(x, y)` a wall?" — which is just `MAP[y][x] != " "`.

# The player

The player needs two things: a **position** and a **direction**. The position is a point somewhere on the map, and because a player can stand *between* cells it's stored as floating-point numbers rather than whole cells — `px, py = 3.5, 4.5` puts them in the middle of a floor tile. The direction is just an angle, in radians, that we can turn later:

```python-raw
px, py = 3.5, 4.5     # position, in map cells (floats, so we can stand mid-cell)
angle = -0.6          # facing direction, in radians
```

From an angle, the *unit vector* pointing that way is `(cos(angle), sin(angle))` — a step of length 1 in the direction we're facing. We'll lean on that constantly: it's how we move forward, and how we aim rays.

# Seeing it from above

Let's draw the map top-down so we've got our bearings. We'll pick a `CELL` size in pixels, centre the grid on the screen, and draw a filled square for every cell — walls brighter than floor. Then we drop the player on as an orange dot, with a yellow line showing which way they face.

```python {expanded}
import math

MAP = [
  "################",
  "#      #       #",
  "#  ##  #  ###  #",
  "#  ##  #  # #  #",
  "#      #  # #  #",
  "#         #    #",
  "####  ##  #  ###",
  "#     ##     # #",
  "#  ##     #    #",
  "#  ##  #  #  # #",
  "#      #      ##",
  "################",
]
MW, MH = len(MAP[0]), len(MAP)     # map width and height, in cells

CELL = 9                                     # pixels per map cell in this top-down view
OX = (screen.width - MW * CELL) // 2         # offsets to centre the map on screen
OY = (screen.height - MH * CELL) // 2

px, py = 3.5, 4.5                            # player position, in map cells
angle = -0.6                                 # facing direction, in radians

while True:
  screen.pen = color.rgb(18, 20, 28); screen.clear()

  # draw the map: a filled square for every cell, walls brighter than floor
  for my in range(MH):
    for mx in range(MW):
      if MAP[my][mx] != " ":
        screen.pen = color.rgb(78, 92, 128)
      else:
        screen.pen = color.rgb(32, 36, 48)
      screen.rectangle(OX + mx * CELL + 1, OY + my * CELL + 1, CELL - 2, CELL - 2)

  # the player, plus a line showing which way they face
  ex = px + math.cos(angle) * 1.4            # a point 1.4 cells ahead of the player
  ey = py + math.sin(angle) * 1.4
  screen.pen = color.yellow
  screen.line(OX + px * CELL, OY + py * CELL, OX + ex * CELL, OY + ey * CELL)
  screen.pen = color.orange
  screen.circle(OX + int(px * CELL), OY + int(py * CELL), 3)

  badge.update()
```

Notice how the facing line is built: `math.cos(angle)` and `math.sin(angle)` give the direction, we scale it by `1.4` cells to get a point out in front, and draw a line to it. That exact move — *take the direction, scale it, add it to the position* — is the one we'll use to cast rays and to walk around.

Everything multiplies map coordinates by `CELL` and adds the `OX`/`OY` offsets to turn "cells" into "screen pixels". That's only for this top-down preview; the 3D view we build next won't need it, because there the distance *is* the size.

We've got a world and someone standing in it. In the [next part](02_casting_rays.md) we'll fire a ray out from that orange dot and work out exactly where it hits a wall — the algorithm that makes the whole thing possible.

---
title: Raycasting a 3D world
summary: Build a Wolfenstein-style 3D engine, one ray at a time — from a flat map to textured walls under a sky.
icon: deployed_code
sort: 2
publish: true
---
# Raycasting a 3D world

Long before hardware could push real 3D, games like *Wolfenstein 3D* faked it with a trick called **raycasting**: for every vertical column of the screen, shoot a single ray out across a flat 2D map, see how far it travels before it hits a wall, and draw a wall slice whose height depends on that distance. Near walls draw tall, far walls draw short, and your eye reads the result as a 3D corridor — even though the whole world is really just a grid drawn on paper.

It's a wonderful thing to build. The maths is mostly a bit of trigonometry and some careful bookkeeping, it runs comfortably on the badge, and the moment the flat map first "stands up" into a 3D view is genuinely magic. Over these six parts we'll build the whole thing from scratch:

- **Introduction** — the idea, and the map we'll walk around
- **Casting rays** — the algorithm that measures wall distances, shown from above
- **Rendering walls** — standing the map up into a 3D view
- **Moving around** — driving the camera with the buttons, without walking through walls
- **Texturing the walls** — painting brickwork onto the wall slices
- **Sky and floor** — finishing the scene above and below the walls

Here's where we'll end up — textured walls receding into the distance, with a sky and floor:

```simulator
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
W, H = screen.width, screen.height

TS = 64
tex = image(TS, TS)
tex.pen = color.rgb(150, 74, 56); tex.clear()
tex.pen = color.rgb(46, 30, 28)
for y in range(0, TS, 16):
  tex.rectangle(0, y, TS, 2)
for r in range(TS // 16):
  off = 0 if r % 2 == 0 else 16
  for x in range(off, TS + 32, 32):
    tex.rectangle(x, r * 16, 2, 16)

FOG = color.rgb(28, 28, 38)
px, py = 3.5, 4.5
angle = 0.0

@micropython.native
def render():
  dirx, diry = math.cos(angle), math.sin(angle)
  planex, planey = -diry * 0.66, dirx * 0.66
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 0, H // 2, [(0.0, color.rgb(10, 12, 26)), (1.0, color.rgb(58, 52, 74))])
  screen.rectangle(0, 0, W, H // 2)
  screen.pen = brush.gradient(brush.LINEAR, 0, H // 2, 0, H, [(0.0, color.rgb(44, 38, 32)), (1.0, color.rgb(14, 13, 12))])
  screen.rectangle(0, H // 2, W, H - H // 2)
  for x in range(W):
    camera = 2 * x / W - 1
    rayx = dirx + planex * camera
    rayy = diry + planey * camera
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
    dist = (sidex - ddx) if side == 0 else (sidey - ddy)
    if dist < 0.0001: dist = 0.0001
    height = H / dist
    top = (H - height) / 2
    if side == 0:
      u = py + dist * rayy
    else:
      u = px + dist * rayx
    u -= int(u)
    if side == 0 and rayx > 0: u = 1 - u
    if side == 1 and rayy < 0: u = 1 - u
    y0 = math.floor(top)
    y1 = math.ceil(top + height)
    screen.blit_vspan(tex, x, y0, y1 - y0, u, (y0 - top) / height, u, (y1 - top) / height)
    fog = int(dist * 26)
    if side == 1: fog += 40
    if fog > 205: fog = 205
    screen.pen = FOG
    screen.alpha = fog
    screen.rectangle(x, top, 1, height)
    screen.alpha = 255

while True:
  angle += 0.012
  render()
  badge.update()
```

Ready? Let's start with the map.

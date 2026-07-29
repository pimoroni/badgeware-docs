---
title: Sky and floor
summary: Fill in the world above and below the walls, and complete the scene.
sort: 6
publish: true
---
# Above and below

Our walls float in a flat grey void. The last step is to fill in everything the walls *don't* cover — the sky above the horizon and the floor below it — and suddenly the room has a top and a bottom, and feels like somewhere you could stand.

There's a lovely shortcut hiding in how a raycaster draws. Every wall slice is centred on the middle of the screen, so the horizon always sits at the halfway line, `H / 2`. That means the top half of the screen is *always* sky and the bottom half is *always* floor — wherever a wall doesn't reach. So if we paint the sky across the top half and the floor across the bottom half **before** we draw any walls, the wall slices simply cover the middle band, and whatever's left showing is correctly sky or floor. No per-pixel work, no cleverness.

# A sky and a floor

We could fill each half with a flat colour, but a gradient does so much more for the mood — and we've already got `brush.gradient` from the [brushes guide](../api/brush.md). For the sky, we run dark at the very top to a lighter, warmer band at the horizon, like a night sky catching some distant glow. For the floor, we go the other way: brighter close to us at the bottom of the screen, fading to dark as it reaches the horizon:

```python-raw
def draw_sky_floor():
  # sky fills the top half: dark up high, lifting toward the horizon
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 0, H // 2,
                              [(0.0, color.rgb(10, 12, 26)), (1.0, color.rgb(58, 52, 74))])
  screen.rectangle(0, 0, W, H // 2)
  # floor fills the bottom half: brighter near us, dark toward the horizon
  screen.pen = brush.gradient(brush.LINEAR, 0, H // 2, 0, H,
                              [(0.0, color.rgb(44, 38, 32)), (1.0, color.rgb(14, 13, 12))])
  screen.rectangle(0, H // 2, W, H - H // 2)
```

Each gradient runs vertically — its start and end points share an `x` and differ only in `y` — so the colour changes purely top-to-bottom. Then it's two filled rectangles, one per half. In the main loop this replaces the old `screen.clear()`: we call `draw_sky_floor()` first, then `render()` paints the walls over the middle.

# The finished raycaster

Here's everything, all six parts of it, in one program: a textured, walkable room under a night sky. Take it for a final wander.

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
W, H = screen.width, screen.height

# build a 64x64 brick texture once, into an off-screen image
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
MOVE = 0.04
TURN = 0.03

def try_move(nx, ny):
  global px, py
  if MAP[int(py)][int(nx)] == " ": px = nx
  if MAP[int(ny)][int(px)] == " ": py = ny

def draw_sky_floor():
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 0, H // 2,
                              [(0.0, color.rgb(10, 12, 26)), (1.0, color.rgb(58, 52, 74))])
  screen.rectangle(0, 0, W, H // 2)
  screen.pen = brush.gradient(brush.LINEAR, 0, H // 2, 0, H,
                              [(0.0, color.rgb(44, 38, 32)), (1.0, color.rgb(14, 13, 12))])
  screen.rectangle(0, H // 2, W, H - H // 2)

@micropython.native
def render():
  dirx, diry = math.cos(angle), math.sin(angle)
  planex, planey = -diry * 0.66, dirx * 0.66
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

    # snap the span to whole rows (a touch too tall, clipped for free) and give
    # the exact texture v at each end, so the brick stays locked and can't comb
    y0 = math.floor(top)
    y1 = math.ceil(top + height)

    v0 = 0
    v1 = 1

    if top < 0:
      v0 = abs(top) / height
      height += top
      top = 0

    if height > 120:
      v1 -= (height - 120) / height
      height = 120

    screen.blit_vspan(tex, x, top, height, u, v0, u, v1)

    fog = int(dist * 26)
    if side == 1: fog += 40
    if fog > 205: fog = 205
    screen.pen = FOG
    screen.alpha = fog
    screen.rectangle(x, top, 1, height)
    screen.alpha = 255

screen.font = rom_font.nope

while True:
  dirx, diry = math.cos(angle), math.sin(angle)
  if badge.held(BUTTON_UP):   try_move(px + dirx * MOVE, py + diry * MOVE)
  if badge.held(BUTTON_DOWN): try_move(px - dirx * MOVE, py - diry * MOVE)
  if badge.held(BUTTON_A):    angle -= TURN
  if badge.held(BUTTON_C):    angle += TURN

  draw_sky_floor()
  render()

  screen.pen = color.white
  screen.text("A/C turn   UP/DOWN move", 6, 108)
  badge.update()
```

# Where to take it next

You've built a complete raycasting engine from nothing but a grid of text — and it's a springboard for plenty more:

- **A textured floor and ceiling.** Our sky and floor are flat gradients. The same casting idea can be run *per floor pixel* to paint a tiled texture stretching to the horizon — a great excuse to reach for `@micropython.viper`, as covered in [Pushing pixels](../guides/performance.md).
- **Different walls.** The map stores a character per cell, and right now we only ask *"wall or not?"*. Read the actual character and pick a different texture for `#` versus, say, `=`, and you've got a varied level.
- **A mini-map.** You already wrote a top-down renderer back in [Part 1](01_introduction.md) — draw it small in a corner over the 3D view and you've got a HUD.
- **Sprites and enemies.** Objects in a raycaster are billboarded sprites, drawn after the walls and sorted by distance so nearer ones cover farther ones — the natural next step toward an actual game.

Whatever you build, it all rests on the one idea we started with: for every column of the screen, cast a ray, measure the distance, and draw a slice. Everything else is decoration. Happy casting.

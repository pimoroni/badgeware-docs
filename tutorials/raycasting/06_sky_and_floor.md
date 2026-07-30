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

# the level, laid out as text: '#' is a wall, ' ' is empty floor
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
W, H = screen.width, screen.height   # one ray — and one wall slice — per column

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

# player state and movement speeds
FOG = color.rgb(28, 28, 38)     # the murk distant walls fade into
px, py = 3.5, 4.5               # player position, in cells
angle = 0.0                     # direction the player faces, in radians
MOVE = 2.4                      # cells moved per second while walking
TURN = 1.8                      # radians turned per second

# move on each axis only if its target cell is empty, so we slide along walls
def try_move(nx, ny):
  global px, py
  if MAP[int(py)][int(nx)] == " ": px = nx
  if MAP[int(ny)][int(px)] == " ": py = ny

# fill the top half with a sky gradient and the bottom half with a floor one
def draw_sky_floor():
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 0, H // 2,
                              [(0.0, color.rgb(10, 12, 26)), (1.0, color.rgb(58, 52, 74))])
  screen.rectangle(0, 0, W, H // 2)
  screen.pen = brush.gradient(brush.LINEAR, 0, H // 2, 0, H,
                              [(0.0, color.rgb(44, 38, 32)), (1.0, color.rgb(14, 13, 12))])
  screen.rectangle(0, H // 2, W, H - H // 2)

# the DDA from Part 2 — walk the grid until we hit a wall — now also
# returning which face we struck, so we can map and shade it
@micropython.native
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
  dist = (sidex - ddx) if side == 0 else (sidey - ddy)
  return dist, side

@micropython.native
def render():
  dirx, diry = math.cos(angle), math.sin(angle)
  planex, planey = -diry * 0.66, dirx * 0.66
  for x in range(W):
    camera = 2 * x / W - 1
    rayx = dirx + planex * camera
    rayy = diry + planey * camera

    dist, side = cast(rayx, rayy)              # how far to the wall, and which face
    if dist < 0.0001: dist = 0.0001
    height = H / dist                          # nearer wall -> taller slice
    top = (H - height) / 2

    # where along the wall the ray struck -> texture column u (0..1)
    if side == 0:
      u = py + dist * rayy
    else:
      u = px + dist * rayx
    u -= int(u)
    if side == 0 and rayx > 0: u = 1 - u
    if side == 1 and rayy < 0: u = 1 - u

    # paint that column down the slice, snapped to whole rows so it can't comb
    y0 = math.floor(top)
    y1 = math.ceil(top + height)
    screen.blit_vspan(tex, x, y0, y1 - y0, u, (y0 - top) / height, u, (y1 - top) / height)

    # fog: a translucent wash over the slice that thickens with distance
    fog = int(dist * 26)
    if side == 1: fog += 40
    if fog > 205: fog = 205
    screen.pen = FOG
    screen.alpha = fog
    screen.rectangle(x, top, 1, height)
    screen.alpha = 255

screen.font = font.nope

while True:
  # scale movement by frame time, so speed is the same at any framerate
  dt = badge.ticks_delta / 1000
  move, turn = MOVE * dt, TURN * dt

  # drive the player from the buttons: A/C turn, UP/DOWN walk (blocked by walls)
  dirx, diry = math.cos(angle), math.sin(angle)
  if badge.held(BUTTON_UP):   try_move(px + dirx * move, py + diry * move)
  if badge.held(BUTTON_DOWN): try_move(px - dirx * move, py - diry * move)
  if badge.held(BUTTON_A):    angle -= turn
  if badge.held(BUTTON_C):    angle += turn

  # sky and floor first, then the walls drawn over the middle band
  draw_sky_floor()
  render()

  # a small on-screen controls hint
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

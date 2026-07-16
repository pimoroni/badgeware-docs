---
title: Texturing the walls
summary: Paint brickwork onto every wall slice, mapped correctly with perspective.
sort: 5
publish: true
---
# From flat colour to brick

Grey walls prove the geometry works; textures make it a *place*. The plan is to give each wall slice a strip of an image — a brick texture — instead of a flat shade. Two things make that possible: knowing exactly *where along a wall* each ray struck, so we sample the right column of the texture, and a drawing helper that paints a whole texture column into a slice, scaled with perspective, in one fast call.

# A texture to paint with

We could load a `.png`, but a brick pattern is so regular we can just draw one, once, into a small off-screen image at startup. We make a 64×64 `image`, flood it with brick red, then lay down darker mortar: a horizontal line every 16 pixels for the courses, and short vertical joints staggered on alternate rows so the bricks interlock like real brickwork:

```python-raw
TS = 64
tex = image(TS, TS)
tex.pen = color.rgb(150, 74, 56); tex.clear()      # brick red
tex.pen = color.rgb(46, 30, 28)                    # mortar
for y in range(0, TS, 16):
  tex.rectangle(0, y, TS, 2)                        # horizontal courses
for r in range(TS // 16):
  off = 0 if r % 2 == 0 else 16                     # stagger every other row
  for x in range(off, TS + 32, 32):
    tex.rectangle(x, r * 16, 2, 16)                 # vertical joints
```

Because `tex` is just an `image`, all the normal drawing methods work on it — we're using the same `rectangle()` we've been drawing walls with, only aimed at our own little canvas instead of the screen.

# Where did the ray hit?

To pick the right column of the texture, we need the fractional position where the ray met the wall — `0.0` at one edge of a cell, `1.0` at the other. Whichever grid line the DDA crossed last tells us: for a wall hit on a vertical line we take the *y* of the hit point, on a horizontal line the *x*, and keep only the fractional part:

```python-raw
if side == 0:
  u = py + dist * rayy      # hit a vertical wall face — position along it is the y coordinate
else:
  u = px + dist * rayx      # hit a horizontal face — use x
u -= int(u)                 # keep just the fraction, 0..1 across the brick
```

That `u` is the texture's horizontal coordinate — its *u* in the 0–1 range textures are addressed by. One tidy-up: walls facing opposite directions would otherwise show the brick mirror-imaged, so we flip `u` on two of the four facings to keep the pattern consistent:

```python-raw
if side == 0 and rayx > 0: u = 1 - u
if side == 1 and rayy < 0: u = 1 - u
```

# Painting the slice

Now the satisfying bit. We want to take the single column of the texture at `u` and stretch it down the whole height of the wall slice — near walls stretch it tall, far walls squash it short. Doing that pixel-by-pixel in Python would be painfully slow, so Badgeware gives us `blit_vspan()`, which draws a **vertical span** sampled from a source image, scaling as it goes — all in fast C:

```python-raw
screen.blit_vspan(tex, x, top, height, u, 0, u, 1)
```

Reading the arguments: draw into column `x` starting at `top`, for `height` pixels, sampling the texture from `(u, 0)` at the top to `(u, 1)` at the bottom — i.e. straight down the texture column at our `u`. Because it samples across the *full* requested height and clips whatever falls off-screen, near walls whose slices overshoot the display are handled for free, with the perspective still correct. One call replaces the whole flat strip.

There's one subtlety that separates crisp brickwork from a shimmering mess. `blit_vspan` draws its span between whole pixel rows — it snaps the `top` we hand it down to an integer. On a receding wall every column's *true* top has a different fractional part, so that snapping shifts the texture by a slightly different amount in each column, and horizontal features (the mortar!) comb up and down from one column to the next.

The cure is to stop fighting the snapping and work with it. We draw a span that already sits on whole pixels — from `floor(top)` down to `ceil(top + height)`, a touch taller than the wall — and tell `blit_vspan` the exact texture `v` coordinate at each of those two integer rows. Because `v` is interpolated linearly between them, every pixel row in between lands on precisely the right part of the texture, so the brick stays locked to the wall however the grid falls. The small overhang top and bottom just gets clipped away for free:

```python-raw
y0 = math.floor(top)              # snap the span to whole rows...
y1 = math.ceil(top + height)      # ...a touch taller than the wall itself
# ...and give the exact texture v at each end, so the fill can't drift
screen.blit_vspan(tex, x, y0, y1 - y0, u, (y0 - top) / height, u, (y1 - top) / height)
```

Keeping `top` and `height` fractional matters here — those exact values are what the `v` coordinates are measured against. (Very distant walls still soften a touch, since a mortar line thinner than a pixel simply can't be drawn in full, but the combing is gone.)

# Fog instead of flat shading

We've lost our distance shading, though — `blit_vspan` just copies texture pixels. We bring depth back by drawing our background colour *over* each slice at an opacity that grows with distance: near walls get almost none, far ones are washed out into the murk. `screen.alpha` sets how opaque the next draw is, so a single translucent strip does it. We add a little extra on the `side == 1` faces to keep those corners reading:

```python-raw
fog = int(dist * 26)
if side == 1: fog += 40
if fog > 205: fog = 205
screen.pen = FOG
screen.alpha = fog                      # 0 = invisible, 255 = solid
screen.rectangle(x, top, 1, height)
screen.alpha = 255                      # reset for everything else
```

# The textured world

Here's the full program — the walkable room from Part 4, now in brick. Wander up to the pillar and watch the bricks resolve as you approach and dissolve into fog as they recede.

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
    screen.blit_vspan(tex, x, y0, y1 - y0, u, (y0 - top) / height, u, (y1 - top) / height)

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

  screen.pen = FOG; screen.clear()
  render()

  screen.pen = color.white
  screen.text("A/C turn   UP/DOWN move", 6, 108)
  badge.update()
```

Swapping in a different texture is now just a matter of drawing — or loading — a different image into `tex`; the renderer doesn't care what's on it. Try `image.load()` with your own artwork, or give walls of different map characters different textures.

The walls are done. All that's left is everything above and below them — in the [final part](06_sky_and_floor.md) we'll add a sky and a floor, and the scene will be complete.

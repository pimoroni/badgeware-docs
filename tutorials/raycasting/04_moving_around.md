---
title: Moving around
summary: Drive the camera with the buttons, and stop yourself walking through walls.
sort: 4
publish: true
---
# Taking the controls

So far the view has drifted on its own. Time to grab the wheel: walk forwards and backwards, turn left and right, and — importantly — bump to a stop when we meet a wall instead of gliding straight through it. None of the rendering changes here; we're only updating the player's `px`, `py` and `angle` each frame before we draw.

# Reading held buttons

For movement we want something to happen *continuously* while a button is down, not once per press — hold **UP** and you keep walking. That's exactly what `badge.held()` reports: `True` for every frame the button is down. (Its cousin `badge.pressed()` fires only on the frame a button first goes down, which is what you'd use for a menu.) We'll wire the badge's five buttons up like this:

- **UP** / **DOWN** — walk forward / back
- **A** / **C** — turn left / right

Turning is the easy half: nudge `angle` by a small step. Because the whole renderer derives its direction from `angle` every frame, changing it is all it takes to look around. We scale each nudge by `badge.ticks_delta` — the milliseconds elapsed since the last frame — so `TURN` is a rate *per second* and turning feels the same whether the badge runs at 60 frames a second or 30:

```python-raw
dt = badge.ticks_delta / 1000                 # seconds since the last frame
if badge.held(BUTTON_A): angle -= TURN * dt   # turn left
if badge.held(BUTTON_C): angle += TURN * dt   # turn right
```

# Walking forward

To walk, we step the position along the way we're facing. We've met this move already — the facing direction is `(cos(angle), sin(angle))`, and scaling it by our `MOVE` speed (and the same `dt`) gives this frame's stride:

```python-raw
dirx, diry = math.cos(angle), math.sin(angle)
if badge.held(BUTTON_UP):
  # move to px + dirx * MOVE * dt, py + diry * MOVE * dt
```

Walking backward is the same step with the sign flipped. But we can't just assign the new position — first we have to make sure we're not stepping into a wall.

# Not walking through walls

The simplest collision check asks the map whether the cell we want to move into is empty. But if we test the whole move at once, brushing a wall at an angle stops us dead. The nicer trick is to check each axis *separately*: try the new `x` on its own, then the new `y` on its own. Slide along a wall you're pushing into diagonally, and one axis stays blocked while the other keeps sliding — so you glide along the wall instead of sticking to it:

```python-raw
def try_move(nx, ny):
  global px, py
  if MAP[int(py)][int(nx)] == " ": px = nx     # take the x move only if that cell is clear
  if MAP[int(ny)][int(px)] == " ": py = ny     # then the y move, independently
```

`int(px)` turns our floating-point position into the whole-number cell to look up in the map. That's all the physics we need — walls are cells, and a move is allowed only into an empty one.

# Putting it together

Here's the walkable version. Click the preview to give it focus, then use the on-screen buttons (or your keyboard's arrow keys and mapped buttons) to explore the room. The renderer is exactly the one from Part 3, now with `@micropython.native` on it and a movement block up top.

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

px, py = 3.5, 4.5
angle = 0.0

MOVE = 2.4        # cells travelled per second while walking
TURN = 1.8        # radians turned per second

# move each axis only if its target cell is empty — so we slide along walls
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
    height = int(H / dist)
    top = (H - height) // 2
    shade = 255 - dist * 34
    if side == 1: shade *= 0.65
    if shade < 20: shade = 20
    c = int(shade)
    screen.pen = color.rgb(c, c, c)
    screen.rectangle(x, top, 1, height)

screen.font = font.nope

while True:
  # scale movement by frame time, so speed is the same at any framerate
  dt = badge.ticks_delta / 1000
  move, turn = MOVE * dt, TURN * dt

  # turn and walk from the buttons, blocked by walls
  dirx, diry = math.cos(angle), math.sin(angle)
  if badge.held(BUTTON_UP):   try_move(px + dirx * move, py + diry * move)
  if badge.held(BUTTON_DOWN): try_move(px - dirx * move, py - diry * move)
  if badge.held(BUTTON_A):    angle -= turn
  if badge.held(BUTTON_C):    angle += turn

  screen.pen = color.rgb(28, 28, 38); screen.clear()
  render()

  screen.pen = color.white
  screen.text("A/C turn   UP/DOWN move", 6, 108)
  badge.update()
```

Have a wander. Notice you can walk right up to one of the free-standing pillars and slide around its corner without catching — that's the per-axis check earning its keep. With rooms and corridors to explore now, the world already feels like a place.

It's a convincing room, but a grey one. In the [next part](05_texturing.md) we'll paint the walls with brickwork, mapping a texture onto every slice as we draw it.

---
title: Rendering walls
summary: Turn each ray's distance into a vertical wall slice — and watch the map stand up into 3D.
sort: 3
publish: true
---
# Standing the map up

This is the part where it becomes 3D. We have, for every ray, the distance to the wall it hits. The leap is to stop drawing that on a flat map and instead read it as *depth into the screen* — and the rule for that is beautifully simple: **the height of a wall slice is inversely proportional to its distance.** Twice as far away, half as tall.

We'll cast one ray for every one of the screen's 160 columns, and for each, draw a single vertical strip of wall, centred on the middle of the screen. Close walls make tall strips that fill the display; distant ones make short strips huddled around the horizon line. Line all 160 up and your brain assembles them into walls.

# From distance to a strip

For a column `x`, we build its ray exactly as before and run the DDA to get `dist`. The slice height is the screen height divided by the distance, and we centre it vertically:

```python-raw
height = int(H / dist)          # nearer wall -> taller strip
top = (H - height) // 2         # centre the strip on the horizon
```

If a wall is one cell away, `height` is the full screen; at two cells it's half, sitting in the middle third; and so on. `top` can go negative for very near walls — the strip simply runs off the top and bottom of the screen, which is exactly what you want when a wall is right in your face. Drawing routines clip to the screen, so we don't have to fuss over it.

# Perpendicular distance, and why there's no fisheye

There's one subtlety worth pausing on. If we'd measured the plain straight-line distance from the player to each wall, the walls would bulge outward in the middle — the infamous *fisheye* distortion — because rays toward the edges of the view are naturally longer than the one pointing dead ahead.

We already avoided it, without extra work. The `dist` our DDA returns is measured along the ray, but scaled by that camera-plane construction from the last part, it comes out as the distance measured *perpendicular to the camera plane* — the depth straight into the screen — rather than the true diagonal to the player. That perpendicular distance is what gives flat walls flat, and it's why we built the rays from a direction plus a plane instead of from an angle per column.

# Shading for depth

Flat-grey walls read as 3D from their shape alone, but a couple of cheap shading tricks make it far more convincing. First, fade strips toward black with distance, so far walls sink into gloom. Second, darken the walls the ray hit on a *horizontal* grid line (`side == 1`) slightly compared to vertical ones — as if light comes from one direction — which makes every corner pop:

```python-raw
shade = 255 - dist * 34         # dimmer with distance
if side == 1: shade *= 0.65     # one set of faces darker, so corners read
if shade < 20: shade = 20       # never go fully black
c = int(shade)
screen.pen = color.rgb(c, c, c)
screen.rectangle(x, top, 1, height)     # a 1px-wide vertical strip
```

# The whole thing

Here's the full renderer. It's the DDA from Part 2, but now each column draws a shaded strip instead of a line on a map — and the map is gone; we're inside it. The view slowly rotates so you can look around the room.

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

def render():
  dirx, diry = math.cos(angle), math.sin(angle)
  planex, planey = -diry * 0.66, dirx * 0.66
  for x in range(W):
    camera = 2 * x / W - 1              # -1..1 across the screen
    rayx = dirx + planex * camera
    rayy = diry + planey * camera

    # --- DDA: step through the grid to the first wall (Part 2) ---
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

    # --- draw the wall slice for this column ---
    height = int(H / dist)
    top = (H - height) // 2
    shade = 255 - dist * 34
    if side == 1: shade *= 0.65
    if shade < 20: shade = 20
    c = int(shade)
    screen.pen = color.rgb(c, c, c)
    screen.rectangle(x, top, 1, height)

while True:
  angle += 0.015
  screen.pen = color.rgb(28, 28, 38); screen.clear()      # a plain background for now
  render()
  badge.update()
```

There it is — a flat grid of text, standing up as a room you can look around. That leap, from Part 1's little map to this, is the whole reason raycasting is such a joy to build.

# Making it fly on real hardware

Casting 160 rays a frame in plain Python is a real workout for the badge's processor. The fix is one line: put `@micropython.native` on `render()`, and MicroPython compiles it to native machine code — typically around twice as fast, for no other change:

```python-raw
@micropython.native
def render():
  ...
```

We'll keep that decorator on `render()` from here on. It's the gentlest of the speed-ups covered in the [Pushing pixels](../guides/performance.md) guide — worth a read if you want to understand what it's doing, or push the frame rate further.

Next we'll stop the room spinning on its own and [take the controls](04_moving_around.md) — walking and turning with the buttons, without strolling straight through the walls.

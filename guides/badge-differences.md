---
title: The three badges
summary: How Tufty, Badger, and Blinky differ — and how to write code that runs on all three.
icon: badge
sort: 2
---

# The three badges

Tufty, Badger, and Blinky run near-identical hardware — the same processor, memory, buttons, and API. What really sets them apart is the display, and that shapes what each badge is best at. You draw to all three with exactly the same commands, so most code runs anywhere; this page covers where they differ, and how to make the most of each.

| | Badger | Tufty | Blinky |
|---|---|---|---|
| Display | E Ink | Colour IPS LCD | LED matrix |
| Resolution | 264 × 176 | 160 × 120 (320 × 240 hi-res) | 39 × 26 |
| Colour | Black, white & two greys | Full RGB | Greyscale |
| Refresh | On demand, sleeps between | Continuous | Continuous |
| Best for | Text, dashboards, e-readers | Games, animation, rich UIs | Scrolling text, pixel art |

You draw to every badge the same way. Anything drawn outside the physical screen simply doesn't appear — run a layout designed for Tufty on Blinky and you'll just see its top-left 39 × 26 pixels.

Colour is handled for you too: colour images are quantised to Badger's greys, or reduced to greyscale on Blinky, automatically. If you want fine control over grey levels, work in greyscale yourself. You can also [dither](/api/image.md#dither) on any badge — most useful on Badger's E Ink display, where a repeating pattern creates intermediate shades of grey.

# Tufty

A full-colour IPS LCD that redraws continuously, Tufty is the one to reach for when you want colour, motion, and rich graphics. It runs at 160 × 120 by default, or switch to a crisp 320 × 240 with [`mode(HIRES)`](/api/badge.md#mode) — sharp for detailed interfaces, while the lower resolution frees up frame rate for animation.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<tufty-model float shadow lighting="150" position="-7 -18 0" camera="0deg 90deg 61%"></tufty-model>
</div>
<figcaption>Tufty's full colour LCD display is ideal for fluid animated graphics.</figcaption>
</figure>

Because it redraws continuously — and can shift plenty of vectors per frame — you can lean into smooth graphics. Here big gradient numerals sit over a drifting field of dots, with a thin bar sweeping out the seconds:

```python
badge.mode(HIRES)                       # 320 x 240
screen.antialias = X4                   # smooth vector edges

clock_font = font.load("/system/assets/fonts/Roboto-Medium-With-Material-Symbols.af")
screen.font = clock_font

cx, cy = screen.width // 2, screen.height // 2

# a cyan-to-violet gradient to fill the numerals — (position 0..1, colour)
TIME_GRADIENT = [
  (0.0, color.rgb(90, 220, 255)),
  (1.0, color.rgb(180, 130, 255)),
]

# a scattering of background dots — Tufty can shift plenty of these per frame
DOTS = [(i * 47 % screen.width, i * 71 % screen.height, 1 + i % 3) for i in range(160)]

while True:
  now = rtc.datetime()
  hour, minute = now[3], now[4]

  # a smooth 0..1 value that sweeps and resets each second
  sweep = (badge.ticks % 1000) / 1000

  # drifting dots for a little ambient motion
  drift = badge.ticks / 40
  screen.pen = color.rgb(40, 48, 72)
  for dx, dy, r in DOTS:
    screen.circle(dx, int((dy + drift) % (screen.height + 8)) - 4, r)

  # the hours and minutes, large, filled left-to-right with the gradient
  clock = "{:02d}:{:02d}".format(hour, minute)
  w, h = screen.measure_text(clock, 104)
  tx, ty = cx - w / 2, cy - h / 2 - 16
  m = mat3().translate(tx, ty).scale(w, h)
  screen.pen = brush.gradient(brush.LINEAR, 0, 0.5, 1, 0.5, TIME_GRADIENT, m)
  screen.text(clock, tx, ty, 104)

  # a thick bar sweeping out the seconds, matching the width of the time above
  by = ty + h + 16
  screen.pen = color.rgb(44, 50, 72)
  screen.shape(shape.rounded_rectangle(tx, by, w, 10, 5))
  screen.pen = color.rgb(150, 210, 255)
  screen.shape(shape.rounded_rectangle(tx, by, w * sweep, 10, 5))

  badge.update()
```

And it can push hundreds of moving, coloured vectors every frame — something neither the e-paper Badger nor the tiny Blinky could get anywhere near. Here a few hundred particles drift in and swarm into the time, re-forming whenever the minute changes:

```python
import math, random, micropython, time

badge.mode(HIRES)                       # 320 x 240
badge.default_clear = None               # we fade the screen ourselves (translucent BG), for trails
BG = color.rgb(8, 10, 20, 12)            # translucent fade — lower alpha = longer trails

cx, cy = screen.width // 2, screen.height // 2
EDGE = int((cx ** 2 + cy ** 2) ** 0.5)   # centre-to-corner; further than this is off-screen

# a precomputed cyan -> magenta palette across the screen width — the hot loop just indexes
# it by x, so no color.hsv() (much slower than the raster fill) runs per frame
PAL = [color.hsv(int(128 + x / screen.width * 90), 210, 255) for x in range(screen.width)]
W1 = screen.width - 1

# --- sample a built-in pixel font into per-character dot maps ----------------
# render each glyph to a scratch buffer and read back its lit pixels (a lit pixel has a
# non-zero premultiplied colour, .p). pixel fonts are already dot-sized, so we use them 1:1.
buf = image(48, 28)
BG_P = color.rgb(0, 0, 0).p

def lit_pixels(ch):
  buf.pen = color.rgb(0, 0, 0)           # opaque clear (a transparent fill would no-op)
  buf.rectangle(0, 0, buf.width, buf.height)
  buf.pen = color.rgb(255, 255, 255)
  buf.text(ch, 0, 0)
  return [(x, y) for y in range(buf.height) for x in range(buf.width) if buf.get(x, y).p != BG_P]

# all the built-in ROM pixel fonts, to cycle through with UP / DOWN
FONT_NAMES = ["absolute", "ark", "awesome", "bacteria", "compass", "corset", "curse", "desert",
              "fear", "futile", "holotype", "hungry", "ignore", "kobold", "lookout", "loser",
              "manticore", "match", "memo", "more", "nope", "outflank", "saga", "salty", "sins",
              "smart", "teatime", "torch", "troll", "unfair", "vest", "winds", "yesterday",
              "yolk", "ziplock"]
font_idx = 0

# sample a font: build each glyph's dots as scaled screen offsets (centred within its slot),
# the x-position of each of the 8 slots, and a fresh particle pool sized to exactly what's
# needed — 8 slots x MAXC particles, MAXC being the busiest character's lit-cell count
def load_font(name):
  global FONT_NAME, DOTS, SLOT_X, Y0, SCALE, MAXC, rects, ease, settled, dots, shown
  buf.font = getattr(rom_font, name)
  FONT_NAME = name
  raw = {ch: lit_pixels(ch) for ch in "0123456789:"}
  ys = [y for ch in "0123456789" for (x, y) in raw[ch]]
  top, height = min(ys), max(ys) - min(ys) + 1
  width = {ch: max(x for x, y in raw[ch]) - min(x for x, y in raw[ch]) + 1 for ch in raw}
  dw = max(width[c] for c in "0123456789")
  cols = [dw, dw, width[":"], dw, dw, width[":"], dw, dw]      # H H : M M : S S, monospaced
  SCALE = max(2, (screen.width - 8) // (sum(cols) + 7))        # screen pixels per font pixel
  Y0 = cy - height * SCALE // 2
  DOTS = {}
  for ch in raw:
    minx = min(x for x, y in raw[ch])
    off = 0 if ch == ":" else (dw - width[ch]) * SCALE // 2    # centre digits in their slot
    DOTS[ch] = [((x - minx) * SCALE + off, (y - top) * SCALE) for x, y in raw[ch]]  # cell top-left
  SLOT_X, x = [], cx - (sum(cols) + 7) * SCALE // 2
  for c in cols:
    SLOT_X.append(x)
    x += (c + 1) * SCALE
  # each particle IS a rect, reused every frame: we mutate its x/y as it eases and pass the
  # object straight to rectangle() (no per-call construction). 8 slots x MAXC, sized to fit
  MAXC = max(len(DOTS[ch]) for ch in "0123456789:")
  rects = [rect(random.random() * screen.width, random.random() * screen.height, SCALE - 1, SCALE - 1)
           for _ in range(8 * MAXC)]
  ease = [random.uniform(3, 9) for _ in range(8 * MAXC)]      # per-second convergence rate, varied
  settled = [False] * 8                                        # per slot: True once its cells arrive
  dots, shown = [], ""                                         # rebuilt / re-formed next frame

load_font(FONT_NAMES[font_idx])

t_render = t_explode = t_blur = 0         # profiling: ms spent in each (explode holds its last)

# the two hot per-frame loops, @native so they compile to machine code on the RP2350.
# both work per-slot and touch only that character's active cells (rects[base .. base+cells]),
# so no spare particles are ever iterated.
@micropython.native
def explode(s):                          # fling one changed slot's cells off-screen to re-form
  base = s * MAXC
  for j in range(len(dots[s])):
    ro = rects[base + j]
    a = random.uniform(0, 6.283)
    r = EDGE + 10 + random.random() * 160
    ro.x = cx + math.cos(a) * r
    ro.y = cy + math.sin(a) * r
  settled[s] = False

@micropython.native
def render(dt):                          # ease each slot's cells to their dots and draw them
  for s in range(8):
    d = dots[s]
    base = s * MAXC
    if settled[s]:                       # slot has arrived — just redraw its cells, no easing
      for j in range(len(d)):
        ro = rects[base + j]
        screen.pen = PAL[clamp(int(ro.x), 0, W1)]
        screen.rectangle(ro)
    else:
      moving = False
      for j in range(len(d)):
        ro = rects[base + j]
        hx, hy = d[j]
        dx, dy = hx - ro.x, hy - ro.y
        if dx * dx + dy * dy > 0.25:     # ease[.] * dt keeps the pace framerate-independent
          f = min(ease[base + j] * dt, 1)
          ro.x += dx * f
          ro.y += dy * f
          moving = True
        else:
          ro.x, ro.y = hx, hy            # snap exactly onto the integer grid once close
        screen.pen = PAL[clamp(int(ro.x), 0, W1)]   # PAL indexes the precomputed gradient by x
        screen.rectangle(ro)             # pass the reused rect straight in (no 4-number call)
      if not moving:
        settled[s] = True                # everything's arrived — stop easing this slot

while True:
  loop_start = time.ticks_us()           # time our own per-frame work directly (not ticks_delta)
  dt = badge.ticks_delta / 1000          # ms since last update() — framerate-independent easing

  # UP / DOWN cycle the font, re-sampling into the new one
  step = 0
  if badge.pressed(BUTTON_UP):
    step = 1
  elif badge.pressed(BUTTON_DOWN):
    step = -1
  if step:
    font_idx = (font_idx + step) % len(FONT_NAMES)
    load_font(FONT_NAMES[font_idx])      # rebuilds the pool and resets shown, so it re-forms

  now = rtc.datetime()
  hm = "{:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5])
  if hm != shown:
    dots = [[(SLOT_X[s] + dx, Y0 + dy) for dx, dy in DOTS[hm[s]]] for s in range(8)]
    # fling the particles of any digit that changed out in all directions; the easing
    # below then whizzes them back in to re-form the character (skipped on first load,
    # so the intro keeps its full-screen zoom instead)
    if shown:
      te = time.ticks_us()
      for s in range(8):
        if hm[s] != shown[s]:            # re-form only the glyphs that changed
          explode(s)
      t_explode = time.ticks_diff(time.ticks_us(), te) / 1000
    shown = hm

  # blur the previous frame, then fade it back toward the background — soft, bloomy trails
  tb = time.ticks_us()
  screen.blur(20)
  t_blur = time.ticks_diff(time.ticks_us(), tb) / 1000
  screen.pen = BG
  screen.rectangle(0, 0, screen.width, screen.height)

  tr = time.ticks_us()
  render(dt)
  t_render = time.ticks_diff(time.ticks_us(), tr) / 1000

  # corner: the active font's name, drawn in that font
  screen.font = buf.font
  screen.pen = color.rgb(255, 255, 255)
  screen.text(FONT_NAME, 6, 6)

  # profiling (ms): loop = our own measured work this frame; sys = the overhead badge.update()
  # itself adds (flush + clear + poll + any vsync wait) = ticks_delta - loop. render/blur/explode
  # are subsets of loop; vs is the live vsync state read back from badge.mode()
  t_loop = time.ticks_diff(time.ticks_us(), loop_start) / 1000
  sys = badge.ticks_delta - t_loop
  screen.font = rom_font.sins
  screen.text("render {:.1f}  blur {:.1f}  exp {:.1f}".format(t_render, t_blur, t_explode), 6, screen.height - 24)
  screen.text("loop {:.1f}  sys {:.1f}  vs {}".format(t_loop, sys, 1 if badge.mode() & VSYNC else 0), 6, screen.height - 12)
  # FPS from the true frame period (ticks_delta), right-aligned in the bottom-right corner
  fps_txt = "{:.1f} fps".format(1000 / badge.ticks_delta if badge.ticks_delta else 0)
  screen.text(fps_txt, screen.width - screen.measure_text(fps_txt)[0] - 6, screen.height - 12)

  badge.update()
```

# Badger

Badger's E Ink display only draws power when it changes, which makes it superb for low-power, always-on apps. To exploit that, Badger sleeps between updates and wakes on a timer or a button press. Waking restarts your program from the top — so anything you haven't saved is lost — which means a Badger app typically draws once, then sleeps until it next needs to change.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<badger-model float shadow lighting="179" position="-2 32 0" camera="0deg 90deg 71%"></badger-model>
</div>
<figcaption>For low power projects that need to run for months you can't beat Badger.</figcaption>
</figure>

So rather than a continuous loop, a Badger clock draws the time, then sleeps until the next minute:

```python
# Badger restarts from the top each time it wakes, so this runs once per minute
now = rtc.datetime()
hour, minute, second = now[3], now[4], now[5]

# e-paper: draw in black on the cleared white background
screen.pen = color.black
screen.text("{:02d}:{:02d}".format(hour, minute), 96, 76)
badge.update()

badge.sleep(60 - second)   # sleep to the next minute, then wake and redraw
```

Refresh speed trades crispness against ghosting; tune it with [`FAST_UPDATE`, `MEDIUM_UPDATE`, or `FULL_UPDATE`](/api/badge.md#mode).

# Blinky

Blinky's 39 × 26 LED matrix is bright and bold — perfect for scrolling text, pixel art, and notifications you can read across a room. Like Tufty, it redraws continuously. It also has cutouts for the case corners and buttons, but you don't need to account for them: anything drawn into those pixels is simply ignored.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<blinky-model float shadow lighting="179" position="4 -22 0" camera="0deg 90deg 66%"></blinky-model>
</div>
<figcaption>Brilliant retro pixel art truly sparkles on Blinky.</figcaption>
</figure>

With so few pixels, a clock has to be compact — stack the hours over the minutes:

```python
screen.font = rom_font.nope

while True:
  now = rtc.datetime()
  hour, minute = now[3], now[4]

  # only 39 x 26 pixels, so put the hours above the minutes
  screen.pen = color.white
  screen.text("{:02d}".format(hour), 12, 3)
  screen.text("{:02d}".format(minute), 12, 15)

  badge.update()
```

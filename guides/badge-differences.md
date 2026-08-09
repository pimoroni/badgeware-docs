---
title: The three badges
summary: How Tufty, Badger, and Blinky differ — and how to write code that runs on all three.
icon: badge
sort: 2
---

# The three badges

Tufty, Badger, and Blinky are built around the same processor, memory, buttons, and API. What really sets them apart is the display. Three distinct technologies, each shaping what each badge is best at. You draw to all three with exactly the same commands, so most code runs anywhere. This page covers where they differ, and how to make the most of each.

| | Badger | Tufty | Blinky |
|---|---|---|---|
| Display | E Ink | Colour IPS LCD | LED matrix |
| Resolution | 264 × 176 | 160 × 120 (320 × 240 hi-res) | 39 × 26 |
| Colour | Black, white & two greys | Full RGB | Greyscale |
| Refresh | On demand, sleeps between | Continuous | Continuous |
| Best for | Text, dashboards, e-readers | Games, animation, rich UIs | Scrolling text, pixel art |

You draw to every badge the same way, and anything drawn outside the physical screen doesn't appear. Run a layout designed for Tufty on Blinky and you'll see only its top-left 39 × 26 pixels.

Colour is handled for you too: colour images are quantised to Badger's greys, or reduced to greyscale on Blinky, automatically. If you want fine control over grey levels, work in greyscale yourself. You can also [dither](/api/image.md#dither) on any badge — most useful on Badger's E Ink display, where a repeating pattern creates the illusion of intermediate shades of grey.

Three badges, three screens, three very different sizes and styles. Below you'll learn what each is great at, and get a taste for how you might write a clock app for each.

# Tufty

Tufty sports a full-colour IPS LCD that redraws continuously. This is the badge to reach for when you want colour, motion, and rich graphics. It runs at 160 × 120 by default, freeing up the framerate for fluid animation. Switch to a crisp 320 × 240 with [`mode(HIRES)`](/api/badge.md#mode) for detailed interfaces.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<tufty-model float shadow lighting="150" position="-7 -18 0" camera="0deg 90deg 61%"></tufty-model>
</div>
<figcaption>Tufty's full-colour LCD display is ideal for fluid animated graphics.</figcaption>
</figure>

Because it redraws continuously and works in full colour, a Tufty clock is just a loop that draws the time fresh every frame. For a big bold clock we scale the built-in absolute font up 2× (the fourth argument to [`text()`](/api/image.md#text) is an integer scale for pixel fonts). Pixel text is drawn through the current brush just like vector text, so we can fill it with a gradient brush. Rebuild this each frame with a rotating matrix and a bright highlight sweeps around the clock, appearing horizontal exactly as each second ticks over:

```python
import time

screen.font = font.absolute

# cyan -> violet with a white highlight that sweeps as the gradient spins
STOPS = [
  (0.0, color.rgb(120, 90, 255)),
  (0.42, color.rgb(90, 220, 255)),
  (0.5, color.rgb(255, 255, 255)),
  (0.58, color.rgb(90, 220, 255)),
  (1.0, color.rgb(120, 90, 255)),
]

while True:
  # clear the framebuffer to black each frame
  screen.pen = color.black
  screen.clear()

  # RP2350 clock: H:M:S from localtime(), ms phase from time_ns()
  lt = time.localtime()
  hour, minute, second = lt[3], lt[4], lt[5]
  frac = time.time_ns() // 1_000_000 % 1000   # ms into the current second

  # turn 180deg per second, passing horizontal (90deg) on the tick; the
  # stops are symmetric so 90deg and 270deg match - no jump at the boundary
  angle = 90 + frac * 180 / 1000
  m = mat3().translate(80, 60).rotate(angle).scale(150)
  screen.pen = brush.gradient(brush.LINEAR, -0.5, 0, 0.5, 0, STOPS, m)

  clock = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
  screen.text(clock, 23, 44, 2)

  badge.update()
```

# Badger

Badger's E Ink display only draws power when it changes, which makes it superb for low-power, always-on apps. To exploit that, Badger sleeps between updates and wakes on a timer or a button press. Waking restarts your program from the top — so anything you haven't saved is lost — which means a Badger app typically draws once, saves its state, then sleeps until it next needs to change.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<badger-model float shadow lighting="179" position="-2 32 0" camera="0deg 90deg 71%"></badger-model>
</div>
<figcaption>For low power projects that need to run for months you can't beat Badger.</figcaption>
</figure>

In lieu of a continuous loop a Badger clock draws the time and sleeps until the next minute:

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

Blinky's 39 × 26 LED matrix is bright and bold — perfect for scrolling text, pixel art, and notifications you can read across a room. Like Tufty, it redraws continuously. It also has cutouts for the case corners and buttons, but you don't need to account for them: anything drawn into those pixels is ignored.

<figure class="feature-callout">
<div class="callout-media" style="--callout-aspect: 2.5 / 1">
<blinky-model float shadow lighting="179" position="4 -22 0" camera="0deg 90deg 66%"></blinky-model>
</div>
<figcaption>Brilliant retro pixel art truly sparkles on Blinky.</figcaption>
</figure>

With so few pixels, a clock has to be compact — stack the hours over the minutes:

```python
screen.font = font.nope

while True:
  now = rtc.datetime()
  hour, minute = now[3], now[4]

  # only 39 x 26 pixels, so put the hours above the minutes
  screen.pen = color.white
  screen.text("{:02d}".format(hour), 12, 3)
  screen.text("{:02d}".format(minute), 12, 15)

  badge.update()
```

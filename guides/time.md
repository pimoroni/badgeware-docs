---
title: Time
summary: Process the passing of time and scale changes to your application state based on elapsed frame time.
icon: timer
---

# Timing

Your `update()` function runs once per frame, but frames don't take exactly the same amount of time — a busy frame that draws a lot takes longer than a quiet one. If you move things by a fixed amount every frame, they'll speed up and slow down with the framerate. The fix is to base movement on *time*, not on frames.

Badgeware gives you two clocks on the `badge` object for this.

## badge.ticks
The number of ticks (milliseconds) since the badge was powered on, sampled when the current frame began. Use it as a steadily increasing clock to drive animations.

```python
import math

while True:
  # bob a circle up and down using a sine wave over time
  y = 60 + math.sin(badge.ticks / 300) * 30

  screen.pen = color.orange
  screen.circle(80, y, 15)

  badge.update()
```

## badge.ticks_delta
The number of ticks (milliseconds) since the previous frame. Multiply your speeds by this to get frame-rate-independent movement: something that moves "60 pixels per second" will do so no matter how fast or slow the frames are.

```python
x = 0.0

while True:
  # move 60 pixels per second, regardless of framerate
  x += 60 * (badge.ticks_delta / 1000)
  if x > screen.width:
    x = 0

  screen.pen = color.lime
  screen.circle(int(x), 60, 10)

  badge.update()
```

# Timed loops and progress

If you're building a splash screen or a timed animation, you can let [run()](/api/run.md) handle the timing for you. Give it a `duration` and use `loop.progress` — a value from 0 to 1 — to drive the animation. See the [run](/api/run.md) reference for more.

# Real-world time

For the wall-clock date and time — which keeps ticking even while the badge sleeps — use the [rtc](/api/rtc.md) instead. It can also wake the badge on a schedule, which is how low-power clocks and dashboards refresh themselves.

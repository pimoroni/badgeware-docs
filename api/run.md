---
title: The main loop
summary: How a Badgeware app is structured — draw in a loop and call badge.update() each frame. Plus run(), the convenience wrapper used by the menu system.
icon: play_circle
publish: true
---
# Introduction
A Badgeware app is just a loop. Each time round, you draw to the `screen`, then call [badge.update()](/api/badge.md#update) to push what you've drawn to the display and read the buttons. That's the whole model:

```python
while True:
  screen.pen = color.white
  screen.text("Hello, Badgeware!", 10, 10)

  badge.update()
```

The screen starts cleared, and `badge.update()` clears it again ready for the next frame — so inside the loop you only need to draw. Under the hood, each call to `badge.update()`:

1. Pushes the framebuffer to the physical display.
2. Clears the screen to `badge.default_clear` (ready for the next frame).
3. Polls the buttons and updates the tick counter.

Because `badge.update()` handles all of this, you rarely need to call `screen.update()`, `badge.clear()` or `badge.poll()` individually — but you can, if you want finer control. See the [badge](/api/badge.md) article for those building blocks.

# run()
`run()` is a convenience wrapper around exactly the loop above. You give it an `update` function, and it calls that function once per frame, calling `badge.update()` for you in between. It's the mechanism the built-in menu and app system uses to launch apps, and it's handy when you want the loop to stop on a condition or after a set time.

If your `update` function returns a value, the loop stops and `run()` hands that value back — a tidy way to close a menu or sub-screen and return a result. You can also pass a `duration` in milliseconds, after which the loop stops on its own, which is perfect for splash screens and timed animations.

### Usage
- `run(update)`
    - `update`: The function to call once per frame.
- `run(update, duration=ms)`
    - `duration`: How long to run for, in milliseconds, before stopping automatically.

### Returns
The value returned by `update()`, if it returned one to stop the loop; otherwise `None`.

### Example
```python
# a five second countdown, then stop
def update():
  remaining = 5 - loop.ticks // 1000

  screen.pen = color.yellow
  screen.font = rom_font.more
  screen.text(f"{remaining}", 70, 45)

  # stop early if A is pressed
  if badge.pressed(BUTTON_A):
    return "cancelled"

run(update, duration=5000)
```

# loop
While `run()` is running, a global `loop` object describes the current loop. Use it to time animations and to drive progress bars. It's only available inside a `run()` — if you write your own `while True` loop, use [badge.ticks](/api/badge.md#ticks) for timing instead.

## ticks
The number of milliseconds since this loop started. Unlike `badge.ticks` (which counts from power-on), `loop.ticks` resets to zero each time you call `run()`, so it's a convenient clock for a single screen or animation.

## progress
A value from 0 to 1 describing how far through a timed loop you are, i.e. `loop.ticks / duration`. If the loop was started without a `duration`, `progress` is always 0.

### Example
```python
def update():
  # a progress bar that fills over three seconds
  screen.pen = color.grey
  screen.rectangle(20, 55, 120, 10)

  screen.pen = color.lime
  screen.rectangle(20, 55, int(120 * loop.progress), 10)

run(update, duration=3000)
```

# launch()
Launches another app by path. This is mainly used by the Badgeware menu system to start the app you select, but it's available if you're building your own launcher. When the app exits (or the user presses the HOME button) control returns to your code.

### Usage
- `launch(path)`
    - `path`: The path to the app to launch.

# Reference

## Functions
```python-raw
run(update: function) -> any
run(update: function, duration: int) -> any
launch(path: string) -> any
```

## loop
```python-raw
loop.ticks -> int
loop.progress -> float
```

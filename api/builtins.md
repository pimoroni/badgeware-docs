---
title: builtins
summary: Handy global helpers — the app loop, saved state, clamping, random numbers, file checks and memory reporting — available in any app without importing anything.
icon: widgets
publish: true
---
# Introduction
Badgeware puts a handful of convenience functions straight into the global namespace, so they're available in any app without an `import`. They cover the jobs that come up constantly: running your app's loop, remembering things between runs, keeping a number in range, picking a random value, checking for a file, and seeing how much memory is free.

# The app loop

## run()
Runs your app. Hand `run()` a function and it calls it over and over: clearing the screen, running your function, showing the frame, and reading the buttons, until your function returns something.

The screen is cleared to [`badge.default_clear`](/api/badge.md#default_clear) and the pen set to `badge.default_pen` before your function is called, so there's no need to clear it yourself.

Returning anything other than `None` from your function ends the loop, and that value lands on the `result` of the loop `run()` returns.

It also works as a decorator:

```python-raw
@run
def update():
  screen.text("Hello!", 10, 10)
```

An unhandled exception inside your function shows the error in a box on screen, waits for a button, and resets. The full details go to the console as well, so they're still there if you're plugged in.

### Usage
`run(update)` \
`run(duration=ms)(update)`

| Parameter | Type | Description |
|---|---|---|
| `update` | `function` | Called once per frame, taking no arguments. Return anything to stop |
| `duration` | `int` | *Optional.* Keyword only. Stop after this many milliseconds, whatever your function returns |

### Returns
The loop. The `result` property holds the value your function returned.

```python
def menu():
  screen.text("A: coffee", 10, 20)
  screen.text("B: tea", 10, 40)

  if badge.pressed(BUTTON_A):
    return "coffee"
  if badge.pressed(BUTTON_B):
    return "tea"

# blocks here until a button picks one
chosen = run(menu).result

def show():
  screen.text("You chose {}".format(chosen), 10, 30)

run(show)
```

## loop
While a `run()` is going, the global `loop` is the loop that's running.

| Property | Type | Description |
|---|---|---|
| `ticks` | `int` | Milliseconds since this loop started |
| `progress` | `float` | How far through a `duration` the loop is, from `0` to `1`. Reads `0` if it was given no duration |
| `duration` | `int` \| `None` | The duration it was given |
| `result` | `any` | What the loop's function returned to end it |

Loops nest: a `run()` inside a running loop becomes `loop` for as long as it lasts, and the outer one is restored afterwards. A timed splash screen is then a self-contained function:

```python
def splash():
  # fade the title in over the two seconds the loop is given
  screen.pen = color.white.with_alpha(int(loop.progress * 255))
  screen.text("BADGEWARE", 30, 55)

run(duration=2000)(splash)

def main():
  screen.text("...and we're off", 20, 55)

run(main)
```

# Numbers

## clamp()
Constrains a value to a range — returning `vmin` if `v` is below it, `vmax` if above, or `v` unchanged when it's already within.

### Usage
`clamp(v, vmin, vmax)`

| Parameter | Type | Description |
|---|---|---|
| `v` | `int` \| `float` | The value to constrain |
| `vmin` | `int` \| `float` | The lower bound |
| `vmax` | `int` \| `float` | The upper bound |

### Returns
`v` limited to the range `vmin` to `vmax`.

```python-raw
x = clamp(x, 0, screen.width)   # keep x on screen
```

## rnd()
Returns a random **integer**. With one argument the range is `0` to `v1`; with two it's `v1` to `v2`. Both ends are inclusive.

### Usage
`rnd(v1)` \
`rnd(v1, v2)`

| Parameter | Type | Description |
|---|---|---|
| `v1` | `int` | The upper bound, or the lower bound when `v2` is given |
| `v2` | `int` | *Optional.* The upper bound |

### Returns
A random `int` within the range (inclusive).

## frnd()
Returns a random **float**. With one argument the range is `0.0` to `v1`; with two it's `v1` to `v2`.

### Usage
`frnd(v1)` \
`frnd(v1, v2)`

| Parameter | Type | Description |
|---|---|---|
| `v1` | `float` | The upper bound, or the lower bound when `v2` is given |
| `v2` | `float` | *Optional.* The upper bound |

### Returns
A random `float` within the range.

```python-raw
angle = frnd(6.28)          # a random angle in radians
speed = frnd(0.5, 2.0)      # a random speed
```

# Files

## file_exists()
Returns whether anything — a file or a directory — exists at the given path.

### Usage
`file_exists(path)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | The path to check |

### Returns
`True` if something exists at `path`, otherwise `False`.

## is_dir()
Returns whether the given path is a directory.

### Usage
`is_dir(path)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | The path to check |

### Returns
`True` if `path` is a directory, otherwise `False`.

# Saved state
`State` keeps a dictionary of settings or progress in `/state/<name>.json`, so an app can pick up where it left off after a reset, a sleep, or a trip round the menu. The name should be distinct, so it doesn't clash with another app, and the same one used for both saving and loading.

Everything in the dictionary has to survive a round trip through JSON, so numbers, strings, booleans, lists and dictionaries of those. A `vec2` or a `color` will not go in. Save the components as a list of numbers and rebuild it on the way out.

## State.load()
Loads the saved state for an app into a dictionary of defaults, overwriting the entries it finds and leaving the rest alone. Nothing saved yet, or a file too damaged to read, leaves your defaults as they are. It also writes them out, so there's a file to load next time.

A save written before you added a setting has no entry for it, and the default you passed in stays.

### Usage
`State.load(name, defaults)`

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | The name this app saves under |
| `defaults` | `dict` | Loaded into in place |

### Returns
`True` if a saved state was read, `False` if the defaults were used.

## State.save()
Saves a dictionary as this app's state, replacing whatever was there. Creates `/state` if it's missing.

### Usage
`State.save(name, data)`

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | The name this app saves under |
| `data` | `dict` | The state to write |

## State.modify()
Merges a dictionary into the saved state, leaving keys you don't supply as they were. Handy for writing one setting without loading and re-saving the lot.

### Usage
`State.modify(name, data)`

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | The name this app saves under |
| `data` | `dict` | The entries to change |

## State.delete()
Deletes an app's saved state, if there is any.

### Usage
`State.delete(name)`

| Parameter | Type | Description |
|---|---|---|
| `name` | `string` | The name this app saves under |

```python
settings = {"high_score": 0, "sound": True}
State.load("my_game", settings)

def update():
  screen.text("Best: {}".format(settings["high_score"]), 10, 20)

  if badge.pressed(BUTTON_A):
    settings["high_score"] += 10
    State.modify("my_game", {"high_score": settings["high_score"]})

run(update)
```

# Memory

## free()
Prints the current free memory in kilobytes, along with the change since the last call — handy for spotting leaks or checking headroom while developing. It runs a garbage collection first, so the figure reflects genuinely reclaimable memory.

### Usage
`free()` \
`free(message)`

| Parameter | Type | Description |
|---|---|---|
| `message` | `string` | *Optional.* A label to print before the figure |

### Returns
Nothing — the reading is printed, for example `after assets: 812kb (-40kb)`.

```python-raw
free("startup")
# ... load some assets ...
free("after assets")    # prints the memory used since startup
```

---
title: builtins
summary: Handy global helpers — clamping, random numbers, file checks and memory reporting — available in any app without importing anything.
icon: widgets
publish: true
---
# Introduction
Badgeware puts a handful of convenience functions straight into the global namespace, so they're available in any app without an `import`. They cover the little jobs that come up constantly: keeping a number in range, picking a random value, checking for a file, and seeing how much memory is free.

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

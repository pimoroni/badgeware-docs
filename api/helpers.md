---
title: helpers
summary: Handy global helper functions for random numbers, clamping, filesystem checks, font loading and memory reporting.
icon: build
publish: true
---
# Introduction
Badgeware adds a handful of small helper functions to the global namespace. They're always available — you don't need to import anything — and they smooth over some of the most common little jobs: picking random numbers, keeping a value in range, checking whether a file exists, loading a font by name, and keeping an eye on free memory.

# Maths helpers
Small numeric conveniences that come up constantly in games and animations.

## clamp()
Constrains a value to a range, returning `vmin` if it's too low, `vmax` if it's too high, or the value unchanged if it's already inside the range.

### Usage
- `clamp(v, vmin, vmax)`
    - `v`: The value to constrain.
    - `vmin`: The lowest allowed value.
    - `vmax`: The highest allowed value.

### Returns
The clamped value.

## rnd()
Returns a random **integer**. With one argument it returns a value from 0 up to and including that number; with two it returns a value in the given range.

### Usage
- `rnd(v)`
    - `v`: Returns a random integer from 0 to `v`.
- `rnd(v1, v2)`
    - `v1, v2`: Returns a random integer from `v1` to `v2`.

### Returns
A random `int`.

## frnd()
The floating-point companion to `rnd()`. Returns a random **float**, either from 0 to `v`, or between `v1` and `v2`.

### Usage
- `frnd(v)`
    - `v`: Returns a random float from 0 to `v`.
- `frnd(v1, v2)`
    - `v1, v2`: Returns a random float from `v1` to `v2`.

### Returns
A random `float`.

### Example
```python
# scatter some randomly placed, randomly sized dots, kept on-screen
dots = []
for _ in range(40):
  dots.append((rnd(screen.width), rnd(screen.height), frnd(1, 5)))

while True:
  for x, y, r in dots:
    screen.pen = color.hsv(rnd(255), 200, 255)
    # clamp keeps the radius sensible even if the data changes
    screen.circle(x, y, clamp(r, 1, 6))

  badge.update()
```

# Filesystem helpers
Quick checks for the presence and type of files on the badge.

## file_exists()
Returns `True` if a file or directory exists at the given path, otherwise `False`.

### Usage
- `file_exists(path)`
    - `path`: The path to check.

### Returns
`bool`

## is_dir()
Returns `True` if the given path exists and is a directory, otherwise `False`.

### Usage
- `is_dir(path)`
    - `path`: The path to check.

### Returns
`bool`

# Fonts

## load_font()
Loads a font by name or path, returning a `font` (vector) or `pixel_font` (bitmap) as appropriate. It searches the badge's font folders for you — ROM fonts, `/system/assets/fonts`, `/fonts` and `/assets` — so you can usually just pass a short name like `"nope"` and it'll find it. Pass a full path (ending in `.af` or `.ppf`) to load a specific file. Raises `OSError` if the font can't be found.

### Usage
- `load_font(name_or_path)`
    - `name_or_path`: A ROM font name, a bare font name, or a full path to an `.af` or `.ppf` file.

### Returns
A `font` or `pixel_font`, depending on the file type.

### Example
```python
screen.font = load_font("nope")

while True:
  screen.pen = color.cyan
  screen.text("loaded by name!", 10, 20)

  badge.update()
```

# Memory

## free()
Runs a garbage collection, then prints the amount of free RAM (in kilobytes) to the console. If you call it more than once it also shows how much has changed since the previous call, which is handy for spotting leaks or heavy allocations. An optional message is printed alongside to label the reading.

### Usage
- `free(message)`
    - `message` (Optional): A label to print before the reading.

### Returns
`None`

# Reference

## Functions
```python-raw
clamp(v: int|float, vmin: int|float, vmax: int|float) -> int|float
rnd(v1: int, v2: int=None) -> int
frnd(v1: int|float, v2: int|float=None) -> float
file_exists(path: string) -> bool
is_dir(path: string) -> bool
load_font(name_or_path: string) -> font | pixel_font
free(message: string="") -> None
```

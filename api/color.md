---
title: color
summary: Methods for creating colours in a variety of different colourspaces and selecting colours from the built-in palette.
icon: palette
publish: true
---
# Introduction
Represents an RGBA colour.

The `color` type provides methods for creating colours from RGBA, HSV, and OKLCH colour spaces. Colours can be adjusted, blended, and combined using a range of utility methods.

A colour preserves the space and the components it was authored in, so `color.hsv(...)` reports its hue back and adjusts along the HSV axes, while `color.rgb(...)` works in channels.

# Properties
All properties are read-only.

These are available on any colour, whatever space it came from:

| Property | Type | Description |
|---|---|---|
| `r`, `g`, `b` | `int` | The red, green and blue the colour resolves to, 0–255 |
| `a` | `int` | Alpha, 0–255 |
| `space` | `string` | How the colour was authored: `"rgb"`, `"hsv"` or `"oklch"` |
| `p` | `int` | The premultiplied RGBA colour as a 32-bit unsigned integer |
| `luminance` | `float` | WCAG relative luminance, 0.0–1.0. Alpha is ignored |
| `in_gamut` | `bool` | Whether the screen can show this colour. Only `color.oklch()` can produce one it can't; see [`fit()`](#fit) |

These read back the components the colour was authored with, so each belongs to one space. Use [`to_oklch()`](#to_oklch) to work in another space:

| Property | Type | Available on | Description |
|---|---|---|---|
| `h` | `int` | `hsv`, `oklch` | Hue, 0–255 |
| `s` | `int` | `hsv` | Saturation, 0–255 |
| `v` | `int` | `hsv` | Value, 0–255 |
| `l` | `int` | `oklch` | Lightness, 0–255 |
| `c` | `int` | `oklch` | Chroma, 0–255 |

# Static Methods
The first three create `color` objects from different colour representations. `ramp()` samples a gradient into a list, and `max_chroma()` reports the gamut limit at a given lightness and hue.

## rgb()
Creates a new `color` object from red, green, blue, and optional alpha values.

### Usage
`color.rgb(r, g, b, a)`

| Parameter | Type | Description |
|---|---|---|
| `r`, `g`, `b` | `int` | Colour component values, 0–255 |
| `a` | `int` | *Optional.* Alpha value, 0–255 |

### Returns
A new `color`.

```python
def update():
  # draw a gradient from cyan to magenta
  for x in range(0, 160):
    step = (x * 255) / 160
    screen.pen = color.rgb(step, 255 - step, 150)
    screen.line(x, 0, x, 120)

run(update)
```

## hsv()
Creates a new `color` object from hue, saturation, value, and optional alpha values.

HSV is not perceptually uniform, so equal changes in its values do not correspond to equal perceived colour changes. This can lead to uneven gradients and unintuitive results when adjusting saturation or brightness.

### Usage
`color.hsv(h, s, v, a)`

| Parameter | Type | Description |
|---|---|---|
| `h` | `int` | Hue, 0–255 |
| `s` | `int` | Saturation, 0–255 |
| `v` | `int` | Value (brightness), 0–255 |
| `a` | `int` | *Optional.* Alpha value, 0–255 |

### Returns
A new `color`.

```python
def update():
  # draw a hue gradient
  for x in range(0, 160):
    hue = 255 * (x / 160)
    saturation = 255
    value = 255
    screen.pen = color.hsv(hue, saturation, value)
    screen.line(x, 0, x, 120)

run(update)
```

## oklch()
Creates a new `color` object from OKLCH parameters and an optional alpha value.

OKLCH is a perceptually uniform colour space, meaning equal changes in its values produce more consistent visual changes. This makes it better suited for colour adjustment and interpolation than HSV, which can produce uneven or unexpected results.

The components are 0–255 like every other space here: `l` covers the full 0 to 1 lightness range, `c` covers 0 to 0.35 chroma, and `h` is 256 counts to a full turn, so `250` is 352 degrees. `color.oklch()` can also produce colours the screen can't show; see [`in_gamut`](#properties) and [`fit()`](#fit).

### Usage
`color.oklch(l, c, h, a)`

| Parameter | Type | Description |
|---|---|---|
| `l` | `int` | Lightness, 0–255 |
| `c` | `int` | Chroma (saturation), 0–255 |
| `h` | `int` | Hue, 0–255 |
| `a` | `int` | *Optional.* Alpha value, 0–255 |

### Returns
A new `color`.

```python
def update():
  for x in range(0, 160):
    lightness = 220
    chroma = 150
    hue = 255 * (x / 160)
    screen.pen = color.oklch(lightness, chroma, hue)
    screen.line(x, 0, x, 120)

run(update)
```

## ramp()
Samples a gradient into a list of colours. `stops` is a sequence of `(position, color)` pairs with positions from `0` to `1`, exactly as [`brush.gradient()`](/api/brush.md#gradient-brushes) takes them, and sampled the same way — so two OKLCH stops ramp through OKLCH, and every stop lands exactly on an entry.

The result is an ordinary list, ready for [`palette_dither()`](/api/image.md#palette_dither) or to index into.

### Usage
`color.ramp(stops, count)`

| Parameter | Type | Description |
|---|---|---|
| `stops` | `list` | Up to 16 `(position, color)` tuples, positions from `0` to `1` |
| `count` | `int` | How many colours to sample, 1–1024 |

### Returns
A `list` of `count` colours.

```python
shades = color.ramp([(0, color.navy), (0.5, color.red), (1, color.yellow)], 32)

def update():
  for i, shade in enumerate(shades):
    screen.pen = shade
    screen.rectangle(i * 5, 20, 5, 80)

run(update)
```

## max_chroma()
Returns the most chroma an OKLCH colour can carry at a given lightness and hue. The gamut is lopsided: a yellow reaches far more than a blue at the same lightness.

### Usage
`color.max_chroma(l, h)`

| Parameter | Type | Description |
|---|---|---|
| `l` | `int` | Lightness, 0–255 |
| `h` | `int` | Hue, 0–255 |

### Returns
An `int` from 0 to 255.

# Reading a colour in another space
A colour's components belong to the space it was authored in. These two return the same colour authored in another space, so its components can be read there and arithmetic acts on those axes.

## to_oklch()
Returns this colour authored in OKLCH, so its `l`, `c` and `h` can be read. A colour already in OKLCH comes back unchanged; anything else goes via sRGB and lands on the nearest byte per axis. Near-greys have no meaningful hue, so don't read much into the one you get.

### Usage
`.to_oklch()`

### Returns
A new `color` in the `oklch` space.

```python-raw
base = color.red.to_oklch()     # a palette entry, now adjustable by lightness
print(base.l, base.c, base.h)
```

## to_rgb()
Returns this colour authored in RGB, whatever space it came from.

### Usage
`.to_rgb()`

### Returns
A new `color` in the `rgb` space.

# Adjusting a colour
Every one of these returns a new colour and leaves the original as it was.

## lighten() / darken()
Returns the colour lightened or darkened by an amount. Which component moves depends on the space: `v` on an HSV colour, `l` on an OKLCH one, and all three channels on an RGB one. Values clamp at the ends.

### Usage
`.lighten(amount)` \
`.darken(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | How far to move, 0–255 |

### Returns
A new `color`.

## scale()
Returns the colour with its lightness scaled by a percentage, where `100` leaves it alone. It moves the same component `lighten()` does, and alpha is untouched. Scaling suits shading a whole palette at once, where a fixed `lighten()` would flatten the dark end.

### Usage
`.scale(percent)`

| Parameter | Type | Description |
|---|---|---|
| `percent` | `int` | Lightness as a percentage of what it was, `100` being unchanged |

### Returns
A new `color`.

## with_alpha()
Returns the colour at a different alpha.

### Usage
`.with_alpha(a)`

| Parameter | Type | Description |
|---|---|---|
| `a` | `int` | Alpha, 0–255 |

### Returns
A new `color`.

## mix()
Returns this colour blended toward another. When both share a space it interpolates the authored components, taking a hue the short way round the wheel; otherwise it interpolates sRGB.

### Usage
`.mix(other, t)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `color` | The colour to blend toward |
| `t` | `int` | How far, where `0` is this colour and `255` is `other` |

### Returns
A new `color`.

```python-raw
# a flash that fades back to the base colour over half a second
t = clamp(int((badge.ticks - hit_at) / 500 * 255), 0, 255)
screen.pen = color.white.mix(base, t)
```

## over()
Returns this colour as it lands over a background, weighted by its alpha: the same composite the renderer performs. Useful when you need the composited colour as a value, since [`contrast()`](#contrast) and [`difference()`](#difference) ignore alpha.

### Usage
`.over(background)`

| Parameter | Type | Description |
|---|---|---|
| `background` | `color` | The colour underneath |

### Returns
A new `color`.

## rotate()
Returns the colour with its hue rotated round the wheel, wrapping, where 256 is a full turn.

### Usage
`.rotate(counts)`

| Parameter | Type | Description |
|---|---|---|
| `counts` | `int` | How far to turn, 256 being all the way round |

### Returns
A new `color` in the `oklch` space, fitted to what the screen can show.

## saturate()
Returns the colour with more chroma, on an OKLCH colour, or more saturation on an HSV one. A negative amount takes it out again. Values clamp at the ends, and the result is fitted.

### Usage
`.saturate(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | How much to add, or remove if negative |

### Returns
A new `color`.

# Measuring a colour
For choosing colours on a small screen: whether text can be read, and whether two colours can be told apart.

## contrast()
Returns the WCAG 2.1 contrast ratio against another colour, from `1.0` for identical colours to `21.0` for black on white. The audited thresholds are 3 for large text and interface components, 4.5 for body text at AA, and 7 at AAA. Alpha is ignored, so [`over()`](#over) either colour onto its background first if it's translucent.

### Usage
`.contrast(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `color` | The colour to measure against |

### Returns
A `float` from 1.0 to 21.0.

## difference()
Returns the perceptual distance to another colour, on a scale where black to white is 100. Around 2 is where a difference becomes noticeable and around 5 where it becomes obvious, so this is the way to check whether two colours in a palette are too close to tell apart. Alpha is ignored.

### Usage
`.difference(other)`

| Parameter | Type | Description |
|---|---|---|
| `other` | `color` | The colour to measure against |

### Returns
A `float`, where 100 is black to white.

## fit()
Returns the colour with only as much chroma as the screen can show at its lightness and hue: use it on an OKLCH colour that reads [`in_gamut`](#properties) as `False`. Colours already in gamut come back unchanged, as do RGB and HSV colours, which can't be out of it.

### Usage
`.fit()`

### Returns
A new `color`.

# Building a palette
These generate a set of colours around one you already have, for building an interface out of a single theme colour. They read the colour in OKLCH first, so a palette entry works as well as a colour authored there, and everything they return is fitted.

## harmony()
Returns a colour-wheel scheme around this colour, as a tuple with this colour first.

### Usage
`.harmony(scheme)`

| Parameter | Type | Description |
|---|---|---|
| `scheme` | `int` | One of the [harmony schemes](#harmony-schemes) |

### Returns
A `tuple` of 2 to 4 colours, this one first.

```python
base = color.oklch(160, 110, 40)
scheme = base.harmony(color.TETRAD)

def update():
  for i, swatch in enumerate(scheme):
    screen.pen = swatch
    screen.rectangle(i * 40, 30, 40, 60)

run(update)
```

## tones()
Returns a tonal ladder: `count` colours at evenly spaced lightness from black to white, holding this colour's hue and chroma. The surfaces of an interface, from one theme colour: background, panel, border, text.

### Usage
`.tones(count)`

| Parameter | Type | Description |
|---|---|---|
| `count` | `int` | How many steps, 1–64 |

### Returns
A `tuple` of `count` colours, darkest first.

```python
ladder = color.oklch(160, 90, 170).tones(8)

def update():
  for i, tone in enumerate(ladder):
    screen.pen = tone
    screen.rectangle(i * 20, 30, 20, 60)

run(update)
```

## readable_on()
Returns this colour moved along its lightness until it clears a given contrast ratio against a background, holding its hue and chroma. A colour that already clears the ratio comes back unchanged. A saturated mid-tone background can be unreachable from either direction, in which case you get the most readable colour there is rather than an error.

### Usage
`.readable_on(background)` \
`.readable_on(background, ratio)`

| Parameter | Type | Description |
|---|---|---|
| `background` | `color` | The colour the text will sit on |
| `ratio` | `float` | *Optional.* The contrast ratio to reach. Defaults to `4.5`, the AA threshold for body text |

### Returns
A new `color`.

```python
background = color.oklch(150, 90, 60)
label = color.oklch(150, 120, 200)      # same lightness, so unreadable as it is

def update():
  screen.pen = background
  screen.clear()

  screen.pen = label
  screen.text("As authored", 20, 40)

  screen.pen = label.readable_on(background)
  screen.text("Made readable", 20, 70)

run(update)
```

# Operators
The three arithmetic operators are shorthands for the adjustments above. Colours are immutable, so `c += 10` binds a new colour to `c`.

| Operator | Result |
|---|---|
| `c + n` | Lightened by `n`, as [`lighten()`](#lighten-darken) |
| `c - n` | Darkened by `n`, as [`darken()`](#lighten-darken) |
| `c * f` | Lightness scaled by a factor, so `c * 0.5` is [`scale(50)`](#scale) |
| `c == other`, `c != other` | Whether both render as the same colour, whatever space each was authored in |

# Constants

## Harmony schemes
Passed to [`harmony()`](#harmony) to pick which colours around the wheel you get back.

| Constant | Returns |
|---|---|
| `color.COMPLEMENT` | 2 colours, opposite each other |
| `color.SPLIT` | 3 colours: this one, and the two either side of its opposite |
| `color.TRIAD` | 3 colours, evenly spaced thirds |
| `color.TETRAD` | 4 colours, two complementary pairs |
| `color.SQUARE` | 4 colours, evenly spaced quarters |
| `color.ANALOGOUS` | 3 colours: this one and its neighbours either side |

## Default palette
A set of 16 named colours based on the [DawnBringer 16](https://lospec.com/palette-list/dawnbringer-16) palette.

These constants provide a convenient starting point for UI elements, sprites, and general drawing.

<style>
  #palette_grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(5rem, 1fr)); grid-gap: 0.25rem;

    >div {
      aspect-ratio: 1; font-size: 0.9rem; font-family: Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace; display: flex; align-items: center; justify-content: center;
      &:nth-child(n+9) {
        color: var(--black);
      }
    }
  }
</style>
<div id="palette_grid" style="">
  <div style="background-color: #141e28;">black</div>
  <div style="background-color: #442434;">grape</div>
  <div style="background-color: #30346d;">navy</div>
  <div style="background-color: #4e4a4e;">grey</div>
  <div style="background-color: #854c30;">brown</div>
  <div style="background-color: #346524;">green</div>
  <div style="background-color: #d04648;">red</div>
  <div style="background-color: #757161;">taupe</div>
  <div style="background-color: #597dce;">blue</div>
  <div style="background-color: #d27d2c;">orange</div>
  <div style="background-color: #8595a1;">smoke</div>
  <div style="background-color: #6daa2c;">lime</div>
  <div style="background-color: #d2aa99;">latte</div>
  <div style="background-color: #6dc2ca;">cyan</div>
  <div style="background-color: #dad45e;">yellow</div>
  <div style="background-color: #deeed6;">white</div>
</div>

```python
palette = [
  color.black, color.grape, color.navy, color.grey,
  color.brown, color.green, color.red, color.taupe,
  color.blue, color.orange, color.smoke, color.lime,
  color.latte, color.cyan, color.yellow, color.white
]
def update():
  for i in range(len(palette)):

    screen.pen = palette[i]
    screen.circle(32 + (i * 6), 60, 20)

run(update)
```
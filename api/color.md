---
title: color
summary: Methods for creating colours in a variety of different colourspaces and selecting colours from the built-in palette.
icon: palette
publish: true
---
# Introduction
Represents an RGBA colour.

The `color` type provides methods for creating colours from RGBA, HSV, and OKLCH colour spaces. Colours can be adjusted, blended, and combined using a range of utility methods.

Regardless of how a colour is constructed, it is stored internally as a premultiplied RGBA value.

# Properties

## p
The premultiplied RGBA color as a 32 bit unsigned integer.

# Static Methods
The following static methods create new `color` objects from different colour representations.

## rgb
Creates a new `color` object from red, green, blue, and optional alpha values.

### Usage
- `rgb(r, g, b[, a])`
    - `r, g, b`: Colour component values from 0 to 255
    - `a`: Optional alpha value from 0 to 255

### Returns
`color`

### Example
```python
def update():
  # draw a gradient from cyan to magenta
  for x in range(0, 160):
    step = (x * 255) / 160
    screen.pen = color.rgb(step, 255 - step, 150)
    screen.line(x, 0, x, 120)
```

## hsv
Creates a new `color` object from hue, saturation, value, and optional alpha values.

HSV is not perceptually uniform, so equal changes in its values do not correspond to equal perceived colour changes. This can lead to uneven gradients and unintuitive results when adjusting saturation or brightness.

### Usage
- `hsv(h, s, v[, a])`
    - `h`: Hue from 0 to 255
    - `s`: Saturation from 0 to 255
    - `v`: Value (brightness) from 0 to 255
    - `a`: Optional alpha value from 0 to 255

### Returns
`color`

### Example
```python
def update():
  # draw a hue gradient
  for x in range(0, 160):
    hue = 255 * (x / 160)
    saturation = 255
    value = 255
    screen.pen = color.hsv(hue, saturation, value)
    screen.line(x, 0, x, 120)
```

## oklch
Creates a new `color` object from OKLCH parameters and an optional alpha value.

OKLCH is a perceptually uniform colour space, meaning equal changes in its values produce more consistent visual changes. This makes it better suited for colour adjustment and interpolation than HSV, which can produce uneven or unexpected results.

### Usage
- `oklch(l, c, h[, a])`
    - `l`: Lightness from 0 to 255
    - `c`: Chroma (saturation) from 0 to 255
    - `h`: Hue from 0 to 255
    - `a`: Optional alpha value from 0 to 255

### Returns
`color`

### Example
```python
def update():
  for x in range(0, 160):
    lightness = 220
    chroma = 150
    hue = 255 * (x / 160)
    screen.pen = color.oklch(lightness, chroma, hue)
    screen.line(x, 0, x, 120)
```
# Constants

## Default palette
A set of 16 named colours based on the [DawnBringer 16](https://lospec.com/palette-list/dawnbringer-16) palette.

These constants provide a convenient starting point for UI elements, sprites, and general drawing.

<style>
  #palette_grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr; grid-gap: 0.25rem;

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
```
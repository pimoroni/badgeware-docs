---
title: brush
summary: Fill vector shapes with images, gradients or patterns — or transform what's underneath with effect brushes like blur, pixelate and darken.
icon: brush
publish: true
---
# Introduction
Brushes are a powerful tool when drawing vector shapes on Badgeware. Instead of a solid flat colour, they can paint an image, a smooth gradient, or a repeating pattern across the shapes you draw. In fact, `color` itself is a type of brush - anywhere that you might use `color` to set a pen, you can set that pen to a `brush` instead.

# Image brushes
One use of brushes is to fill a shape with an image rather than with a flat colour. The image should be loaded in as a variable as usual, then passed into `brush.image()`. You can also pass in a transformation matrix as a `mat3` to determine the size, translation and rotation of the image. This image will tile infinitely if its size is smaller than the shape it is filling.

### Usage
`brush.image(image, matrix)`

| Parameter | Type | Description |
|---|---|---|
| `image` | `image` | The image to use as the brush |
| `matrix` | `mat3` | A transformation matrix representing the size, translation and rotation of the image |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

skull = image.load("/system/assets/skull.png")

while True:
  t = mat3().translate(-12, -12).rotate(badge.ticks / 100).translate(80, 60).scale(math.sin(badge.ticks / 1000) * 4)
  imgbrush = brush.image(skull, t)

  screen.pen = imgbrush
  screen.shape(shape.circle(80, 60, 50))

  badge.update()
```

# Gradient brushes
A gradient brush fills a shape with a smooth blend between colours. A **linear** gradient runs the colours along a line, and a **radial** one spreads them outward from a point. You give it the type, the two points that define its axis, and a list of colour *stops* — each a position from `0` to `1` along the axis paired with a colour. An optional `mat3` can move, rotate or scale the whole gradient.

### Usage
`brush.gradient(type, x1, y1, x2, y2, stops, matrix)`

| Parameter | Type | Description |
|---|---|---|
| `type` | `int` | `brush.LINEAR` to blend along the axis, or `brush.RADIAL` to blend outward from the first point |
| `x1`, `y1` | `float` | The start of the gradient axis — the centre, for a radial gradient |
| `x2`, `y2` | `float` | The end of the axis; for a radial gradient this sets the outer radius |
| `stops` | `list` | Up to 16 `(position, color)` tuples, where `position` runs from `0` to `1` along the axis |
| `matrix` | `mat3` | *Optional.* A transformation applied to the gradient — its size, position and rotation |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
# every colour, all at once — graphic design is my passion
loud = [
  (0.0,  color.rgb(255, 0, 200)),   # hot pink
  (0.33, color.rgb(255, 230, 0)),   # yellow
  (0.66, color.rgb(0, 220, 255)),   # cyan
  (1.0,  color.rgb(120, 255, 0)),   # lime
]
clash = [(0.0, color.rgb(255, 0, 255)), (1.0, color.rgb(0, 255, 0))]

screen.antialias = image.X4     # smooth edges on the vector shapes
screen.font = font.nope

while True:
  # LINEAR: a clashing gradient right across the background
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 160, 120, loud)
  screen.clear()

  # RADIAL: the stops spread out from the centre — filling a very tasteful star
  screen.pen = brush.gradient(brush.RADIAL, 80, 50, 80, 98, clash)
  screen.shape(shape.star(80, 50, 9, 20, 46))

  # a gradient fills text just as it fills a shape (restraint is optional)
  screen.pen = color.black
  screen.text("Graphic design is my passion", -13, 105)          # drop shadow
  screen.pen = brush.gradient(brush.LINEAR, 0, 0, 200, 0, loud)
  screen.text("Graphic design is my passion", -16, 102)

  badge.update()
```

# Effect brushes
The brushes above paint new content into a shape. A second family instead *transforms the pixels already on the target* beneath the shape — the shape becomes a mask for an effect. They're ideal for spotlights, frosted-glass panels, pixelated censor boxes and vignettes, and all have antialiased edges.

The effect brushes on this page fall into a few groups: the simple masks below, then the [colour and tone brushes](#colour-and-tone-brushes), the [retro and screen brushes](#retro-and-screen-brushes), and the [artistic brushes](#artistic-brushes). Every one of them reads whatever is already on the target and rewrites it, so remember to draw your scene *first* — the effect only shows where there is something underneath it.

## pixelate()
Mosaics the area under the shape into blocks.

### Usage
`brush.pixelate(size)`

| Parameter | Type | Description |
|---|---|---|
| `size` | `int` | The block size in pixels (`1` or more) |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # mosaic everything to the right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.pixelate(6)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## blur()
Box-blurs the area under the shape.

### Usage
`brush.blur(radius)`

| Parameter | Type | Description |
|---|---|---|
| `radius` | `int` | The blur radius in pixels (`1` or more) |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # blur everything to the right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.blur(4)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## lighten() / darken()
Adds to (or subtracts from) every colour channel of the pixels under the shape, brightening or darkening what's already there.

### Usage
`brush.lighten(amount)` \
`brush.darken(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | How much to add or subtract per channel, `0`–`255` |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # darken the left of a sliding split, lighten the right
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.darken(70)
  screen.shape(shape.rectangle(0, 0, split, 240))
  screen.pen = brush.lighten(70)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## erase()
Punches through what's been drawn — fully transparent with no argument, or a translucent window tinted toward colour `c` if one is given.

### Usage
`brush.erase()` \
`brush.erase(c)`

| Parameter | Type | Description |
|---|---|---|
| `c` | `color` | *Optional.* Tint the erased window toward this colour instead of clearing to full transparency |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # erase everything to the right of a sliding split (pass a colour
  # to erase(...) for a translucent tinted window instead of a hole)
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.erase()
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

# Colour and tone brushes
These effect brushes leave the *shape* of what's underneath alone and instead re-map its colours — draining, boosting, posterising or recolouring the pixels beneath the shape. Like all effect brushes they feather in at antialiased edges, so a filter can fade smoothly across a soft-edged shape.

## monochrome()
Drains all colour from the area under the shape, leaving a greyscale image.

### Usage
`brush.monochrome()`

Takes no arguments.

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # drain the colour from everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.monochrome()
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## invert()
Photonegative — flips every colour channel of the pixels under the shape (`255 - value`).

### Usage
`brush.invert()`

Takes no arguments.

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # invert everything to the right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.invert()
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## saturation()
Pushes the colours under the shape toward or away from grey without changing their brightness.

### Usage
`brush.saturation(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | `0` leaves the colours unchanged; positive values boost the colour, negative values drain it. `-256` gives a fully greyscale result |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # boost the colour on everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.saturation(180)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## contrast()
Expands or compresses the pixels under the shape around mid-grey.

### Usage
`brush.contrast(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | `0` leaves the pixels unchanged; positive values increase contrast, negative values flatten it. `-256` collapses everything to mid-grey |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # add contrast to everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.contrast(160)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## threshold()
Hard two-tone posterisation: every pixel under the shape becomes one of two colours depending on how bright it is.

### Usage
`brush.threshold(level, lo, hi)`

| Parameter | Type | Description |
|---|---|---|
| `level` | `int` | The brightness cut-off, `0`–`255`. Pixels brighter than this become `hi`, the rest become `lo` |
| `lo` | `color` | The colour used for pixels at or below `level` |
| `hi` | `color` | The colour used for pixels above `level` |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # posterise everything right of a sliding split: bright pixels turn
  # lime, the rest navy
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.threshold(128, color.navy, color.lime)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## dither()
Ordered (Bayer) dither of the area under the shape down to a small, screen-aligned palette — a classic retro, low-colour look.

### Usage
`brush.dither()`

Takes no arguments.

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # dither everything to the right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.dither()
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## duotone()
Maps the brightness of the pixels under the shape onto a two-colour ramp — dark areas take the `shadow` colour, bright areas the `highlight` colour, with a smooth blend between. Great for sepia and other tinted looks.

### Usage
`brush.duotone(shadow, highlight)`

| Parameter | Type | Description |
|---|---|---|
| `shadow` | `color` | The colour the darkest pixels map to |
| `highlight` | `color` | The colour the brightest pixels map to |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # map everything right of a sliding split onto a warm sepia ramp
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.duotone(color.rgb(40, 20, 10), color.rgb(255, 230, 180))
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

# Retro and screen brushes
This family fakes the look of old displays and worn video — scanlines, vignettes, phosphor glow, chromatic fringing, grain and glitching. Several of them animate on their own (they read `badge.ticks` as they're built), so rebuild them inside your loop to see them move.

## crt()
A CRT tube look: darkens every few rows to fake scanlines, and rounds off the corners so the picture reads like a curved glass tube.

### Usage
`brush.crt(spacing, darkness)`

| Parameter | Type | Description |
|---|---|---|
| `spacing` | `int` | Scanline spacing — every `spacing`-th row is darkened (`1` or more) |
| `darkness` | `int` | How hard the scanlines darken, `0`–`255` |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # CRT scanlines and rounded corners over everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.crt(3, 60)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## vignette()
Darkens the pixels under the shape by their distance from the centre of the screen, so the frame falls off toward black at the corners.

### Usage
`brush.vignette(strength)`

| Parameter | Type | Description |
|---|---|---|
| `strength` | `int` | How dark the corners get, `0`–`255` |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # darken everything right of a sliding split by distance from the centre
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.vignette(220)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## phosphor()
Recolours the area under the shape as a glowing single-colour phosphor — bright pixels take the full `tint`, dark pixels stay dark. Perfect for green- or amber-screen terminals.

### Usage
`brush.phosphor(tint)`

| Parameter | Type | Description |
|---|---|---|
| `tint` | `color` | The phosphor colour the glow is tinted toward, e.g. a green or amber |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # recolour everything right of a sliding split as a green terminal
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.phosphor(color.rgb(0, 255, 0))
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## chromatic()
Chromatic aberration — pulls the red and blue channels apart horizontally to fake a mis-aligned lens or a cheap CRT.

### Usage
`brush.chromatic(offset)`

| Parameter | Type | Description |
|---|---|---|
| `offset` | `int` | How far, in pixels, to split the red and blue channels apart |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # split the red and blue channels on everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.chromatic(3)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## noise()
Adds film grain to the pixels under the shape — the same random amount is added to every channel of each pixel.

### Usage
`brush.noise(amount, interval)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | The most the grain can lighten or darken a pixel |
| `interval` | `int` | *Optional.* How often the grain refreshes, in milliseconds. `0` (the default) holds a single static pattern |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # add static film grain to everything right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.noise(30, 0)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## glitch()
Animated VHS-style datamosh — horizontal bands slide sideways with a magenta/cyan channel split, and the odd bright line flashes across the frame. It animates on its own from `badge.ticks`.

### Usage
`brush.glitch(amount)`

| Parameter | Type | Description |
|---|---|---|
| `amount` | `int` | How much glitching, `0`–`255` — scales how many bands break up, how far they slide, and how often the lines flash |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # break everything right of a sliding split into glitching bands
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.glitch(80)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

## nightvision()
A night-vision goggle look: amplifies everything into green, adds animated grain and darkens the edges.

### Usage
`brush.nightvision()`

Takes no arguments.

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # night-vision everything to the right of a sliding split
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.nightvision()
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

# Artistic brushes
A brush for turning the pixels under a shape into something that looks hand-made.

## oilpaint()
A painterly, oil-paint filter — replaces each pixel under the shape with the dominant colour of its neighbourhood, flattening detail into brush-stroke-like blobs, then eases the result back toward the original by `strength`.

### Usage
`brush.oilpaint(radius, strength)`

| Parameter | Type | Description |
|---|---|---|
| `radius` | `int` | The size of the neighbourhood each pixel looks at, `1`–`4`. Larger is chunkier (and slower) |
| `strength` | `int` | *Optional.* How strongly the painted result replaces the original, `0`–`255`. Defaults to `255` (fully painted) |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

badge.mode(HIRES)

while True:
  # a common scene for every example — a full-screen photo
  screen.load_into("/system/assets/tufty.png")

  # turn everything right of a sliding split into oil paint
  split = 160 + math.sin(badge.ticks / 1000) * 120
  screen.pen = brush.oilpaint(2)
  screen.shape(shape.rectangle(split, 0, 320 - split, 240))

  # mark the split with a white line
  screen.pen = color.white
  screen.line(split, 0, split, 240)

  badge.update()
```

# Pattern brushes
A pattern brush works similarly to an image brush, but instead of a picture a pattern of lit pixels is used. You can pass in the foreground and background colours of the pattern. Patterns can either be picked from the built in range in Badgeware, or you can specify a custom pattern by inputting it yourself as a tuple. These patterns remain static and are pixel scaled, so they cannot have a transformation matrix applied to them like an image brush can.

### Usage
`brush.pattern(col1, col2, pattern)`

| Parameter | Type | Description |
|---|---|---|
| `col1`, `col2` | `color` | The foreground and background colours of the pattern |
| `pattern` | `int` \| `tuple` | The pattern itself — either an integer selecting one of the built-in patterns, or a tuple of binary numbers representing a custom pattern |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

# a fully transparent colour, used as the patterns' background so the
# unlit pixels let whatever is behind them show through
TRANSPARENT = color.rgb(0, 0, 0, 0)

while True:
  # a custom pattern: each 0b number is one binary row, where the 1s and 0s
  # are the lit and unlit pixels of the pattern
  custom_pattern = brush.pattern(color.red, TRANSPARENT, (
    0b00000000,
    0b01111110,
    0b01000010,
    0b01011010,
    0b01011010,
    0b01000010,
    0b01111110,
    0b00000000))
  screen.pen = custom_pattern
  screen.shape(shape.circle(80 + math.cos(badge.ticks / 500) * 30, 60 + math.sin(badge.ticks / 1000) * 30, 30))

  built_in_pattern = brush.pattern(color.lime, TRANSPARENT, 11)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.sin(badge.ticks / 250) * 60, 60 + math.cos(badge.ticks / 500) * 60, 30))

  built_in_pattern = brush.pattern(color.blue, TRANSPARENT, 8)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.cos(badge.ticks / 250) * 60, 60 + math.sin(badge.ticks / 500) * 60, 30))

  badge.update()
```

## Built-in patterns
The patterns built in to Badgeware, selectable by index with `brush.pattern()`.

<style>
  .pattern-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(4rem, 1fr));
    gap: 0.75rem;
    margin: 1rem 0;
  }
  .pattern-grid figure { margin: 0; text-align: center; }
  .pattern-grid img {
    width: 100%; display: block; border-radius: 0.25rem;
    image-rendering: pixelated;
  }
  .pattern-grid figcaption {
    font-size: 0.8rem; color: var(--faint); margin-top: 0.3rem;
  }
</style>

<div class="pattern-grid">
<figure><img src="/docs/patterns/pattern0.png"><figcaption>0</figcaption></figure>
<figure><img src="/docs/patterns/pattern1.png"><figcaption>1</figcaption></figure>
<figure><img src="/docs/patterns/pattern2.png"><figcaption>2</figcaption></figure>
<figure><img src="/docs/patterns/pattern3.png"><figcaption>3</figcaption></figure>
<figure><img src="/docs/patterns/pattern4.png"><figcaption>4</figcaption></figure>
<figure><img src="/docs/patterns/pattern5.png"><figcaption>5</figcaption></figure>
<figure><img src="/docs/patterns/pattern6.png"><figcaption>6</figcaption></figure>
<figure><img src="/docs/patterns/pattern7.png"><figcaption>7</figcaption></figure>
<figure><img src="/docs/patterns/pattern8.png"><figcaption>8</figcaption></figure>
<figure><img src="/docs/patterns/pattern9.png"><figcaption>9</figcaption></figure>
<figure><img src="/docs/patterns/pattern10.png"><figcaption>10</figcaption></figure>
<figure><img src="/docs/patterns/pattern11.png"><figcaption>11</figcaption></figure>
<figure><img src="/docs/patterns/pattern12.png"><figcaption>12</figcaption></figure>
<figure><img src="/docs/patterns/pattern13.png"><figcaption>13</figcaption></figure>
<figure><img src="/docs/patterns/pattern14.png"><figcaption>14</figcaption></figure>
<figure><img src="/docs/patterns/pattern15.png"><figcaption>15</figcaption></figure>
<figure><img src="/docs/patterns/pattern16.png"><figcaption>16</figcaption></figure>
<figure><img src="/docs/patterns/pattern17.png"><figcaption>17</figcaption></figure>
<figure><img src="/docs/patterns/pattern18.png"><figcaption>18</figcaption></figure>
<figure><img src="/docs/patterns/pattern19.png"><figcaption>19</figcaption></figure>
<figure><img src="/docs/patterns/pattern20.png"><figcaption>20</figcaption></figure>
<figure><img src="/docs/patterns/pattern21.png"><figcaption>21</figcaption></figure>
<figure><img src="/docs/patterns/pattern22.png"><figcaption>22</figcaption></figure>
<figure><img src="/docs/patterns/pattern23.png"><figcaption>23</figcaption></figure>
<figure><img src="/docs/patterns/pattern24.png"><figcaption>24</figcaption></figure>
<figure><img src="/docs/patterns/pattern25.png"><figcaption>25</figcaption></figure>
<figure><img src="/docs/patterns/pattern26.png"><figcaption>26</figcaption></figure>
<figure><img src="/docs/patterns/pattern27.png"><figcaption>27</figcaption></figure>
<figure><img src="/docs/patterns/pattern28.png"><figcaption>28</figcaption></figure>
<figure><img src="/docs/patterns/pattern29.png"><figcaption>29</figcaption></figure>
<figure><img src="/docs/patterns/pattern30.png"><figcaption>30</figcaption></figure>
<figure><img src="/docs/patterns/pattern31.png"><figcaption>31</figcaption></figure>
<figure><img src="/docs/patterns/pattern32.png"><figcaption>32</figcaption></figure>
<figure><img src="/docs/patterns/pattern33.png"><figcaption>33</figcaption></figure>
<figure><img src="/docs/patterns/pattern34.png"><figcaption>34</figcaption></figure>
<figure><img src="/docs/patterns/pattern35.png"><figcaption>35</figcaption></figure>
<figure><img src="/docs/patterns/pattern36.png"><figcaption>36</figcaption></figure>
<figure><img src="/docs/patterns/pattern37.png"><figcaption>37</figcaption></figure>
</div>

<style>
  /* a full-page layer that sits behind the content (above the gradient) and
     fades in a tiled pattern while a swatch above is hovered */
  #pattern-page-bg {
    position: fixed; inset: 0; z-index: -1; pointer-events: none;
    background-repeat: repeat; image-rendering: pixelated;
    opacity: 0; transition: opacity 0.5s ease;
  }
  #pattern-page-bg.active { opacity: 0.03; }
  .pattern-grid figure { cursor: pointer; }
</style>
<script>
  (function () {
    var bg = document.createElement("div");
    bg.id = "pattern-page-bg";
    document.body.appendChild(bg);

    document.querySelectorAll(".pattern-grid figure").forEach(function (fig) {
      var img = fig.querySelector("img");
      if (!img) return;
      fig.addEventListener("mouseenter", function () {
        bg.style.backgroundImage = "url('" + img.src + "')";
        bg.classList.add("active");
      });
      fig.addEventListener("mouseleave", function () {
        bg.classList.remove("active");
      });
    });
  })();
</script>

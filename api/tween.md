---
title: tween
summary: Maps a progress value to an eased value between two endpoints — smooth animation that holds no clock of its own.
icon: timeline
publish: true
---
# Introduction
A `tween` smoothly moves a value from a **start** to an **end**. You give it a *progress* — a number from `0` (at the start) to `1` (at the end) — and it hands back the value that far along the way. Ask for `0.5` and you get the halfway value.

What makes it more than plain arithmetic is *easing*. Instead of moving at a constant speed, the value can start slow and speed up, overshoot and settle, or bounce — so motion feels natural rather than mechanical. You pick the curve when you create the tween.

A tween keeps no clock of its own: you decide the progress and read the value back with `at()`.

```python-raw
# a value that eases from 0 to 100
fade = tween(0, 100, easing=tween.QUAD_OUT)

fade.at(0)     # -> 0.0    the start
fade.at(0.5)   # -> 75.0   eased, so already past halfway
fade.at(1)     # -> 100.0  the end
```

Usually the progress comes from the clock, which keeps the animation smooth and running at the same speed on any badge (see the example under [`at()`](#at) below). The start and end don't have to be numbers, either — they can be a `vec2`, `rect` or `mat3`, so one tween can animate a position, a rectangle, or a whole transformation.

# Constructor

## tween()
Creates a tween between two endpoints, with an optional duration and easing curve.

### Usage
`tween(start, end)` \
`tween(start, end, duration, easing)`

| Parameter | Type | Description |
|---|---|---|
| `start` | `float` \| `vec2` \| `rect` \| `mat3` | The value at progress 0 |
| `end` | `float` \| `vec2` \| `rect` \| `mat3` | The value at progress 1 |
| `duration` | `float` | *Optional.* Duration in seconds. The default, `1.0`, means `at()` takes a progress from 0 to 1. |
| `easing` | `int` | *Optional.* An easing constant (see below). Defaults to `tween.LINEAR`. |

### Returns
A `tween` object.

# Properties
All properties are read-only.

| Property | Type | Description |
|---|---|---|
| `start` | *endpoint* | The start endpoint |
| `end` | *endpoint* | The end endpoint |
| `duration` | `float` | The duration in seconds (`1.0` = a progress from 0 to 1) |

# Methods

## at()
Returns the eased value at progress `t`. With the default duration of `1.0`, `t` is a fraction from 0 to 1; if a duration in seconds was given, `t` is the elapsed time in seconds. Progress outside the range is clamped to the endpoints.

### Usage
`.at(t)`

| Parameter | Type | Description |
|---|---|---|
| `t` | `float` | Progress — a 0–1 fraction, or elapsed seconds if a duration was set |

### Returns
The eased value, of the same type as the endpoints.

For example, a ball crossing the screen at a steady pace while bouncing as it falls. Both positions read from the same progress `p`: `x` uses a `LINEAR` tween (even speed), `y` a `BOUNCE_OUT` one (settles with a bounce). The value of `p` is printed beneath the ball as it travels:

```python
# same progress drives both: x moves evenly, y bounces
across = tween(12, 148, easing=tween.LINEAR)
drop = tween(16, 92, easing=tween.BOUNCE_OUT)

screen.font = font.sins

while True:
  screen.pen = color.black
  screen.clear()

  p = badge.ticks % 2000 / 2000    # 0 -> 1 every 2 seconds
  x = across.at(p)

  screen.pen = color.orange
  screen.circle(x, drop.at(p), 6)

  # print the progress, sliding along beneath the ball
  screen.pen = color.white
  screen.text("{:.2f}".format(p), x - 8, 104)

  badge.update()
```

# Easing constants
The `easing` argument selects the curve applied between the endpoints. `LINEAR` interpolates at a constant rate; every other family comes in three variants — `_IN` eases away from the start, `_OUT` eases into the end, and `_INOUT` eases at both.

| Family | Constants |
|---|---|
| Linear | `tween.LINEAR` |
| Quadratic | `tween.QUAD_IN`, `tween.QUAD_OUT`, `tween.QUAD_INOUT` |
| Cubic | `tween.CUBIC_IN`, `tween.CUBIC_OUT`, `tween.CUBIC_INOUT` |
| Quartic | `tween.QUART_IN`, `tween.QUART_OUT`, `tween.QUART_INOUT` |
| Quintic | `tween.QUINT_IN`, `tween.QUINT_OUT`, `tween.QUINT_INOUT` |
| Sine | `tween.SINE_IN`, `tween.SINE_OUT`, `tween.SINE_INOUT` |
| Exponential | `tween.EXPO_IN`, `tween.EXPO_OUT`, `tween.EXPO_INOUT` |
| Circular | `tween.CIRC_IN`, `tween.CIRC_OUT`, `tween.CIRC_INOUT` |
| Back (overshoot) | `tween.BACK_IN`, `tween.BACK_OUT`, `tween.BACK_INOUT` |
| Elastic | `tween.ELASTIC_IN`, `tween.ELASTIC_OUT`, `tween.ELASTIC_INOUT` |
| Bounce | `tween.BOUNCE_IN`, `tween.BOUNCE_OUT`, `tween.BOUNCE_INOUT` |

# Easing reference
A visual guide to every curve. `_IN` starts slow, `_OUT` ends slow, and `_INOUT` eases at both ends.

<figure style="text-align: center; margin: 1.5em auto;">
  <img src="/docs/api/assets/easing-curves.svg" alt="Easing curves for every constant: each family's IN, OUT and INOUT variants plotted from 0 to 1" style="display: block; margin: 0 auto; max-width: 100%; height: auto;">
  <figcaption style="margin-top: 0.6em; font-style: italic; font-size: 0.85em; opacity: 0.7;">Each plot runs progress left-to-right against the eased value bottom-to-top; the faint diagonal is linear, for comparison.</figcaption>
</figure>

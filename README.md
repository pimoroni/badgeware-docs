---
title: Welcome to Badgeware!
summary: An introduction to Badgeware and the Badgeware SDK
hide_toc: true
---

# Welcome to Badgeware!

Badgeware is a MicroPython-powered platform for our family of programmable badges — **Tufty**, **Badger**, and **Blinky**. Write a short Python script, copy it to your badge over USB, and it runs. No toolchains, no compilers, no fuss.

Each badge runs the same API, so code you write for one model will mostly work on the others. The main differences are screen resolution, colour, and refresh behaviour — see [Coding for the different badges](/introduction/badge-differences.md) for the full details.

---

## Meet the badges

| | **Tufty** | **Badger** | **Blinky** |
|---|----------|----------|----------|
| | ![Tufty](/assets/tufty_web_front.png) | ![Badger](/assets/tufty_web_front.png) | ![Blinky](/assets/tufty_web_front.png) |
| **Display** | 320x240 full-colour IPS LCD | 264x176 e-paper (black, white, 2 greys) | 39x26 LED matrix (255 levels greyscale) |
| **Best for** | Graphics-heavy apps, games, animations | Low-power name badges, dashboards, e-readers | Wearable light displays, pixel art, notifications |
| **Refresh** | Continuous — redraws as fast as your code runs | Sleeps between updates — perfect for all-day battery life | Continuous — smooth animations at high frame rates |
| **Battery** | 1000mAh rechargeable (up to 8 hours active) | 1000mAh rechargeable (up to 100 days standby) | 1000mAh rechargeable (up to 8 hours active) |

All three are powered by the **RP2350** (dual-core ARM Cortex-M33 @ 200MHz) with 16MB flash, 8MB PSRAM, WiFi, Bluetooth 5, and USB-C. See [The hardware](/introduction/hardware.md) for the full spec.

---

## A taste of Badgeware

Every app is built around a single `update()` function that the badge calls once per frame. Here's the smallest complete app:

```python
def update():
    screen.pen = color.navy
    screen.clear()

    screen.pen = color.white
    screen.font = rom_font.smart
    screen.text("Hello, world!", 10, 50)

run(update)
```

Want to make it interactive? Add button input:

```python
messages = ["Hello, world!", "Badgeware rocks!", "Press a button!"]
current = 0

def update():
    global current

    if badge.pressed(BUTTON_UP):
        current = (current + 1) % len(messages)

    screen.pen = color.navy
    screen.clear()

    screen.pen = color.white
    screen.font = rom_font.smart

    text = messages[current]
    width, _ = screen.measure_text(text)
    x = (screen.width / 2) - (width / 2)

    screen.text(text, x, 50)

run(update)
```

Press **Up** to cycle through the messages. That's it — everything else is just building on these ideas.

---

## Start here

New to Badgeware? Work through these in order.

1. [Getting Started](/introduction/getting-started.md) — plug in, create your first app, and run it in minutes
2. [Creating an app](/introduction/your-first-app.md) — the full app structure, including `init()` and `on_exit()`
3. [The hardware](/introduction/hardware.md) — what's inside your badge
4. [Coding for the different badges](/introduction/badge-differences.md) — how Tufty, Badger, and Blinky differ and how to handle it
5. [Badge modes](/introduction/editing-on-device.md) — Disk Mode, deep sleep, and firmware updates

Then try one of the tutorials:

- [Tutorial 1: A Simple Badge](/tutorials/creating_a_simple_badge.md) — images, text, and interaction
- [Tutorial 2: Dashboard](/tutorials/creating_a_dashboard.md) — fetching and displaying live data
- [Tutorial 3: A Simple Game](/tutorials/creating_a_game.md) — animation, input, and game loops

---

## Guides

Feature-focused walkthroughs for when you're ready to go deeper.

- [Text](/guides/text.md) — fonts, colour, positioning, and effects like drop shadows
- [Buttons](/guides/buttons.md) — single presses, holds, and building menus
- [Sprites](/guides/sprites.md) — loading and drawing images and sprite sheets
- [Vector Shapes](/guides/vector_shapes.md) — lines, circles, polygons, and transforms
- [Files](/guides/filesystem.md) — reading and writing to the badge filesystem
- [Time](/guides/time.md) — the real-time clock and scheduling updates
- [Animation](/guides/animation.md) — smooth movement and frame timing
- [The Framebuffer](/guides/framebuffer.md) — how the screen works under the hood

---

## API reference

The full reference for every module. Useful when you know what you want but need the exact method signature.

- [badge](/api/badge.md) — buttons, LEDs, and system control
- [image](/api/image.md) — loading and drawing images
- [color](/api/color.md) — named colours and custom RGB values
- [brush](/api/brush.md) — pens, fills, and drawing styles
- [font](/api/font.md) — loading and using fonts
- [pixel_font](/api/pixel_font.md) — bitmap pixel fonts
- [text](/api/text.md) — drawing and measuring text
- [shape](/api/shape.md) — vector shape primitives
- [SpriteSheet](/api/SpriteSheet.md) — sprite sheet loading and animation
- [rect](/api/rect.md) — rectangle helpers
- [vec2](/api/vec2.md) — 2D vector maths
- [mat3](/api/mat3.md) — 3x3 transformation matrices
- [algorithm](/api/algorithm.md) — path-finding, sorting, and utilities
- [rtc](/api/rtc.md) — real-time clock
- [filesystem](/api/filesystem.md) — file and storage access

---

## What's new

**28th February 2026** — Firmware 2.0.1 is out! Fixes for FAT filesystem corruption, vector shape rendering, deep sleep power consumption, and more. A new `badge` module replaces `io` with many extra features. See the [full release notes](https://github.com/pimoroni/badger2350/releases/tag/v2.0.1) and [how to update](/introduction/update-your-firmware.md).

---

## Get help

- [GitHub](https://github.com/pimoroni/badgeware-docs) — report issues or suggest improvements to these docs
- [Pimoroni Store](https://shop.pimoroni.com) — pick up accessories and breakouts

---
title: Welcome to Badgeware!
summary: An introduction to Badgeware and the Badgeware SDK
---

# Welcome to Badgeware!

Badgeware is a MicroPython-powered platform for our family of programmable badges — **Tufty**, **Badger**, and **Blinky**. Write a short Python script, copy it to your badge over USB, and it runs. No toolchains, no compilers, no fuss.

Your badge comes preloaded with a set of apps, but the real fun starts when you write your own. Everything is built around a simple `update()` function that the badge calls once per frame — draw to the screen, read some buttons, and you've got an app. If you've ever written a few lines of Python, you already have everything you need to get started.

This site is your guide. You'll find step-by-step tutorials to get you up and running, feature guides that go deeper on topics like sprites, text, and vector shapes, and a full API reference for when you need the details. Whether you're building a name badge for a conference, a tiny game to pass the time, or a dashboard that pulls live data over WiFi — it all starts here.

# Meet the badges

## Tufty

A full-colour IPS LCD badge with a 320x240 display (or 160x120 in low-res mode for extra performance). Tufty is the most versatile of the three — its high refresh rate and RGB colour make it ideal for graphics-heavy apps, games, animations, and rich user interfaces. The screen redraws continuously, so your `update()` function runs as fast as your code allows. If you want smooth movement and vibrant visuals, Tufty is the one to reach for.

## Badger

An e-paper badge with a 264x176 display in black, white, and two shades of grey. E-paper only draws power when the screen updates, so Badger is designed around that — it sleeps between updates and wakes on a button press or RTC alarm. This makes it perfect for things that don't need to change often: name badges, conference schedules, dashboards, to-do lists, and e-readers. A single charge can last up to 100 days in standby. The trade-off is speed — full screen refreshes take a moment, though a fast-update mode is available for more responsive interfaces.

## Blinky

A 39x26 LED matrix badge with 255 levels of brightness per pixel, making it essentially a greyscale display you can wear. Blinky is compact, eye-catching, and great for scrolling text, pixel art, simple animations, and notification displays. Like Tufty, it refreshes continuously so animations run smoothly. The matrix has cutouts for case corners and buttons — anything drawn into those pixels is automatically ignored, so you don't need to worry about them in your code.

## What they have in common

Despite their different displays, all three badges share the same core hardware and software platform:

- **Processor** — RP2350 dual-core ARM Cortex-M33 @ 200MHz with hardware floating point
- **Memory** — 16MB flash for firmware, code, and assets plus 8MB PSRAM for runtime use
- **Connectivity** — 2.4GHz WiFi and Bluetooth 5 for downloading data, syncing, or communicating between badges
- **Power** — 1000mAh rechargeable battery with USB-C charging
- **Expansion** — Qw/ST port for connecting breakout accessories, SWD port for debugging
- **Inputs** — five front-facing buttons, plus RESET and BOOTSEL on the back
- **Software** — the same Badgeware MicroPython API, so code written for one badge runs on the others with minimal changes
- **Disk Mode** — double-tap RESET to mount the badge as a USB drive, drag your files on, eject, and go

See [The hardware](/introduction/hardware.md) for the full spec.

Each badge runs the same API, so code you write for one model will mostly work on the others. The main differences are screen resolution, colour, and refresh behaviour — see [Coding for the different badges](/introduction/badge-differences.md) for the full details.

# A taste of Badgeware

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

# Start here

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

# Guides

Feature-focused walkthroughs for when you're ready to go deeper.

- [Text](/guides/text.md) — fonts, colour, positioning, and effects like drop shadows
- [Buttons](/guides/buttons.md) — single presses, holds, and building menus
- [Sprites](/guides/sprites.md) — loading and drawing images and sprite sheets
- [Vector Shapes](/guides/vector_shapes.md) — lines, circles, polygons, and transforms
- [Files](/guides/filesystem.md) — reading and writing to the badge filesystem
- [Time](/guides/time.md) — the real-time clock and scheduling updates
- [Animation](/guides/animation.md) — smooth movement and frame timing
- [The Framebuffer](/guides/framebuffer.md) — how the screen works under the hood

# API reference

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

# What's new

**28th February 2026** — Firmware 2.0.1 is out! Fixes for FAT filesystem corruption, vector shape rendering, deep sleep power consumption, and more. A new `badge` module replaces `io` with many extra features. See the [full release notes](https://github.com/pimoroni/badger2350/releases/tag/v2.0.1) and [how to update](/introduction/update-your-firmware.md).

# Get help

- [GitHub](https://github.com/pimoroni/badgeware-docs) — report issues or suggest improvements to these docs
- [Pimoroni Store](https://shop.pimoroni.com) — pick up accessories and breakouts

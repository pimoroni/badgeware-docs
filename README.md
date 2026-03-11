## Welcome to Badgeware! ❤️

Badgeware is a MicroPython-powered platform for our family of programmable badges — **Tufty**, **Badger**, and **Blinky** (aka Badgeware). Write a short Python script, copy it to your badge over USB, and it runs. No toolchains, no compilers, no fuss.

Each badge runs the same API, so code you write for one model will mostly work on the others. The main differences are screen resolution and colours — see [Coding for the different badges](/introduction/badge-differences.md) for the details.

---

## A taste of Badgeware

Every app is built around a single `update()` function that the badge calls once per frame. Here's the smallest complete app:

```python
def update():
    # screen.pen = color.navy
    # screen.clear()

    # screen.pen = color.white
    # screen.font = rom_font.smart
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

    text = messages[current]
    width, _ = screen.measure_text(text)
    x = (screen.width / 2) - (width / 2)

    screen.text(text, x, 50)

run(update)
```

Press **Up** to cycle through the messages. That's pretty much it — everything else is just building on these ideas.

---

## Start here

New to Badgeware? Work through these in order.

- [Getting Started](/introduction/getting-started.md) — plug in, create your first app, and run it in minutes
- [Creating an app](/introduction/your-first-app.md) — the full app structure, including `init()` and `on_exit()`
- [The hardware](/introduction/hardware.md) — what's inside your badge
- [Coding for the different badges](/introduction/badge-differences.md) — how Tufty, Badger, and Blinky differ and how to handle it
- [Badge modes](/introduction/editing-on-device.md) — Disk Mode, deep sleep, and firmware updates
- [Tutorial 1: Absolute Beginners](/introduction/tutorial_1.md) — a longer guided project with images, text, and interaction

---
<!--
## Guides

Feature-focused walkthroughs for when you're ready to go further.

- [Text](/guides/text.md) — fonts, colour, positioning, and effects like drop shadows
- [Buttons](/guides/buttons.md) — single presses, holds, and building menus
- [Sprites](/guides/sprites.md) — loading and drawing images and sprite sheets
- [Vector Shapes](/guides/vector_shapes.md) — lines, circles, polygons, and transforms
- [Algorithms](/guides/algorithms.md) — path-finding, sorting, and other built-in utilities
- [Files](/guides/files.md) — reading and writing to the badge filesystem
- [Time](/guides/time.md) — the real-time clock and scheduling updates

--- -->

## API reference

The full reference for every module. Useful when you know what you want but need the exact method signature.

- [image](/api/image.md)
- [color](/api/color.md)
- [brush](/api/brush.md)
- [shape](/api/shape.md)
- [mat3](/api/mat3.md)
- [rect](/api/rect.md)
- [vec2](/api/vec2.md)
- [pixel_font](/api/pixel_font.md)
- [io](/api/io.md)

---

## What's new

**28th February 2026** — Firmware update available. See [Updating your firmware](/introduction/update-your-firmware.md) for instructions.

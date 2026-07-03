---
title: Welcome to Badgeware!
summary: An introduction to Badgeware and the Badgeware SDK
hide_toc: true
---

# Welcome to Badgeware!

Badgeware is a MicroPython-powered platform for our family of programmable badges — **Tufty**, **Badger**, and **Blinky**. Write a short Python script, copy it to your badge over USB, and it runs. No toolchains, no compilers, no fuss.

Your badge comes preloaded with a set of apps, but the real fun starts when you write your own. Everything is built around a simple `update()` function that the badge calls once per frame — draw to the screen, read some buttons, and you've got an app. If you've ever written a few lines of Python, you already have everything you need to get started.

This site is your guide. You'll find step-by-step tutorials to get you up and running, feature guides that go deeper on topics like sprites, text, and vector shapes, and a full API reference for when you need the details. Whether you're building a name badge for a conference, a tiny game to pass the time, or a dashboard that pulls live data over WiFi — it all starts here.

New here? Head straight to **[Getting started](/introduction/getting-started.md)** to write your first app in minutes.

# Meet the badges

There are three badges in the family, each with its own kind of display — but they all run the same Badgeware API, so code you write for one will mostly work on the others. Where they differ is resolution, colour, and how the screen refreshes.

| Tufty | Badger | Blinky |
|---|---|---|
|<tufty-model environment="neutral" shadow-intensity="1" camera-orbit="0deg 78deg 85%" loading="lazy" style="display:block;width:100%;aspect-ratio:1/1" alt="Tufty badge"></tufty-model>|<badger-model environment="neutral" shadow-intensity="1" camera-orbit="0deg 78deg 85%" loading="lazy" style="display:block;width:100%;aspect-ratio:1/1" alt="Badger badge"></badger-model>|<blinky-model environment="neutral" shadow-intensity="1" camera-orbit="0deg 78deg 85%" loading="lazy" style="display:block;width:100%;aspect-ratio:1/1" alt="Blinky badge"></blinky-model>|
| *The versatile all-rounder — smooth, vivid, and up for anything graphical.* | *The low-power one — sips battery and idles for up to 100 days.* | *The little showpiece — tiny, bright, and made to be worn.* |
| Full-colour IPS LCD | E-paper display | Greyscale LED matrix |
| 320×240 (or 160×120) | 264×176 | 39×26 |
| Full RGB colour | Black, white + 2 greys | Bright white LEDs |
| Redraws continuously | Updates on demand, sleeps between | Redraws continuously |
| Great for games, animation, and rich UIs | Great for name badges, dashboards, and e-readers | Great for scrolling text, pixel art, and notifications |

# Shared hardware

Despite their different displays, all three badges share the same core hardware and software platform:

| | |
|---|---|
| **Processor** | RP2350 dual-core ARM Cortex-M33 @ 200MHz with hardware floating point |
| **Memory** | 16MB flash for firmware, code, and assets, plus 8MB PSRAM for runtime use |
| **Connectivity** | 2.4GHz WiFi and Bluetooth 5 for downloading data, syncing, or communicating between badges |
| **Power** | 1000mAh rechargeable battery with USB-C charging |
| **Expansion** | Qw/ST port for connecting breakout accessories, SWD port for debugging |
| **Inputs** | Five front-facing buttons, plus RESET and BOOTSEL on the back |
| **Software** | The same Badgeware MicroPython API, so code written for one badge runs on the others with minimal changes |
| **Disk Mode** | Double-tap RESET to mount the badge as a USB drive, drag your files on, eject, and go |

# A taste of Badgeware

Every app is built around a single `update()` function that the badge calls once per frame. Here's a quick example — a bouncing ball with a greeting, in about 20 lines:

```python
x, y = 80, 60
dx, dy = 2, 1

while True:
    x, y = x + dx, y + dy
    if x < 5 or x > screen.width - 5:  dx = -dx
    if y < 5 or y > screen.height - 5: dy = -dy

    screen.pen = color.navy
    screen.clear()

    screen.pen = color.orange
    screen.circle(x, y, 10)

    screen.pen = color.white
    screen.font = rom_font.smart
    screen.text("Hello, Badgeware!", 24, 50)
```

That's a complete, runnable app — copy it onto your badge and it just works. Everything else is building on these ideas: drawing to the screen, reading buttons, and letting `update()` do its thing.

# Where to next

- **[Getting started](/introduction/getting-started.md)** — plug in and run your first app in minutes.
- **[Creating your first app](/introduction/your-first-app.md)** — the full app structure, including `init()` and `on_exit()`.
- **[Coding for the different badges](/introduction/badge-differences.md)** — how Tufty, Badger, and Blinky differ, and how to write code that runs on all three.
- **[Guides](/README.md#guides)** — go deeper on sprites, text, vector shapes, animation, and more.
- **[API reference](/README.md#api)** — the details, for when you need them.

Happy hacking!
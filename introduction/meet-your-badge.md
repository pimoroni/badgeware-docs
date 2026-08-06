---
title: Meet your badge
summary: Meet your Badgeware badge — a quick tour of what's inside and what it can do.
icon: rocket
publish: true
sort: 1
---
# Meet your badge

Before you write a line of code, let's take a tour of the hardware. You'll learn what every part does, and why it's there.

# Display

Every badge is built around its display, the one feature that sets the three apart. Each has a completely different kind of screen, so the badge you choose shapes how your apps look and feel. The good news: you draw to all of them with the same commands, so code written for one mostly runs on the others — see **[Coding for the different badges](/guides/badge-differences.md)** for more specific information on how to deal with their differences.

| Tufty | Badger | Blinky |
|---|---|---|
| <tufty-model shadow lighting="150" position="-3 30 0" model-offset="-0.002m 0m 0m" camera="0deg 90deg 45%" style="aspect-ratio:1 / 1"></tufty-model> | <badger-model shadow lighting="150" position="-3 30 0" model-offset="-0.002m 0m 0m" camera="0deg 90deg 45%" style="aspect-ratio:1 / 1"></badger-model> | <blinky-model shadow lighting="150" position="-3 30 0" model-offset="-0.002m 0m 0m" camera="0deg 90deg 45%" style="aspect-ratio:1 / 1"></blinky-model> |
| Full-colour IPS LCD | E Ink display | Greyscale LED matrix |
| 320 × 240 | 264 × 176 | 39 × 26 |
| Full RGB colour | Black, white + 2 greys | Bright white greyscale |
| Redraws continuously | Updates on demand, sleeps between | Redraws continuously |
| Games, animation, and rich UIs | Name badges, dashboards, and e-readers | Scrolling text, pixel art, and notifications |

In short: reach for **Tufty** when you want colour, motion, and rich graphics; **Badger** when you want low power and always-on, glare-free text; and **Blinky** when you want a bright, bold display that makes you stand out in a crowd. 😎

# Buttons

<figure class="feature-callout">
<div class="callout-media">
<tufty-model hotspots="user-buttons" float shadow camera-target="0.014m 0.004m 0m" camera="28deg 80deg 90%"></tufty-model>
</div>
<figcaption>Five soft-touch buttons — everything your apps need to feel interactive.</figcaption>
</figure>

Five tactile buttons on the front — **A**, **B**, **C**, **UP**, and **DOWN** — are how people interact with your apps: scroll a menu, flip a page, fire a shot, cast a vote.

<figure class="feature-callout">
<div class="callout-media">
<tufty-model hotspots="system-buttons" float shadow camera-target="0m 0.004m 0m" camera="210deg 77deg 90%"></tufty-model>
</div>
</figure>

On the back are two more buttons — **RESET** and **HOME**. Look closely and each carries smaller secondary labels: RESET also reads **DISK** and **SLEEP**, and HOME also reads **BOOT**. That's because the function depends on how you press them.

| Action | What it does |
|---|---|
| Tap HOME | Returns to the main menu |
| Tap RESET | Reboots the badge |
| Double-tap RESET | Enters Disk Mode — mounts as a USB drive |
| Press and hold RESET | Enters battery-saving deep sleep (any front button wakes it) |
| Hold HOME, then tap RESET | Enters the RP2350 firmware bootloader for updates |

# USB-C

<figure class="feature-callout">
<div class="callout-media">
<tufty-model hotspots="usb-c" float shadow camera-target="-0.014m 0.004m 0.002m" camera="-46deg 80deg 90%"></tufty-model>
</div>
<figcaption>USB-C — the badge's one connection for power, charging, and moving your code and files.</figcaption>
</figure>

A single USB-C port on the left-hand edge does it all: powers the badge, tops up the battery, and carries your code across from your computer.

When plugged in your badge keeps a built-in **1,000mAh rechargeable LiPo battery** charged, and carries on running for hours after you unplug it. Or for days on Badger's ultra-low-power E Ink display.

Double-tap **RESET** and the badge mounts as an ordinary USB disk. Drag your apps and assets over and eject. No toolchains, no drivers, no fuss.

Prefer a live workflow? You can also use an editor like **VS Code** (with the [MicroPico](https://github.com/paulober/MicroPico) extension) or [Thonny](https://thonny.org) to write, run, and debug code on your badge in real time. Thonny is especially beginner friendly and a great way to get started.

# Wearable

The lanyard slot and mounting holes are part of the PCB itself, which extends up beyond the top of the clear polycarbonate case for a secure anchor point. Your badge is ready to wear from the moment you power it on.

But it doesn't have to hang around your neck. The shape of the case also lets Badgeware stand upright on any flat surface — ideal for turning it into a tiny internet-connected display for your desk.

# Wi-Fi & Bluetooth

Built-in **2.4GHz WiFi** and **Bluetooth 5.2** let you pull live data over the air, sync your details, show announcements, or have badges talk to each other — perfect for networking games, shared experiences, and dashboards that keep themselves up to date.

# Expansion & debugging

<figure class="feature-callout">
<div class="callout-media">
<tufty-model hotspots="qwst-swd" float shadow camera-target="0m 0.004m 0m" camera="224deg 76deg 88%"></tufty-model>
</div>
</figure>

The **Qw/ST connector** is a standard I2C port — plug in sensors and breakouts with a single cable, no soldering required. Right beside it, the **SWD port** gives you full hardware debugging for when you want to dig deep.

Our **STEM kit** plugs straight into the Qw/ST port and turns your badge into a pocket science lab. It pairs a **sensor stick** — light and proximity, temperature, humidity, pressure, plus a motion-sensing accelerometer and gyroscope — with a **gamepad** add-on of directional, action, and system buttons and four indicator LEDs, so you can measure the world around you or build your own handheld games.

# Backlights

<figure class="feature-callout">
<div class="callout-media">
<tufty-model backlight float shadow camera-target="0m 0.004m 0m" camera="190deg 80deg 90%"></tufty-model>
</div>
<figcaption>Four bright white LEDs glow through the back of the case.</figcaption>
</figure>

Four bright white LEDs around the back of the board glow through the translucent case — status lights, notifications, or ambient effects. Drive each zone independently and animate them however you like.

# Other features

We've covered the headlines — the display, buttons, ports, and wireless. Here's the rest of what's packed into that slim case, from the processor to the little details that make everyday use nicer:

- **Processor** — a Raspberry Pi **RP2350B**: a dual-core Arm Cortex-M33 running at 250MHz with 520KB of SRAM — plenty of grunt for smooth animation.
- **Flash** — 16MB of QSPI flash with execute-in-place (XiP), leaving lots of room for your code and assets.
- **PSRAM** — 8MB of it, so you can code freely without having to sweat every byte.
- **Light sensor** — a phototransistor (Tufty only) that automatically adjusts the screen backlight to suit your surroundings.
- **Real-time clock** — a PCF85063A that keeps accurate time even in deep sleep, so alarms and schedules survive between wake-ups.
- **Case** — a clear polycarbonate shell with a badge-specific colourway on the back to keep everything protected.
- **MicroPython** — programmed in MicroPython; no compilers or toolchains to install.
- **Ready to run** — arrives fully assembled with a matching two-clip lanyard, no soldering required.
- **Dimensions** — 84 × 76 × 20mm with the case on.

# That's your badge

And that's Badgeware — your choice of display served with a handful of buttons, wireless, expansion ports, and a genuinely capable computer, all in a case that's ready to wear or stand on your desk. It's rugged, it's hackable, and every part of it is yours to play with. Now you know your way around the hardware, let's write some code and bring it to life.

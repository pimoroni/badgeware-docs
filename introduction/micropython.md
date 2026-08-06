---
title: What is MicroPython?
summary: The badge runs MicroPython, not desktop Python — here's what that means, and the handful of differences worth knowing.
icon: memory
publish: true
sort: 4
---

# What is MicroPython?

Your badge doesn't run the same Python that's on your laptop. It runs **MicroPython** — a lean reimplementation of Python 3, built to fit and run on tiny microcontrollers. It's already installed on the badge; it's what has been running every example so far.

The good news is that it's *genuinely* Python. The syntax, control flow, functions, classes, list comprehensions, f-strings, exceptions — all there, all familiar. If you know Python, you already know MicroPython.

# Key differences

Because MicroPython is running on a small, self-contained microcontroller rather than a laptop, there are a handful of differences worth knowing before they catch you out.

### Fewer packages

The everyday modules (`time`, `math`, `random`, `json`) are built right in, but plenty of packages you might be used to aren't even available — heavyweight things like video processing or advanced maths just don't fit on a microcontroller. MicroPython has its own package manager, [mip](https://docs.micropython.org/en/latest/reference/packages.html), for grabbing extra libraries, though for badge apps you'll mostly lean on Badgeware's APIs.

### Memory is finite

The badge gives MicroPython an **8MB heap** — great for a microcontroller, and plenty for most apps. But there's no swap to fall back on, so you have to stay within it: large chunks of data or a slow leak will eventually trip a `MemoryError`.

### Lower precision numbers

Whole numbers are arbitrary-precision, just like Python. Floats, however, are usually **single-precision** rather than 64-bit, so expect a touch less decimal accuracy — fine for drawing and everyday maths. Speed isn't a concern, mind: the RP2350 crunches floats in hardware, and MicroPython's own overhead far outweighs any time spent waiting on the maths.

### Timing & hardware

MicroPython also *adds* things desktop Python has no need for: timing helpers like `time.sleep_ms()` and `time.ticks_ms()`, and — via the `machine` module — direct access to the hardware itself: GPIO pins, I²C, SPI, ADC, PWM and more. Badgeware wraps most of what you'll want, but it's all there when you fancy going lower level.

### No operating system

MicroPython more or less *is* the system, so full `threading` and `multiprocessing` aren't really a thing. You don't need them on the badge — the draw-and-`update()` loop is how you stay responsive.

These are the differences you're most likely to run into. If you want the exhaustive detail — down to the finer language-level quirks — MicroPython keeps a thorough [differences from CPython](https://docs.micropython.org/en/latest/genrst/index.html) reference.

# Performance

Interpreted Python on a microcontroller is much slower than on your desktop. For static or lightly interactive apps that's rarely a problem — but anything animation-heavy, games in particular, can push the badge hard. 

Hitting a smooth frame rate often takes real care, but a few techniques go a long way when you've a need for speed:

- **Profile first.** Don't guess — time the slow parts with `time.ticks_us()` and `time.ticks_diff()` to find the real bottleneck before optimising anything.
- **Cache lookups in locals.** Local variables are faster to reach than globals or attributes, so pull frequently used functions and objects into local names before a hot loop — e.g. `text = screen.text`.
- **Allocate as little as possible.** Creating objects inside a tight loop triggers garbage collection, which causes pauses. Preallocate buffers once and reuse them, favour `array`, `bytearray` and in-place operations, and avoid building throwaway objects each frame.
- **Control when the garbage collector runs.** Left to itself it collects whenever memory runs low, showing up as a random stutter. Calling `gc.collect()` yourself at a predictable point makes any pause regular rather than a surprise — though not allocating in the first place (above) is the real win.
- **Use `const()` for fixed values.** Declaring integer constants with `const()` lets MicroPython inline them.
- **Drop to native code for the hottest paths.** The `@micropython.native` and `@micropython.viper` decorators compile a function to machine code for a big speed-up, with inline assembler available for the truly extreme.

For the full picture, with examples of each, MicroPython's [Maximising MicroPython Speed](https://docs.micropython.org/en/latest/reference/speed_python.html) guide is well worth a read.

# mpremote

Beyond an editor like Thonny, MicroPython ships an official command-line tool — [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) — for driving a connected device straight from your terminal. Install it on your computer with `pip install mpremote`, plug the badge in over USB, and you're away.

A few things it's handy for:

| Command | What it does |
|---|---|
| `mpremote` | Connect and drop into a live REPL |
| `mpremote run app.py` | Run a local script on the badge (nothing copied) |
| `mpremote ls` | List the files on the badge |
| `mpremote cp app.py :` | Copy a file onto the badge (`:` is the badge) |
| `mpremote cp -r my_app :/apps/` | Copy a whole app folder into `/apps` |
| `mpremote cp :log.txt .` | Copy a file off the badge to your computer |
| `mpremote cat main.py` | Print a file stored on the badge |
| `mpremote mount .` | Mount your current folder *as* the badge's filesystem — edit locally, run on the badge, no copying |
| `mpremote mip install <name>` | Install a library with mip |
| `mpremote reset` | Reset the badge |

`mpremote mount .` is the one really worth remembering — and you can chain commands too, e.g. `mpremote mount . run app.py`.

If you'd rather live at the command line than in an editor, it's well worth knowing.

# In short

Almost everything you know about Python carries straight across. The differences are really just about living on a small, self-contained computer: a leaner library, finite memory, and no OS to lean on. Keep those in the back of your mind and MicroPython will feel just like home. 🐍

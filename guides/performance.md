---
title: Pushing pixels
summary: When no drawing primitive gives you the effect you want — a plasma, a fire, a rippling reflection — write straight to the pixel buffer and compile the hot loop with @native or Viper, fast enough to use over small areas.
icon: bolt
sort: 1000000
publish: true
---

# Introduction

Badgeware's drawing methods — `rectangle()`, `circle()`, `blit()` and friends — are written in C and are very fast, so reach for them first. But sometimes you want an effect no primitive gives you: a plasma, a fire, a rippling reflection. That means touching pixels one at a time, and doing that from ordinary MicroPython is *slow* — the interpreter's per-operation overhead piles up when you're looping over thousands of pixels every frame.

The fix is to compile that hot loop to native machine code. MicroPython gives you two decorators for it: **`@micropython.native`**, a drop-in speed-up that needs no code changes, and **`@micropython.viper`**, which trades Python's safety for raw, typed pointers and the most performance. A per-pixel loop that crawls in plain Python can run in real time under Viper. This guide builds up to a rippling water reflection and shows how to keep it usable by working over **small areas**.

# The pixel buffer

Every `image` (including `screen`) is a flat block of memory: `width × height` pixels, **4 bytes each** — red, green, blue, alpha — stored one row after another. You get at that memory directly with `memoryview()`:

```python-raw
fx = image(48, 48)      # a small off-screen image
buf = memoryview(fx)    # its raw pixel buffer
```

Treated as 32-bit words (one per pixel), pixel `(x, y)` lives at index `y * width + x`, and the colour is packed little-endian as `alpha << 24 | blue << 16 | green << 8 | red`. Alpha is **premultiplied** — but for a fully opaque pixel (`alpha = 255`) the red/green/blue values are stored as-is, which is the easy case.

You *can* set pixels from Python — either `screen.put(x, y)`, or by indexing the buffer yourself. Writing one pixel's colour straight into the buffer looks harmless enough:

```python-raw
i = (y * width + x) * 4     # byte offset of the pixel
buf[i]     = r
buf[i + 1] = g
buf[i + 2] = b
buf[i + 3] = a
```

But for **every pixel** the interpreter has to work through all of this:

- fetch and decode each bytecode instruction in turn
- load each operand onto the VM stack — `y`, `width`, `x`, `buf`, `r`, `g`, `b`, `a`, and every intermediate result
- evaluate the index arithmetic (`y * width`, `+ x`, `* 4`) as separate operations, each producing a new integer *object* rather than a value in a register
- recompute `i + 1`, `i + 2`, `i + 3` for the other three channels
- for each of the four stores: range-check the index against the buffer length, then dispatch the assignment through the buffer's subscript machinery
- run the loop bookkeeping — increment the `x`/`y` counters and re-test the loop conditions — as yet more bytecode

Multiply all of that by four channels and by 19,200 pixels and you're doing well over half a million object operations and dispatches *every frame*. The pixel maths is trivial; it's the interpreter overhead wrapped around it that sinks you. Compiling the loop to native code strips that overhead away — starting with the gentlest option.

# The easy win: @native

`@micropython.native` is the low-effort win: **typically around 2× faster for no code changes at all**. It compiles a function to native machine code but keeps normal Python semantics — no type annotations, no pointer types — so you just add the decorator and your existing code runs unchanged:

```python-raw
@micropython.native
def fill(buf, width, height, r, g, b, a):
    for y in range(height):
        for x in range(width):
            i = (y * width + x) * 4
            buf[i]     = r
            buf[i + 1] = g
            buf[i + 2] = b
            buf[i + 3] = a
```

That speed-up comes from removing the interpreter's biggest cost — the fetch-decode-dispatch it runs for every bytecode. What it *doesn't* remove is the object model: the index arithmetic and the four stores still go through MicroPython's runtime, with the usual type and bounds checks. Shedding those is what gives Viper its edge.

# The fast lane: @viper

Viper goes further — **tens of times faster for the right code, close to hand-written C**. It lets a function's arguments be typed as raw pointers — `ptr32` (32-bit words), `ptr16`, or `ptr8` (bytes) — that you index like an array, with no bounds checks and no object overhead. Here's a function that fills a buffer with a horizontal gradient:

```python-raw
@micropython.viper
def gradient(buf: ptr32, w: int, h: int):
    i = 0
    for y in range(h):
        for x in range(w):
            v = (x * 255) // w      # 0 -> 255 across the width
            buf[i] = int(0xff000000) | int(v << 16) | int(v << 8) | int(v)
            i += 1
```

Each pixel is a single 32-bit store, and nothing inside the loop allocates a Python object — that's where the speed comes from. You only keep that performance while the loop stays pure integers and pointers, though: call back into Python or allocate an object inside your Viper function and you slide back toward native speeds.

Note the `int(...)` casts. Viper is strict about types, and the literal `0xff000000` is too big to be a Viper machine word, so it counts as a Python *object*. Wrapping each piece in `int()` keeps the whole expression a machine integer; leave it out and you'll hit `ViperTypeError: can't store 'object'`.

## Notes

- **The Viper examples only run on real hardware.** The browser simulator doesn't support `@micropython.viper`, so flash these to a badge to try them out. (`@micropython.native` *does* run in the simulator.)
- Viper's world is machine integers and pointers — no floating point in registers, no rich Python types inside the function. Do your float and object work outside and pass in plain `int`s (and lookup tables), as we did with the wave.
- Writing through a raw pointer skips every safety check. Keep your index within `width × height` words — writing past the end corrupts memory.

# Rippling water effect

Let's put it together: draw the skull, then a **reflection underneath that wobbles like water** — the skull read bottom-up, each row nudged sideways by a scrolling sine wave. Viper can't call `math.sin`, so we bake one cycle of the wave into a small **lookup table** up front and read offsets from it in the loop:

```python-raw
import math

# Load the skull sprite (32 x 24) and make a second image the same size to
# render its rippling reflection into, fresh each frame.
skull = image.load("/system/assets/skull.png")
refl = image(skull.width, skull.height)

# Precompute the horizontal wave. Viper has no math.sin, so we bake one cycle
# into a lookup table the loop can just index. The values end up in the range
# 0 to 6.
wave = bytearray([int(math.sin(i * 0.8) * 3) + 3 for i in range(256)])

# Build one frame of the reflection: copy the skull into `dst` upside-down,
# sliding each row sideways by its wave offset and dimming every pixel so it
# reads as water. `t` advances the wave over time.
@micropython.viper
def ripple(src: ptr32, dst: ptr32, w: int, h: int, t: int):
    # reach the global wave table as a raw byte pointer
    wv = ptr8(wave)
    for ry in range(h):
        # source row, read from the bottom up so the copy is mirrored
        sy = h - 1 - ry
        # this row's sideways shift, recentred to the range -3 to 3
        off = int(wv[(ry + t) & 0xff]) - 3
        for x in range(w):
            # clamp the shifted read back inside the image edges
            sx = x - off
            if sx < 0: sx = 0
            elif sx >= w: sx = w - 1
            # copy the pixel, halving every channel to fade + darken it
            p = int(src[sy * w + sx])
            dst[ry * w + x] = (p >> 1) & int(0x7f7f7f7f)

# centre the skull horizontally; it's drawn at 2x
x = (screen.width - skull.width * 2) // 2
y = 12

while True:
    # rebuild the reflection for this frame; `badge.ticks >> 6` scrolls the wave.
    # the images pass straight into the ptr32 params via the buffer protocol.
    ripple(skull, refl, skull.width, skull.height, badge.ticks >> 6)

    # draw the skull at 2x, then its reflection just below at 1.4x tall (2x
    # squashed to ~70%) — blit scales each buffer to fill its rect.
    screen.blit(skull, rect(x, y, skull.width * 2, skull.height * 2))
    screen.blit(refl, rect(x, y + skull.height * 2, skull.width * 2, int(skull.height * 1.4)))

    badge.update()
```

Because `off` is read from `(ry + t)`, each row is displaced by a different amount. The `t` we pass in comes straight from `badge.ticks`, so the ripple advances in real time — dividing the clock down (here `>> 6`) sets how fast it scrolls, independent of frame rate. Each copied pixel is then halved with `(p >> 1) & 0x7f7f7f7f`; because alpha is premultiplied, that scales red, green, blue *and* alpha together, giving a translucent, dimmer reflection that reads like water over the dark background.

This is the whole point of keeping the work small: the reflection buffer is only 32 × 24 (768 pixels), so rebuilding it from scratch every frame is cheap, and the C `blit()` then scales it up to fill the screen for free. Reach for a bigger buffer only where you actually need the detail.

# Fire

A heat-diffusion fire (the approach from Pimoroni's Galactic Unicorn demo, adapted here). Keep a heat buffer, drop a few random hot embers along the bottom two rows each frame, then relax every cell toward the **average** of itself and the four cells below-ish it — damped by just under 1 so the flames cool as they climb. The averaging is what makes it billow softly, and the random embers keep it dancing. The one thing that needs retuning from the original is that damping: our buffer is far taller than the 11-pixel display it came from, so it has to sit much closer to 1. The buffer is also a few rows *taller than the screen*, with the embers seeded down in that hidden strip — so by the time the flames rise into view they've settled from raw bright dots into soft tongues. The colour ramp is stepped through our baked-in palette (black → grape → red → orange → yellow → white); each `color`'s `.p` is already a packed RGBA word, so it drops straight into the buffer.

```python-raw
import random
from array import array

FW, FH = 80, 60               # visible area; blit scales it up 2x to the screen
PAD = 6                       # extra rows below the screen, where embers seed
BH = FH + PAD                 # full buffer height
fire = image(FW, BH)          # RGBA frame, a little taller than we show
heat = bytearray(FW * BH)     # one heat byte (0..255) per cell
top = fire.window(0, 0, FW, FH)   # the on-screen slice of the buffer

# heat -> colour, stepped through our baked-in palette (.p is buffer-format)
def _fire(v):
    if v < 38:  return color.black
    if v < 70:  return color.grape
    if v < 100: return color.red
    if v < 140: return color.orange
    if v < 190: return color.yellow
    return color.white
palette = array('I', [_fire(v).p for v in range(256)])

# relax each cell toward the average of itself and the four cells below-ish it,
# then damp by ~0.99 so the fire cools as it rises. The averaging is what makes
# it billow softly rather than flicker.
@micropython.viper
def update(w: int, h: int):
    ht = ptr8(heat)
    for y in range(h - 2):
        for x in range(1, w - 1):
            c = y * w + x
            b = c + w
            avg = (int(ht[c]) + int(ht[b]) + int(ht[b + w]) + int(ht[b - 1]) + int(ht[b + 1])) // 5
            ht[c] = (avg * 254) >> 8       # damp ~0.992 (nudge toward 256 for taller flames)

# map each cell's heat through the palette into the frame buffer
@micropython.viper
def shade(n: int):
    ht = ptr8(heat)
    dst = ptr32(fire)
    pal = ptr32(palette)
    for i in range(n):
        dst[i] = pal[int(ht[i])]

while True:
    # clear the bottom two rows, then drop random embers onto them — these sit
    # below the visible area, so the raw seed is hidden until it rises
    last = (BH - 1) * FW
    for x in range(FW):
        heat[last + x] = 0
        heat[last - FW + x] = 0
    for _ in range(12):
        x = random.randint(2, FW - 3)
        for dx in (-1, 0, 1):
            heat[last + x + dx] = 255
            heat[last - FW + x + dx] = 255

    update(FW, BH)
    shade(FW * BH)
    screen.blit(top, rect(0, 0, screen.width, screen.height))
    badge.update()
```

# Metaballs

A handful of soft blobs drifting on sine paths. For each pixel we sum an inverse-square falloff from every blob centre — where two blobs come close their fields add up and merge into one — and the total indexes a palette.

```python-raw
import math, time
from array import array

FW, FH = 160, 120               # half of the 160x120 screen; blit scales it up 2x
blobs = image(FW, FH)

# field strength -> colour: dark -> cyan -> white
def _rgba(r, g, b): return 0xff000000 | (b << 16) | (g << 8) | r
def _blob(i):
    if i < 128: return (0, i * 2, i * 2)
    return ((i - 128) * 2, 255, 255)
palette = array('I', [_rgba(*_blob(i)) for i in range(256)])

NB = 3
bx = array('i', [0] * NB)          # blob centres, refreshed each frame
by = array('i', [0] * NB)

# for every pixel, sum an inverse-square falloff from each blob; the field piles
# up where blobs overlap, and the clamped total picks a palette colour
@micropython.viper
def render(w: int, h: int, nb: int):
    dst = ptr32(screen)
    pal = ptr32(palette)
    X = ptr32(bx)
    Y = ptr32(by)
    i = 0

    for y in range(h):
        for x in range(w):
            s = 0
            for b in range(nb):
                dx = x - int(X[b])
                dy = y - int(Y[b])
                s += 8000 // ((dx * dx + dy * dy + 8) >> 3)   # +1 avoids /0 at the centre
            if s > 255: s = 255
            dst[i] = pal[s]
            i += 1

while True:
    # drift the blobs around on sine/cosine paths
    t = badge.ticks
    for b in range(NB):
        bx[b] = int(FW * 0.5 + math.sin(t * 0.0011 + b * 1.3) * FW * 0.38)
        by[b] = int(FH * 0.5 + math.cos(t * 0.0017 + b * 2.1) * FH * 0.38)

    start = time.ticks_ms()
    render(FW, FH, NB)
    end = time.ticks_ms()
    print(f"{end - start}ms")

    badge.update()
```

# Rotozoomer

Sample a texture through a spinning, zooming transform. Viper has no floating point, so we work out the rotation as fixed-point `cos`/`sin` outside it — and the inner loop is then just two multiply-adds and a wrapped texture lookup per pixel.

```python-raw
import math
from array import array

TS = 64                        # texture is 64 x 64 — a power of two, so the
                               # sample coordinates wrap with a cheap `& 63`
tex = image(TS, TS)
FW, FH = 80, 60               # half of the 160x120 screen; blit scales it up 2x
view = image(FW, FH)

# fill the texture once with a colourful XOR pattern
@micropython.viper
def make_texture(size: int):
    t = ptr32(tex)
    for y in range(size):
        for x in range(size):
            c = (x ^ y) & 0xff
            t[y * size + x] = int(0xff000000) | int(c << 16) | int((c ^ 0x55) << 8) | int(c)
make_texture(TS)

# cosf/sinf are cos/sin pre-scaled by the zoom and by 256, so the per-pixel
# maths stays integer; the `>> 8` undoes that 256, and `& 63` wraps the texture
@micropython.viper
def roto(w: int, h: int, cosf: int, sinf: int, ox: int, oy: int):
    dst = ptr32(view)
    t = ptr32(tex)
    i = 0
    for y in range(h):
        for x in range(w):
            u = ((x * cosf - y * sinf) >> 8) + ox
            v = ((x * sinf + y * cosf) >> 8) + oy
            dst[i] = t[(v & 63) * 64 + (u & 63)]
            i += 1

while True:
    # spin steadily, and pulse the zoom in and out
    a = badge.ticks * 0.002
    zoom = 1.5 + math.sin(badge.ticks * 0.0009) * 1.2
    cosf = int(math.cos(a) * zoom * 256)
    sinf = int(math.sin(a) * zoom * 256)
    ox = (badge.ticks >> 4) & 63                # scroll the texture sideways too

    roto(FW, FH, cosf, sinf, ox, 0)
    screen.blit(view, rect(0, 0, screen.width, screen.height))
    badge.update()
```

For the underlying `raw` buffer and blit details, see the [`image` API](api/image.md).

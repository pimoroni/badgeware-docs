# Introduction

The three different models of Badgeware may have different displays, but behind the scenes they are running very similar hardware. Almost all of the API described in this guide can be used on any of the three models - but of course, you'll have to consider the particular characteristics of the display.

# Resolution

The three models have different screen resolutions. Badger has a 264×176 screen, Tufty 160×120 (or 320×240 in high-resolution mode), and Blinky a 39×26 LED matrix.

You can draw to the screen in exactly the same way on all three, but anything drawn outside the physical screen area will simply not appear.

For example, if you run a program written for Tufty’s resolution on Blinky, you will only see the top-left portion — the first 39×26 pixels.

Blinky also has cutouts in its display for the case corners and buttons. You don’t need to account for these in your code: anything drawn into those pixels is automatically ignored.

# Colour

Another difference between the badges is colour. While Tufty is full RGB, Badger can display black, white and two greys and Blinky can display 255 different levels of brightness, making it essentially a 255 level greyscale screen.

Again, for the most part you don't need to worry about this. You can work with colour images and they will automatically be converted to greyscale for Blinky or quantized for Badger - however, if you want fine control over grey levels you may want to work in greyscale behind the scenes anyway.

You can also dither your image on any of the badges, although it is by far the most useful on Badger. This will give the appearance of more levels of grey, at the cost of a repeating pattern across your image. See the [image](/api/image.md) documentation for an example of this.

# Refresh rate

Tufty and Blinky wil continuously run `update()` as quickly as they can, so the screen will redraw in as much time as it takes to process the contents of your `update()` method. You can of course build in delays or timers in `update()` to get a constant frame rate if you need one.

Badger is a little different. Because Badger is an e-paper display, it only uses power when it is updating, meaning it's perfect for very low power operations. To take advantage of this, we've designed Badger to go to sleep between every update, waking up either on a signal from the RTC or when a button is pressed.

When Badger wakes up from sleep, although it remembers which program was running it basically restarts that program from the beginning. So `init()` runs every time, and anything you haven't saved in a save state will be forgotten.

So your `update()` should look something like this:

- Load in any data you saved last update.
- Get any input such as buttons or RTC alarms.
- Do whatever work your app needs to do this update, including drawing to the screen whatever you want it to display until it's next updated.
- Save any data you need available next update.

# Additional modes

## mode()
Select additional display modes which change how rendering and screen updates behave.

### Parameters
One or more flags (see below), which can be combined as required.

- `mode(flags)`
  - `flags` - One or more mode flags, see below

### Example

```
# enable high resolution mode on Tufty and dither the framebuffer
mode(HIRES | DITHER)
```

### Tufty

- `HIRES` - sets display resolution to **320 x 240**
- `LORES` - sets display resolution to **160 x 120** (retro chic!)

If you’re aiming for smooth animations and lots of sprite manipulation, **LORES** can be a good choice. With only a quarter as many pixels to draw each frame, you can achieve much higher frame rates.

Alternatively, if you want a crisp and clear user interface, **HIRES** may be the way to go. Combined with antialiasing support, you can create very sharp graphics and clean vector shapes.

### Badger

- `FAST_UPDATE` - fastest display refresh timings, but can lead to ghosting from the previous image
- `MEDIUM_UPDATE` - more balanced timings, a good default for most uses
- `FULL_UPDATE` - slowest refresh, but produces the cleanest output

You can mix and match update rates throughout your application. For example, you might use fast updates for a responsive menu, then switch back to full updates when displaying an image.

Update speed also affects the appearance of different grey levels, so it’s worth experimenting to see what works best.

- `DITHER` - automatically dithers the screen output, as if `screen.dither()` were called at the end of each update

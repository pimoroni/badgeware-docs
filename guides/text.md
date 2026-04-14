---
title: Text
summary: Easily position and style text anywhere on the screen, great for menus, labels, and on-screen messages.
icon: text_fields
---

# Introduction

The text drawing functions provide a way to render text across all drawing surfaces in Badgeware. It ensures consistent behavior whether you’re displaying on the main screen, working with images, or composing scenes off-screen, allowing flexible and efficient text rendering throughout your application.

# Loading fonts

Before you can write to the screen you must load a font. Loading a font is a relatively expensive operation so you probably want to preload any fonts you plan to use at the start of your program, you can then swap between them by assigning the `font` property of your `screen`.

```python
nope_font = rom_font.nope
compass_font = rom_font.compass

def update():
  screen.pen = color.navy
  screen.clear()

  screen.pen = color.white

  screen.font = nope_font
  screen.text("this is nope", 10, 10)

  screen.font = compass_font
  screen.text("this is compass", 10, 30)

run(update)
```

> Badgeware ships with a gorgeous set of thirty licensed bitmap fonts designed by https://somepx.itch.io - you are free to use them in your projects!

# Brushes and color

Drawing text uses the currently selected brush. This lets you colour text and also implement effects like drop shadows.

```python
badge.default_clear = color.rgb(192, 192, 192)

def shadow_text(message, x, y):
  # draw the shadow offset by 1 pixel
  screen.pen = color.rgb(0, 0, 0, 64)
  screen.text(message, x + 1, y + 1)

  # draw the text
  screen.pen = color.rgb(128, 0, 0)
  screen.text(message, x, y)

def update():
  shadow_text("Hello, Badgeware!", 10, 10)

run(update)
```

Many effects can be achieved including bolding text, shadows, outlines, and even gradients.

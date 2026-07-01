---
title: font
summary: Functions for loading vector fonts, which can then be used to render text onto images.
icon: text_fields
publish: true
---
# Introduction

This class provides functions for loading vector fonts, which can then be used to render text onto images at any size using the methods in the `text` and `image` modules.

Text is drawn using the currently selected brush, allowing for alpha blending and other visual effects.

# Loading vector fonts
## load()
Font files can be loaded into variables. This is accomplished with `font.load(path)`, where `path` is the full path of the font file. It returns a `font` object you can assign to `screen.font`.

Once a vector font is selected, remember that vector text needs a `size` — pass it to `screen.text(message, x, y, size)` (see [image.text()](/api/image.md#text)).

### Example
```python
screen.font = font.load("/system/assets/fonts/DynaPuff-Medium.af")

while True:
  screen.pen = color.yellow
  # vector fonts scale to any size
  screen.text("Badgeware!", 10, 20, 18)
  screen.text("Badgeware!", 10, 55, 28)

  badge.update()
```

> Tip: `load_font()` is a handy global helper that searches the usual font folders for you and returns either a vector or pixel font depending on the file — see the [text guide](/guides/text.md) for details.

# Finding vector fonts
Vector fonts are stored in the Alright Font (.af) format. This converts the complex structure of .ttf and .otf fonts into simpler glyphs that can be stored in less space. Three .af fonts are preloaded at `/system/assets/fonts` — `DynaPuff-Medium.af`, `IndieFlower-Regular.af` and `MonaSans-Medium.af` — but you can find more, and make your own, at [the Alright Fonts GitHub repository](https://github.com/lowfatcode/alright-fonts).

# Reference

## Static Methods
```python-raw
font.load(path: string) -> font
```
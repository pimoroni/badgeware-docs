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
Loads a vector font from the specified file path and returns it for use when rendering text.

### Usage
```python-raw
font.load(path)
```

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | Full path of the font file to load |

### Returns
A `vector_font` object.

# Finding vector fonts
Vector fonts are stored in the Alright Font (.af) format. This converts the complex structure of .ttf and .otf fonts into simpler glyphs that can be stored in less space. There are three .af fonts preloaded on the badge, but you can find more, and make your own, at [the Alright Fonts GitHub repository](https://github.com/lowfatcode/alright-fonts).
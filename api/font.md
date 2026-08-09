---
title: font
summary: The entry point for fonts — load scalable vector fonts or bitmap pixel fonts with font.load(), and reach the built-in ROM fonts by name with font.<name>.
icon: text_fields
publish: true
---
# Introduction

`font` is the entry point for all fonts on Badgeware. Fonts come in two kinds:

- **Vector fonts** — scalable outlines stored in the Alright Font (`.af`) format. They can be drawn at any point size. Three are preloaded, and you can load your own.
- **Pixel fonts** — crisp bitmap fonts in the Pixel Perfect Font (`.ppf`) format, rendered at integer sizes. Badgeware ships with over thirty of these as *ROM fonts*, always available by name.

Whichever kind you use, the workflow is the same: get hold of a font (load it, or pick a ROM font), assign it with `screen.font = ...`, then draw with [`image.text()`](/api/image.md#text). Text is drawn using the currently selected brush, allowing for alpha blending and other visual effects.

The two kinds differ in how the `size` argument behaves when you draw. A vector font takes a **point size** — any value you like, defaulting to `12`. A pixel font takes an **integer scale**: `1` (the default) is native size, `2` doubles every glyph pixel, `3` triples it. Leave `size` off, or pass `0`, to get the font's own size. Always measure and draw with the same `size`, so your layout matches what's rendered.

# ROM fonts
Badgeware includes over thirty high-quality, licensed pixel fonts, always available without loading anything. Reach them as attributes of `font`, using the font's name:

```python
def update():
  screen.font = font.compass
  screen.pen = color.red
  screen.text("Arr Cap'n!", 10, 10)

  screen.font = font.nope
  screen.pen = color.lime
  screen.text("Arr Cap'n!", 10, 30)

run(update)
```

For the complete set, with a sample of each, see the [font gallery](#font-gallery) below.

# Loading fonts
## load()
Loads a font from a file and returns it, ready to assign to `screen.font`. It's the single loader for both kinds of font: it detects the file type automatically — a `.af` file gives a vector font, a `.ppf` file gives a pixel font. You can pass a full path, or just a font's name to have it found in the system font folders.

### Usage
`font.load(path)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | A full path to a font file, or the bare name of a font to find in the system font folders |

### Returns
A `font` — whichever kind matches the file. Raises `OSError` if no matching font is found.

```python
# a scalable vector font, loaded by path...
handwriting = font.load("/system/assets/fonts/IndieFlower-Regular.af")

# ...and an extra pixel font that isn't baked into ROM, found by name
extra = font.load("unfair")

def update():
  screen.pen = color.white

  screen.font = handwriting
  screen.text("Hello!", 10, 10, 32)   # vector font: 32pt

  screen.font = extra
  screen.text("Hello!", 10, 70)       # pixel font: native size

run(update)
```

# Vector fonts
Vector fonts are stored in the Alright Font (`.af`) format. This converts the complex structure of `.ttf` and `.otf` fonts into simpler glyphs that can be stored in much less space, and — because they're outlines rather than fixed bitmaps — can be drawn at any size. Three `.af` fonts are preloaded in `/system/assets/fonts/`, and you can find more, or make your own, at [the Alright Fonts GitHub repository](https://github.com/lowfatcode/alright-fonts).

Because vector fonts are scalable, pass a point `size` when you draw (see [`image.text()`](/api/image.md#text)); the default is `12`.

# Pixel fonts
Pixel fonts are bitmap fonts in the Pixel Perfect Font (`.ppf`) format. They render at integer sizes only, so the `size` you draw with acts as a whole-number scale (`1` native, `2` double, and so on). Layout (advance, spacing and reported height) scales to match, so [`measure_text()`](/api/image.md#measure_text) with the same scale gives the box you'll actually draw. The ROM fonts are all pixel fonts.

A loaded pixel font also exposes a couple of read-only properties:

| Property | Type | Description |
|---|---|---|
| `height` | `int` | Height in pixels of the font's glyph bounding box (read-only) |
| `name` | `string` | The name of the font (read-only) |

# Font gallery
Text wouldn’t be nearly as engaging without a great selection of fonts. When we came across [Ivano's](https://somepx.itch.io) extensive collection of pixel fonts, we knew they were a perfect match for Badgeware.

Included are a wide range of styles covering everything from clean, readable text to bold display typefaces inspired by classic arcade and sci-fi aesthetics.

These samples should give you a good idea of the style of each ROM font:

|Name|Size|Sample|Description|
|-|-|-|-|
|ark|6px|![ark](/fonts/ark.png)|tiny, smallcaps|
|desert|6px|![desert](/fonts/desert.png)|tiny, drowsy, sunny|
|torch|6px|![torch](/fonts/torch.png)|fiery, pocket-sized, fantasy|
|sins|7px|![sins](/fonts/sins.png)|tiny, classic, stylish|
|teatime|7px|![teatime](/fonts/teatime.png)|classic, readable, monospace|
|hungry|7px|![hungry](/fonts/hungry.png)|playful, unique, monospace|
|kobold|7px|![kobold](/fonts/kobold.png)|classic, tiny, fantasy|
|lookout|7px|![lookout](/fonts/lookout.png)|adventurous, fantasy|
|loser|7px|![loser](/fonts/loser.png)|slanted, smallcaps, monospace|
|winds|7px|![winds](/fonts/winds.png)|tiny, extra-spaced|
|match|7px|![match](/fonts/match.png)|classic, joyful|
|corset|8px|![corset](/fonts/corset.png)|elegant, cozy|
|nope|8px|![nope](/fonts/nope.png)|clear, readable|
|unfair|8px|![unfair](/fonts/unfair.png)|wide, retro, eccentric|
|saga|8px|![saga](/fonts/saga.png)|medieval, fantasy, legendary|
|memo|9px|![memo](/fonts/memo.png)|wacky, distinctive|
|outflank|9px|![outflank](/fonts/outflank.png)|fantasy, arcane|
|salty|9px|![salty](/fonts/salty.png)|thick, all-purpose|
|smart|9px|![smart](/fonts/smart.png)|classic, chunky, smallcaps|
|awesome|9px|![awesome](/fonts/awesome.png)|cheerful, wholesome|
|compass|9px|![compass](/fonts/compass.png)|classic, fantasy|
|yolk|9px|![yolk](/fonts/yolk.png)|classic, fantasy|
|vest|9px|![vest](/fonts/vest.png)|elegant, classic, serif|
|holotype|9px|![holotype](/fonts/holotype.png)|distinctive, premium|
|yesterday|10px|![yesterday](/fonts/yesterday.png)|bold, readable, distinctive|
|absolute|10px|![absolute](/fonts/absolute.png)|bold, boxy|
|fear|11px|![fear](/fonts/fear.png)|smallcaps, horror|
|troll|12px|![troll](/fonts/troll.png)|fantasy, ornate|
|bacteria|12px|![bacteria](/fonts/bacteria.png)|rational, wide, monospace|
|curse|12px|![curse](/fonts/curse.png)|comic, horror, smallcaps|
|ziplock|13px|![ziplock](/fonts/ziplock.png)|round, cheerful, comic|
|futile|14px|![futile](/fonts/futile.png)|big, bold, unique|
|manticore|14px|![manticore](/fonts/manticore.png)|strong, metal, horror|
|more|15px|![more](/fonts/more.png)|chunky, huge, comic|
|ignore|17px|![ignore](/fonts/ignore.png)|colossal, intrepid|

---
title: pixel_font
summary: Functions for loading pixel fonts, which can then be used to render text onto images.
icon: text_fields
publish: true
---
# Introduction

This class provides functions for loading pixel fonts, which can then be used to render text onto images.

Text is drawn using the currently selected brush, allowing for alpha blending and other visual effects.

Badgeware includes over thirty high-quality, licensed pixel fonts created by [somepx](https://somepx.itch.io), giving you plenty of options to add style and character to your applications.

# Properties

## height
The height, in pixels, of the font's glyph bounding box.

## name
The name of the pixel font.

# Font gallery

Text wouldn’t be nearly as engaging without a great selection of fonts. When we came across [Ivano's](https://somepx.itch.io) extensive collection of pixel fonts, we knew they were a perfect match for Badgeware.

Included are a wide range of styles covering everything from clean, readable text to bold display typefaces inspired by classic arcade and sci-fi aesthetics.

Our pixel font file format is called Pixel Perfect Font (`.ppf`) and all of the fonts are pre-loaded onto your badge and accessible via `rom_font`.

```python
def update():
  screen.font = rom_font.compass
  screen.pen = color.red
  screen.text("Arr Cap'n!", 10, 10)

  screen.font = rom_font.nope
  screen.pen = color.lime
  screen.text("Arr Cap'n!", 10, 30)

  screen.font = rom_font.unfair
  screen.pen = color.blue
  screen.text("Arr Cap'n!", 10, 50)
```

These samples should give you a good idea of the style of each font:

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

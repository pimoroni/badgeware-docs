---
title: spritesheet
summary: Provides functions for blitting sprites to the screen.
icon: image
publish: true
---
# Introduction
The `spritesheet` is a helper for managing sheets of individual sprites, be they a deck of cards, character animations or the frames of an animated gif.

![A grid of sprite cells, with column numbers along the top and row numbers down the side, showing the cell at column 3 row 1 pulled out with sprite(3, 1)](/guides/assets/sprite-grid.svg)

## sprite()
Returns a single sprite from the image's grid as an  `image` which is a view onto the sheet. The grid is set by [`spritesheet()`](#spritesheet); a normal image with no grid behaves as a 1 × 1 sheet, so `sprite(0, 0)` is the whole image.

### Usage
`.sprite(x, y)`

| Parameter | Type | Description |
|---|---|---|
| `x` | `int` | The column of the sprite, counting from 0 |
| `y` | `int` | The row of the sprite, counting from 0 |

#### or

`.sprite(n)`

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` | The index of the sprite, counting from 0 |

Sprites are indexed from 0 in the direction set by `direction`. `spritesheet.COLUMNS` will traverse down each column in turn from top to bottom before moving onto the next. `spritesheet.ROWS` will run left to right over each row. Both are useful if your animation frames span subsequent rows or columns.

### Returns
An `image` viewing the requested grid cell. As it shares the sheet's pixel data, it's cheap to create — you can call `sprite()` every frame without copying any image data.

```python
# an 8x4 spritesheet of 16x16 tiles
tiles = image.load("/system/assets/cards.png").spritesheet(13, 6)

def update():
  # draw the tile in column 2, row 1
  screen.blit(tiles.sprite(2, 1), vec2(10, 10))

run(update)
```

# Creating spritesheets

Turn an image into a spritesheet by calling [`spritesheet(cols, rows)`](/api/image.md#spritesheet) on it.

Once you have a spritesheet, [`sprite(x, y)`](#sprite) returns any cell as a lightweight view onto the sheet, ready to blit. Cells are addressed by column (`x`) and row (`y`), counting from `(0, 0)` in the top-left — column first, then row. Or index with `sprite(n)`.

## load()
Loads an image from the specified file path and returns it as a new `spritesheet` object.

### Usage
`image.load(path)`

| Parameter | Type | Description |
|---|---|---|
| `path` | `string` | Path to the image file to load |

```python
import time

gif = spritesheet.load("/system/assets/squirrel.gif")

while True:
  for i in range(gif.sprites):
    screen.blit(gif.sprite(i), rect(48, 28, 64, 64))
    badge.update()
    time.sleep(gif.timings[i] / 1000)
```

# Properties

The `timings` method exists only to preserve the timings read from a gif file, otherwise they would be lost!

| Property | Type | Description |
|---|---|---|
| `rows` | `int` | Number of rows in the spritesheet (read-only) |
| `cols` | `int` | Number of columns in the spritesheet (read-only) |
| `sprites` | `int` | Number of sprites in the spritesheet (read-only) |
| `timings` | `int` | A list of timings in milliseconds for each sprite (gif only) (read-only) |
| `direction` | `int` | The direction that `sprite(n)` traverses the sheet. One of `spritesheet.ROWS` or `spritesheet.COLUMNS` |

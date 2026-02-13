---
title: SpriteSheet
summary: Load and manage spritesheets and animated sprites.
icon: diamond_shine
publish: true
---

# Introduction
Sprites are an easy way or organising multiple graphical elements while keeping memory usage down. Very simply, a spritesheet is a single large image which is split into regular cells. These cells can then be used as individual images themselves while all still referring back to the single image in memory.

Cells within a spritesheet might represent different things stored together in memory for convenience, or they may represent different animation frames of a single object. Badgeware also provides a class which makes organising these animations easier.

# SpriteSheet
The `SpriteSheet` class is loaded along with a definition of how many rows and columns it contains. It's very easy to then address the individual sprites within it, without needing to add any more images into memory.

## SpriteSheet()
This is the basic constructor, returning an instance of the `SpriteSheet` class.

### Usage
- `sheet_name = SpriteSheet(image, columns, rows)`
    - `image` - The path to the image file to be loaded.
    - `columns` - How many columns of sprites there are in the sheet.
    - `rows` - How many rows of sprites there are in the sheet.

## sprite()
This function is the main way to get a sprite from the spritesheet. It returns an `image` which you can blit like any other `image`.

### Usage
- `sheet_name.sprite(column, row)`
    - `column` - The column of the spritesheet to fetch.
    - `row` - The row of the spritesheet to fetch.

### Returns
An `image` representing the selected sprite.

## animation()
This function returns an `AnimatedSprite` object, as described below. It takes in a starting cell on the `SpriteSheet`, and then makes an `AnimatedSprite` using that cell and a number of cells either to its right or below it as specified.

### Usage
- `sheet_name.animation(x, y, count, horizontal)`
    - `x, y` (Optional) - The column and row of the first frame of the animation. Default `0, 0`.
    - `count` (Optional) - How many frames to include in the animation. Default is `None`, which will include all sprites up to the edge of the spritesheet.
    - `horizontal` (Optional) - Boolean determining whether frames will be picked to the right of the starting frame (`True`), or below it (`False`). Defaults to `True`.

### Returns
An `AnimatedSprite` containing the selected frames.

# Animated sprites
A normal sprite pulled from a spritesheet is a simple `image` object. You can do with it anything you would do with any other `image`. But spritesheets are often used to hold animations - for example a game character, where the first row of sprites contains the frames of their walking animation, the second contains the frames of their attacking animation and so on. This is what the `AnimatedSprite` class is used to organise.

## AnimatedSprite()
The basic constructor of the `AnimatedSprite` class, returning an instance of `AnimatedSprite`. Note that this would probably more usually be done via `SpriteSheet.animation()`, and the parameters for creation are almost the same. This also takes a starting cell in a `SpriteSheet`, and then makes an animation sequence from a specified number of sprites to the right or below.

### Usage
- `sprite_name = AnimatedSprite(spritesheet, x, y, count, horizontal)`
    - `spritesheet` - The `SpriteSheet` object the frames should be taken from.
    - `x, y` - The column and row of the first frame of the animation.
    - `count` - How many frames to include in the animation.
    - `horizontal` (Optional) - Boolean determining whether frames will be picked to the right of the starting frame (`True`), or below it (`False`). Defaults to `True`.

### Returns
An `AnimatedSprite` containing the selected frames.

## count
This property of AnimatedSprite simply returns how many frames are in the animation.

## frame()
Returns a single frame from the animation as an `image` object, just like getting a static sprite from a spritesheet.

### Usage
- `sprite_name.frame(frame_index)`
    - `frame_index` (Optional) - the index of the frame in the animation. If this is higher than the number of frames in the animation, it loops, so a looping animation cycle can be gained just by constantly increasing `frame_index`. Defaults to 0.

### Returns
An `image` containing the selected frame.

# Reference

## Constructors
```python-raw
AnimatedSprite(spritesheet: SpriteSheet, x: int, y: int, count: int, horizontal: bool) -> AnimatedSprite
SpriteSheet(image: string, columns: int, rows: int) -> SpriteSheet
```

## Properties
```python-raw
AnimatedSprite.count: int
```

## Methods
```python-raw
AnimatedSprite.frame(index: int=0) -> image
SpriteSheet.animation(x: int=0, y: int=0, count: int|None=None, horizontal: bool=True)
SpriteSheet.sprite(x: int, y: int)
```
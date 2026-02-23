---
title: Sprites
summary: Load spritesheets and extract individual sprites and animation cycles for drawing.
icon: diamond_shine
---

# Introduction

A sprite is just a small image that represents one visual element — like a character, icon, button, or explosion frame. Think of it as a single piece of art used inside a bigger scene.

In classic 2D games, each moving character or object you saw on screen — the hero, enemies, coins, bullets — was drawn as a sprite that the game engine could move, rotate, or hide.

# Why use sprites?

On resource-constrained systems, sprites were helpful to save memory and boost performance. By packing many small images into a single spritesheet, the system only needed to load one image into memory and draw specific parts of it when needed. This reduced file I/O, minimized texture swaps, and allowed even limited hardware to display smooth animations and complex scenes efficiently.

- Fewer image requests = faster loading times
- Switch between frames on the spritesheet to make animations
- All related graphics stay together in one place
- Save memory by using sprites multiple times

![Sprite sheet example](guides/assets/spritesheet1.png)

Badgeware provides a `SpriteSheet` class that helps you load spritesheet images and access the individual sprites within it.

Each spritesheet contains a grid of images that can be referred to by their position in the spritesheet.

For example if we load a spritesheet that is 128 x 64 pixels in size, and specify that there are 8 columns and 4 rows.

| | | | | | | | |
|-|-|-|-|-|-|-|-|
|0 , 0|1 , 0|2 , 0|3 , 0|4 , 0|5 , 0|6 , 0|7 , 0|
|0 , 1|1 , 1|2 , 1|3 , 1|4 , 1|5 , 1|6 , 1|7 , 1|
|0 , 2|1 , 2|2 , 2|3 , 2|4 , 2|5 , 2|6 , 2|7 , 2|
|0 , 3|1 , 3|2 , 3|3 , 3|4 , 3|5 , 3|6 , 3|7 , 3|


# Loading sprite sheets

```python
# example of loading a sprite and blitting it to the screen
from badgeware import screen
from lib import SpriteSheet

# load spritesheet that has 8 columns and 4 rows
sprites = SpriteSheet(f"sprites/character.png", 8, 4)

def update():
  # clear the background
  screen.brush = brushes.color(20, 40, 60)
  screen.clear()

  # blit the sprite at 0, 0 in the spritesheet to the screen
  screen.blit(sprites.sprite(0, 0), 10, 10)

  # scale blit the sprite at 3, 0 in the spritesheet to the screen
  screen.scale_blit(sprites.sprite(0, 0), 50, 50, 30, 30)
```

# Drawing sprites

# Animating sprites

The `Image` class can load images from files on the filesystem which can then be blitted onto the screen. [Click here for full documentation of the `Image` class](api/image.md).

```python
# example of loading a sprite and blitting it to the screen
from badgeware import screen, brushes, Image
from lib import SpriteSheet

# load an image as a sprite sheet specifying the number of rows and columns
mona = SpriteSheet(f"assets/mona-sprites/mona-default.png", 7, 1)

def update():
  # clear the background
  screen.brush = brushes.color(20, 40, 60)
  screen.clear()

  # blit the sprite at 0, 0 in the spritesheet to the screen
  screen.blit(mona.sprite(0, 0), 10, 10)

  # scale blit the sprite at 3, 0 in the spritesheet to the screen
  screen.scale_blit(mona.sprite(0, 0), 50, 50, 30, 30)
```

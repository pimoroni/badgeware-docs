---
title: Sprites
summary: Load spritesheets and extract individual sprites and animation cycles for drawing.
icon: background_grid_small
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

Badgeware provides a `SpriteSheet` class that helps you load spritesheet images and access the individual sprites within it. `SpriteSheet` is available globally, so you don't need to import anything to use it.

Each spritesheet contains a grid of images that can be referred to by their position — a column and a row, both starting from 0.

For example if we load a spritesheet that is 128 x 64 pixels in size, and specify that there are 8 columns and 4 rows, the cells are addressed like this:

| | | | | | | | |
|-|-|-|-|-|-|-|-|
|0 , 0|1 , 0|2 , 0|3 , 0|4 , 0|5 , 0|6 , 0|7 , 0|
|0 , 1|1 , 1|2 , 1|3 , 1|4 , 1|5 , 1|6 , 1|7 , 1|
|0 , 2|1 , 2|2 , 2|3 , 2|4 , 2|5 , 2|6 , 2|7 , 2|
|0 , 3|1 , 3|2 , 3|3 , 3|4 , 3|5 , 3|6 , 3|7 , 3|

# Loading spritesheets

To load a spritesheet, create a `SpriteSheet` with the path to the image and the number of columns and rows it contains. Badgeware slices the image into a grid for you. Each cell is a plain `image`, so you draw it with `screen.blit()` just like any other image.

```python
# load a spritesheet that has 8 columns and 4 rows
sprites = SpriteSheet("/system/assets/character.png", 8, 4)

while True:
  # blit the sprite at column 0, row 0 to the screen at (10, 10)
  screen.blit(sprites.sprite(0, 0), 10, 10)

  # blit the sprite at column 1, row 0
  screen.blit(sprites.sprite(1, 0), 40, 10)

  badge.update()
```

Because each sprite is an `image`, you can scale it too — pass a destination `rect` to `blit()`:

```python
sprites = SpriteSheet("/system/assets/character.png", 8, 4)

while True:
  sprite = sprites.sprite(0, 0)

  # draw it at 1:1
  screen.blit(sprite, 10, 10)

  # and scaled up into a 48x48 box
  screen.blit(sprite, rect(70, 10, 48, 48))

  badge.update()
```

# Animating sprites

Most spritesheets hold the frames of an animation — a walk cycle, a spinning coin, an explosion. The `animation()` method bundles a run of cells into an `AnimatedSprite`, which makes it easy to step through the frames over time.

Call `animation(x, y, count)` to build an animation starting at a cell and taking `count` frames. By default the frames run **horizontally** (to the right); pass `horizontal=False` to run down a column instead.

```python
sprites = SpriteSheet("/system/assets/character.png", 8, 4)

# a 7-frame walk cycle along the top row
walk = sprites.animation(0, 0, 7)

while True:
  # advance the animation using the badge clock;
  # frame() loops automatically, so the cycle repeats forever
  frame = walk.frame(badge.ticks / 100)
  screen.blit(frame, 60, 40)

  badge.update()
```

`frame()` takes a frame index and wraps it around the number of frames, so you can just feed it an ever-increasing number (like a scaled `badge.ticks`) to get a smooth looping cycle. Divide `badge.ticks` by a larger number to slow the animation down, or a smaller number to speed it up.

You can keep several animations from the same sheet — for example a different row for each action:

```python
sprites = SpriteSheet("/system/assets/character.png", 8, 4)

walk = sprites.animation(0, 0, 7)          # row 0: walking
jump = sprites.animation(0, 1, 5)          # row 1: jumping

while True:
  # switch animation depending on a button
  current = jump if badge.held(BUTTON_A) else walk
  screen.blit(current.frame(badge.ticks / 100), 60, 40)

  badge.update()
```

See the [SpriteSheet API reference](/api/SpriteSheet.md) for the full details of `SpriteSheet` and `AnimatedSprite`.

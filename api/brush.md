---
title: brush
summary: Methods for painting images or patterns as fill when creating vector shapes.
icon: brush
publish: true
---
# Introduction
Brushes are a powerful tool when drawing vector shapes on Badgeware. Instead of a solid flat colour, they can paint an image or a repeating pattern across the shapes you draw. In fact, `color` itself is a type of brush - anywhere that you might use `color` to set a pen, you can set that pen to a `brush` instead.

# Image brushes
One use of brushes is to fill a shape with an image rather than with a flat colour. The image should be loaded in as a variable as usual, then passed into `brush.image()`. You can also pass in a transformation matrix as a `mat3` to determine the size, translation and rotation of the image. This image will tile infinitely if its size is smaller than the shape it is filling.

### Usage
```python-raw
brush.image(image, matrix)
```

| Parameter | Type | Description |
|---|---|---|
| `image` | `image` | The image to use as the brush |
| `matrix` | `mat3` | A transformation matrix representing the size, translation and rotation of the image |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

skull = image.load("/system/assets/skull.png")

def update():
  t = mat3().translate(-12, -12).rotate(badge.ticks / 100).translate(80, 60).scale(math.sin(badge.ticks / 1000) * 4)
  imgbrush = brush.image(skull, t)

  screen.pen = imgbrush
  screen.shape(shape.circle(80, 60, 50))

run(update)
```

# Pattern brushes
A pattern brush works similarly to an image brush, but instead of a picture a pattern of lit pixels is used. You can pass in the foreground and background colours of the pattern. Patterns can either be picked from the built in range in Badgeware, or you can specify a custom pattern by inputting it yourself as a tuple. These patterns remain static and are pixel scaled, so they cannot have a transformation matrix applied to them like an image brush can.

### Usage
```python-raw
brush.pattern(col1, col2, pattern)
```

| Parameter | Type | Description |
|---|---|---|
| `col1`, `col2` | `color` | The foreground and background colours of the pattern |
| `pattern` | `int` \| `tuple` | The pattern itself — either an integer selecting one of the built-in patterns, or a tuple of binary numbers representing a custom pattern |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

def update():
  custom_pattern = brush.pattern(color.rgb(255, 100, 100, 100), color.rgb(0, 0, 0, 0), (
    0b00000000,
    0b01111110,
    0b01000010,
    0b01011010,
    0b01011010,
    0b01000010,
    0b01111110,
    0b00000000))
  screen.pen = custom_pattern
  screen.shape(shape.circle(80 + math.cos(badge.ticks / 500) * 30, 60 + math.sin(badge.ticks / 1000) * 30, 30))

  built_in_pattern = brush.pattern(color.rgb(100, 255, 100, 100), color.rgb(0, 0, 0, 0), 11)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.sin(badge.ticks / 250) * 60, 60 + math.cos(badge.ticks / 500) * 60, 30))

  built_in_pattern = brush.pattern(color.rgb(100, 100, 255, 100), color.rgb(0, 0, 0, 0), 8)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.cos(badge.ticks / 250) * 60, 60 + math.sin(badge.ticks / 500) * 60, 30))

run(update)
```

> Note: The `0b` at the beginning of the numbers in the custom pattern signify that the number is binary. The 1s and 0s following it are each row of the pattern.

| | | | |
|-|-|-|-|
| **0**<br>![Pattern 0](/patterns/pattern0.png) | **1**<br>![Pattern 1](/patterns/pattern1.png) | **2**<br>![Pattern 2](/patterns/pattern2.png) | **3**<br>![Pattern 3](/patterns/pattern3.png) |
| **4**<br>![Pattern 4](/patterns/pattern4.png) | **5**<br>![Pattern 5](/patterns/pattern5.png) | **6**<br>![Pattern 6](/patterns/pattern6.png) | **7**<br>![Pattern 7](/patterns/pattern7.png) |
| **8**<br>![Pattern 8](/patterns/pattern8.png) | **9**<br>![Pattern 9](/patterns/pattern9.png) | **10**<br>![Pattern 10](/patterns/pattern10.png) | **11**<br>![Pattern 11](/patterns/pattern11.png) |
| **12**<br>![Pattern 12](/patterns/pattern12.png) | **13**<br>![Pattern 13](/patterns/pattern13.png) | **14**<br>![Pattern 14](/patterns/pattern14.png) | **15**<br>![Pattern 15](/patterns/pattern15.png) |
| **16**<br>![Pattern 16](/patterns/pattern16.png) | **17**<br>![Pattern 17](/patterns/pattern17.png) | **18**<br>![Pattern 18](/patterns/pattern18.png) | **19**<br>![Pattern 19](/patterns/pattern19.png) |
| **20**<br>![Pattern 20](/patterns/pattern20.png) | **21**<br>![Pattern 21](/patterns/pattern21.png) | **22**<br>![Pattern 22](/patterns/pattern22.png) | **23**<br>![Pattern 23](/patterns/pattern23.png) |
| **24**<br>![Pattern 24](/patterns/pattern24.png) | **25**<br>![Pattern 25](/patterns/pattern25.png) | **26**<br>![Pattern 26](/patterns/pattern26.png) | **27**<br>![Pattern 27](/patterns/pattern27.png) |
| **28**<br>![Pattern 28](/patterns/pattern28.png) | **29**<br>![Pattern 29](/patterns/pattern29.png) | **30**<br>![Pattern 30](/patterns/pattern30.png) | **31**<br>![Pattern 31](/patterns/pattern31.png) |
| **32**<br>![Pattern 32](/patterns/pattern32.png) | **33**<br>![Pattern 33](/patterns/pattern33.png) | **34**<br>![Pattern 34](/patterns/pattern34.png) | **35**<br>![Pattern 35](/patterns/pattern35.png) |
| **36**<br>![Pattern 36](/patterns/pattern36.png) | **37**<br>![Pattern 37](/patterns/pattern37.png) |  |  |

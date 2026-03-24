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
- `brush.image(image, matrix)`
    - `image` - the image to use as the brush.
    - `matrix` - a `mat3` representing the transformation of the image.

### Returns
A `brush` representing the brush, which then can be used to set an `image`'s pen.

### Example
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
- `brush.pattern(col1, col2, pattern)`
    - `col1, col2` - the foreground and background `color`s of the pattern.
    - `pattern` - the pattern itself. Note that this can be an integer representing one of the built-in patterns, or a tuple of binary numbers representing a custom pattern.

### Returns
A `brush` representing the brush, which then can be used to set an `image`'s pen.

### Example
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

|Name|Sample|Tiled|
|-|-|-|
|0|![Pattern 0](/patterns/pattern0.png)|![Pattern 0 Tiled](/patterns/pattern0_tiled.png)|
|1|![Pattern 1](/patterns/pattern1.png)|![Pattern 1 Tiled](/patterns/pattern1_tiled.png)|
|2|![Pattern 2](/patterns/pattern2.png)|![Pattern 2 Tiled](/patterns/pattern2_tiled.png)|
|3|![Pattern 3](/patterns/pattern3.png)|![Pattern 3 Tiled](/patterns/pattern3_tiled.png)|
|4|![Pattern 4](/patterns/pattern4.png)|![Pattern 4 Tiled](/patterns/pattern4_tiled.png)|
|5|![Pattern 5](/patterns/pattern5.png)|![Pattern 5 Tiled](/patterns/pattern5_tiled.png)|
|6|![Pattern 6](/patterns/pattern6.png)|![Pattern 6 Tiled](/patterns/pattern6_tiled.png)|
|7|![Pattern 7](/patterns/pattern7.png)|![Pattern 7 Tiled](/patterns/pattern7_tiled.png)|
|8|![Pattern 8](/patterns/pattern8.png)|![Pattern 8 Tiled](/patterns/pattern8_tiled.png)|
|9|![Pattern 9](/patterns/pattern9.png)|![Pattern 9 Tiled](/patterns/pattern9_tiled.png)|
|10|![Pattern 10](/patterns/pattern10.png)|![Pattern 10 Tiled](/patterns/pattern10_tiled.png)|
|11|![Pattern 11](/patterns/pattern11.png)|![Pattern 11 Tiled](/patterns/pattern11_tiled.png)|
|12|![Pattern 12](/patterns/pattern12.png)|![Pattern 12 Tiled](/patterns/pattern12_tiled.png)|
|13|![Pattern 13](/patterns/pattern13.png)|![Pattern 13 Tiled](/patterns/pattern13_tiled.png)|
|14|![Pattern 14](/patterns/pattern14.png)|![Pattern 14 Tiled](/patterns/pattern14_tiled.png)|
|15|![Pattern 15](/patterns/pattern15.png)|![Pattern 15 Tiled](/patterns/pattern15_tiled.png)|
|16|![Pattern 16](/patterns/pattern16.png)|![Pattern 16 Tiled](/patterns/pattern16_tiled.png)|
|17|![Pattern 17](/patterns/pattern17.png)|![Pattern 17 Tiled](/patterns/pattern17_tiled.png)|
|18|![Pattern 18](/patterns/pattern18.png)|![Pattern 18 Tiled](/patterns/pattern18_tiled.png)|
|19|![Pattern 19](/patterns/pattern19.png)|![Pattern 19 Tiled](/patterns/pattern19_tiled.png)|
|20|![Pattern 20](/patterns/pattern20.png)|![Pattern 20 Tiled](/patterns/pattern20_tiled.png)|
|21|![Pattern 21](/patterns/pattern21.png)|![Pattern 21 Tiled](/patterns/pattern21_tiled.png)|
|22|![Pattern 22](/patterns/pattern22.png)|![Pattern 22 Tiled](/patterns/pattern22_tiled.png)|
|23|![Pattern 23](/patterns/pattern23.png)|![Pattern 23 Tiled](/patterns/pattern23_tiled.png)|
|24|![Pattern 24](/patterns/pattern24.png)|![Pattern 24 Tiled](/patterns/pattern24_tiled.png)|
|25|![Pattern 25](/patterns/pattern25.png)|![Pattern 25 Tiled](/patterns/pattern25_tiled.png)|
|26|![Pattern 26](/patterns/pattern26.png)|![Pattern 26 Tiled](/patterns/pattern26_tiled.png)|
|27|![Pattern 27](/patterns/pattern27.png)|![Pattern 27 Tiled](/patterns/pattern27_tiled.png)|
|28|![Pattern 28](/patterns/pattern28.png)|![Pattern 28 Tiled](/patterns/pattern28_tiled.png)|
|29|![Pattern 29](/patterns/pattern29.png)|![Pattern 29 Tiled](/patterns/pattern29_tiled.png)|
|30|![Pattern 30](/patterns/pattern30.png)|![Pattern 30 Tiled](/patterns/pattern30_tiled.png)|
|31|![Pattern 31](/patterns/pattern31.png)|![Pattern 31 Tiled](/patterns/pattern31_tiled.png)|
|32|![Pattern 32](/patterns/pattern32.png)|![Pattern 32 Tiled](/patterns/pattern32_tiled.png)|
|33|![Pattern 33](/patterns/pattern33.png)|![Pattern 33 Tiled](/patterns/pattern33_tiled.png)|
|34|![Pattern 34](/patterns/pattern34.png)|![Pattern 34 Tiled](/patterns/pattern34_tiled.png)|
|35|![Pattern 35](/patterns/pattern35.png)|![Pattern 35 Tiled](/patterns/pattern35_tiled.png)|
|36|![Pattern 36](/patterns/pattern36.png)|![Pattern 36 Tiled](/patterns/pattern36_tiled.png)|
|37|![Pattern 37](/patterns/pattern37.png)|![Pattern 37 Tiled](/patterns/pattern37_tiled.png)|
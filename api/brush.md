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
`brush.image(image, matrix)`

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
`brush.pattern(col1, col2, pattern)`

| Parameter | Type | Description |
|---|---|---|
| `col1`, `col2` | `color` | The foreground and background colours of the pattern |
| `pattern` | `int` \| `tuple` | The pattern itself — either an integer selecting one of the built-in patterns, or a tuple of binary numbers representing a custom pattern |

### Returns
A `brush` which can then be used to set an `image`'s pen.

```python
import math

# a fully transparent colour, used as the patterns' background so the
# unlit pixels let whatever is behind them show through
TRANSPARENT = color.rgb(0, 0, 0, 0)

def update():
  # a custom pattern: each 0b number is one binary row, where the 1s and 0s
  # are the lit and unlit pixels of the pattern
  custom_pattern = brush.pattern(color.red, TRANSPARENT, (
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

  built_in_pattern = brush.pattern(color.lime, TRANSPARENT, 11)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.sin(badge.ticks / 250) * 60, 60 + math.cos(badge.ticks / 500) * 60, 30))

  built_in_pattern = brush.pattern(color.blue, TRANSPARENT, 8)
  screen.pen = built_in_pattern
  screen.shape(shape.circle(80 + math.cos(badge.ticks / 250) * 60, 60 + math.sin(badge.ticks / 500) * 60, 30))

run(update)
```

## Built-in patterns
The patterns built in to Badgeware, selectable by index with `brush.pattern()`.

<style>
  .pattern-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(4rem, 1fr));
    gap: 0.75rem;
    margin: 1rem 0;
  }
  .pattern-grid figure { margin: 0; text-align: center; }
  .pattern-grid img {
    width: 100%; display: block; border-radius: 0.25rem;
    image-rendering: pixelated;
  }
  .pattern-grid figcaption {
    font-size: 0.8rem; color: var(--faint); margin-top: 0.3rem;
  }
</style>

<div class="pattern-grid">
<figure><img src="/docs/patterns/pattern0.png"><figcaption>0</figcaption></figure>
<figure><img src="/docs/patterns/pattern1.png"><figcaption>1</figcaption></figure>
<figure><img src="/docs/patterns/pattern2.png"><figcaption>2</figcaption></figure>
<figure><img src="/docs/patterns/pattern3.png"><figcaption>3</figcaption></figure>
<figure><img src="/docs/patterns/pattern4.png"><figcaption>4</figcaption></figure>
<figure><img src="/docs/patterns/pattern5.png"><figcaption>5</figcaption></figure>
<figure><img src="/docs/patterns/pattern6.png"><figcaption>6</figcaption></figure>
<figure><img src="/docs/patterns/pattern7.png"><figcaption>7</figcaption></figure>
<figure><img src="/docs/patterns/pattern8.png"><figcaption>8</figcaption></figure>
<figure><img src="/docs/patterns/pattern9.png"><figcaption>9</figcaption></figure>
<figure><img src="/docs/patterns/pattern10.png"><figcaption>10</figcaption></figure>
<figure><img src="/docs/patterns/pattern11.png"><figcaption>11</figcaption></figure>
<figure><img src="/docs/patterns/pattern12.png"><figcaption>12</figcaption></figure>
<figure><img src="/docs/patterns/pattern13.png"><figcaption>13</figcaption></figure>
<figure><img src="/docs/patterns/pattern14.png"><figcaption>14</figcaption></figure>
<figure><img src="/docs/patterns/pattern15.png"><figcaption>15</figcaption></figure>
<figure><img src="/docs/patterns/pattern16.png"><figcaption>16</figcaption></figure>
<figure><img src="/docs/patterns/pattern17.png"><figcaption>17</figcaption></figure>
<figure><img src="/docs/patterns/pattern18.png"><figcaption>18</figcaption></figure>
<figure><img src="/docs/patterns/pattern19.png"><figcaption>19</figcaption></figure>
<figure><img src="/docs/patterns/pattern20.png"><figcaption>20</figcaption></figure>
<figure><img src="/docs/patterns/pattern21.png"><figcaption>21</figcaption></figure>
<figure><img src="/docs/patterns/pattern22.png"><figcaption>22</figcaption></figure>
<figure><img src="/docs/patterns/pattern23.png"><figcaption>23</figcaption></figure>
<figure><img src="/docs/patterns/pattern24.png"><figcaption>24</figcaption></figure>
<figure><img src="/docs/patterns/pattern25.png"><figcaption>25</figcaption></figure>
<figure><img src="/docs/patterns/pattern26.png"><figcaption>26</figcaption></figure>
<figure><img src="/docs/patterns/pattern27.png"><figcaption>27</figcaption></figure>
<figure><img src="/docs/patterns/pattern28.png"><figcaption>28</figcaption></figure>
<figure><img src="/docs/patterns/pattern29.png"><figcaption>29</figcaption></figure>
<figure><img src="/docs/patterns/pattern30.png"><figcaption>30</figcaption></figure>
<figure><img src="/docs/patterns/pattern31.png"><figcaption>31</figcaption></figure>
<figure><img src="/docs/patterns/pattern32.png"><figcaption>32</figcaption></figure>
<figure><img src="/docs/patterns/pattern33.png"><figcaption>33</figcaption></figure>
<figure><img src="/docs/patterns/pattern34.png"><figcaption>34</figcaption></figure>
<figure><img src="/docs/patterns/pattern35.png"><figcaption>35</figcaption></figure>
<figure><img src="/docs/patterns/pattern36.png"><figcaption>36</figcaption></figure>
<figure><img src="/docs/patterns/pattern37.png"><figcaption>37</figcaption></figure>
</div>

<style>
  /* a full-page layer that sits behind the content (above the gradient) and
     fades in a tiled pattern while a swatch above is hovered */
  #pattern-page-bg {
    position: fixed; inset: 0; z-index: -1; pointer-events: none;
    background-repeat: repeat; image-rendering: pixelated;
    opacity: 0; transition: opacity 0.5s ease;
  }
  #pattern-page-bg.active { opacity: 0.03; }
  .pattern-grid figure { cursor: pointer; }
</style>
<script>
  (function () {
    var bg = document.createElement("div");
    bg.id = "pattern-page-bg";
    document.body.appendChild(bg);

    document.querySelectorAll(".pattern-grid figure").forEach(function (fig) {
      var img = fig.querySelector("img");
      if (!img) return;
      fig.addEventListener("mouseenter", function () {
        bg.style.backgroundImage = "url('" + img.src + "')";
        bg.classList.add("active");
      });
      fig.addEventListener("mouseleave", function () {
        bg.classList.remove("active");
      });
    });
  })();
</script>

---
title: Working with sprites
summary: Pack artwork into a spritesheet on the image type, then draw, animate, scale and lay out individual sprites — using a deck of cards as the worked example.
icon: background_grid_small
---

# Introduction

A sprite is a small image that stands for one thing on screen — a character, an icon, a tile of scenery, or, in this guide, a single playing card. Almost every 2D game is really just a lot of sprites being moved, swapped and stacked on top of each other, many times a second.

Across Badgeware's displays, your sprites will usually be small, and you'll often draw a lot of them. We'll use a **deck of cards** to show how to store sprites efficiently and get them on screen — still, moving, scaled, or laid out into a scene.

# What is a spritesheet?

Storing every sprite in its own file quickly gets unwieldy, and loading dozens of files is slow. Instead, related sprites are packed together into a single image called a **spritesheet** — a grid of equally-sized cells. Here's the one we'll use: an entire deck of cards — every rank and suit, plus card backs and jokers — on a single image.

<figure style="text-align: center; margin: 1.5em auto;">
  <img src="/docs/guides/assets/cards.png" alt="A pixel-art deck-of-cards spritesheet: thirteen columns of ranks across four suit rows, then a row of patterned card backs, then a row of jokers" style="display: block; margin: 0 auto; width: 650px; max-width: 100%; height: auto; image-rendering: pixelated;">
  <figcaption style="margin-top: 0.6em; font-style: italic; font-size: 0.85em; opacity: 0.7;">The example spritesheet — a full deck laid out as a 13 × 6 grid: ranks across, suits down, then a row of card backs (with a shadow silhouette in the last cell) and a row of jokers.</figcaption>
</figure>

Keeping everything in one image means:

- **One load, not dozens** — the whole deck is a single file
- **Related art stays together** — every card lives in one place
- **Memory-efficient reuse** — draw the same card repeatedly without loading or storing another copy

Badgeware provides some help handling sprites via a few options on the [`image`](/api/image.md) type. When you load or create an image you can tell it how many **columns** and **rows** its grid has, and then pull out any individual cell as a sprite:

```python
# load the sheet: 13 columns x 6 rows
deck = image.load("/system/assets/cards.png")

# convert the loaded image into a spritesheet
deck.spritesheet(13, 6)

# pull out one cell (the Ace of Hearts)
ace = deck.sprite(0, 1)

# solid green felt, then dark + light specks softly over the top
def draw_background():
  screen.pen = color.green
  screen.clear()
  screen.pen = brush.pattern(color.rgb(0, 0, 0, 20), color.rgb(0, 0, 0, 0), 8)
  screen.clear(0, 0, screen.width, screen.height)

while True:
  draw_background()
  screen.blit(ace, 20, 20)
  badge.update()
```

# Anatomy of a spritesheet

Each cell is addressed by its column (`x`) and row (`y`), counting from `(0, 0)` in the top-left corner. Crucially, `sprite()` takes the **column first, then the row**:

![A grid of sprite cells, with column numbers along the top and row numbers down the side, showing the cell at column 3 row 1 pulled out with sprite(3, 1)](/guides/assets/sprite-grid.svg)

On our deck, `sprite(3, 1)` (column 3, row 1) is the 4 of Hearts. `sprite()` hands you back that cell as an ordinary `image` — a lightweight *view* onto the sheet that shares the same pixels rather than copying them, so it's cheap to call. Fetch sprites fresh every frame; there's no need to hold on to them.

For our example spritesheet we've arranged it such that the **row picks the suit** and the **column picks the rank**:

| Row | Contents |
|---|---|
| `0` | ♠ spades |
| `1` | ♥ hearts |
| `2` | ♦ diamonds |
| `3` | ♣ clubs |
| `4` | 12 card backs (columns 0–11) and a **shadow** silhouette (column 12) |
| `5` | four jokers (columns 0–3) |

Within a suit row the columns run `0 = Ace`, `1–9 = 2–10`, `10 = Jack`, `11 = Queen`, `12 = King`.

# Drawing sprites

To put a sprite on the screen you `blit()` it — passing the sprite and a position. Let's deal a hand of five cards, fan them out, and give each a drop shadow using the deck's **shadow** sprite (the silhouette in the last cell of the backs row):

```python
# load the sheet: 13 columns x 6 rows
deck = image.load("/system/assets/cards.png")

# convert the loaded image into a spritesheet
deck.spritesheet(13, 6)

shadow = deck.sprite(12, 4)
shadow.alpha = 100

# five cards, each a (column, row) = (rank, suit) pair
hand = [(0, 1), (12, 0), (11, 2), (10, 3), (9, 1)]   # A♥  K♠  Q♦  J♣  10♥

# solid green felt, then dark + light specks softly over the top
def draw_background():
  screen.pen = color.green
  screen.clear()
  screen.pen = brush.pattern(color.rgb(0, 0, 0, 20), color.rgb(0, 0, 0, 0), 8)
  screen.clear(0, 0, screen.width, screen.height)

while True:
  draw_background()

  x = 6
  for rank, suit in hand:
    screen.blit(shadow, x + 2, 45)              # drop shadow, nudged down-right
    screen.blit(deck.sprite(rank, suit), x, 43)
    x += 30                                    # overlap the cards into a fan

  badge.update()
```

Because each `sprite()` is a cheap view onto the loaded sheet, drawing a whole hand doesn't require separate images for every card. The shadow sprite is a plain dark silhouette; setting its `alpha` lower makes it softer without affecting anything else you draw.

# Animation

Nothing on the badge stays still for long. `badge.ticks` counts upwards in milliseconds, so by working out *where* to draw from it you can move things around. Let's **deal a hand for real** — five random cards, one at a time, each sliding out of a face-down deck into its slot. Every card becomes a small **`Card`** object that carries its own value, sprite and position, and `hand` starts empty and fills up as they're dealt:

```python
import random

deck = image.load("/system/assets/cards.png")
deck.spritesheet(13, 6)

shadow = deck.sprite(12, 4)     # the silhouette we draw under every card
shadow.alpha = 100              # softened so it reads as a shadow
back = deck.sprite(0, 4)        # a face-down card, for the deck itself

deck_position = vec2(128, 4)    # the face-down deck sits here, top-right
DEAL_TIME = 0.3                 # seconds to slide one card into place

hand = []                       # the cards on the table, filled in as we deal


# A Card bundles what we need to know about one card: its value (which card it
# is), its sprite (the artwork) and where it currently sits — and it can draw
# itself, shadow and all.
class Card:
  def __init__(self, rank, suit):
    self.value = (rank, suit)              # the card's identity, for game logic
    self.sprite = deck.sprite(rank, suit)  # a cheap view onto the sheet
    self.pos = deck_position               # it starts on top of the deck

  def draw(self):
    screen.blit(shadow, self.pos + vec2(2, 2))   # soft drop shadow, down-right
    screen.blit(self.sprite, self.pos)


def draw_background():
  screen.pen = color.green
  screen.clear()
  screen.pen = brush.pattern(color.rgb(0, 0, 0, 20), color.rgb(0, 0, 0, 0), 8)
  screen.clear(0, 0, screen.width, screen.height)

# redraw the whole table: the felt, the deck, then every card in the hand
def draw_scene():
  draw_background()
  screen.blit(back, deck_position)
  for card in hand:
    card.draw()

# deal five random cards, sliding each from the deck into its slot in the fan
def deal_hand():
  hand.clear()
  for i in range(5):
    card = Card(random.randint(0, 12), random.randint(0, 3))   # random rank + suit
    hand.append(card)                       # on the table now (still on the deck)
    target = vec2(6 + i * 30, 60)           # this card's slot in the fan
    slide = tween(card.pos, target, DEAL_TIME, easing=tween.BACK_OUT)

    start = badge.ticks
    while (badge.ticks - start) / 1000 < DEAL_TIME:   # badge.ticks is in milliseconds
      card.pos = slide.at((badge.ticks - start) / 1000)   # feed it the elapsed seconds
      draw_scene()
      badge.update()
    card.pos = target                                 # settle exactly on the slot

  start = badge.ticks
  while badge.ticks - start < 1000:         # admire the full hand a moment
    draw_scene()
    badge.update()

while True:
  deal_hand()
```

Because each card carries its own `pos`, drawing gets simple: `draw_scene()` clears the felt, draws the deck, then walks `hand` asking every card to `draw()` itself — no need to track positions separately, or to treat the card that's still moving any differently from the ones that have landed.

`deal_hand()` empties `hand`, then for each of five cards reads straight down the page: pick a random rank and suit, make a `Card`, add it to `hand`, and slide its `pos` with a **`tween`** between two `vec2`s — the deck and the card's slot. Giving the tween a **duration** (`DEAL_TIME`, 0.3 seconds) means we feed `at()` the elapsed *time* rather than a 0–1 fraction; it works out the progress and clamps at the ends for us. We read that elapsed time straight off `badge.ticks` (in milliseconds, hence the `/ 1000`), so each card takes the same 0.3 seconds however fast the badge is drawing, and `tween.BACK_OUT` gives it a little overshoot as it settles. Since the sliding card is already in `hand`, a single `draw_scene()` redraws it — and every card dealt so far — each frame, so the hand builds up one card at a time. To animate a *character* you'd drive a frame index from the clock the same way — `sprite(int(badge.ticks / 80) % frames, row)`.

# Scaling

Blitting into a `rect` stretches the sprite to fill it, so you can draw a sprite at any size. Let's flick through the hand as if picking cards — the fan sits in the centre with its shadows, and each card in turn zooms up out of it:

```python
deck = image.load("/system/assets/cards.png")
deck.spritesheet(13, 6)

shadow = deck.sprite(12, 4)   # a dark silhouette, drawn under each card
shadow.alpha = 100

CARD_W, CARD_H = 25, 35       # the size of one card
hand = [(0, 1), (12, 0), (11, 2), (10, 3), (9, 1)]   # A♥  K♠  Q♦  J♣  10♥

FAN_X, FAN_Y, SPACING = 17, 56, 26   # where the fan sits, and the card gap

# solid green felt, then dark + light specks softly over the top
def draw_background():
  screen.pen = color.green
  screen.clear()
  screen.pen = brush.pattern(color.rgb(0, 0, 0, 20), color.rgb(0, 0, 0, 0), 8)
  screen.clear(0, 0, screen.width, screen.height)

# draw one card scaled up from its slot, lifting as it grows
def draw_card(i, scale):
  rank, suit = hand[i]
  w, h = int(CARD_W * scale), int(CARD_H * scale)
  x = FAN_X + i * SPACING - (w - CARD_W) // 2     # centre on its slot
  y = FAN_Y + CARD_H - h - int(6 * (scale - 1))   # grow upward, lifted
  screen.blit(shadow, rect(x + 3, y + 3, w, h))
  screen.blit(deck.sprite(rank, suit), rect(x, y, w, h))

# the picked card eases from its normal size up to a crisp 2x
grow = tween(1.0, 2.0, easing=tween.BACK_OUT)

selected = 0
while True:
  selected = (selected + 1) % len(hand)     # move on to the next card

  # zoom it up and hold for 1.2 seconds, redrawing the fan each frame
  start = badge.ticks
  while badge.ticks - start < 1200:
    draw_background()

    scale = grow.at((badge.ticks - start) / 325)   # the zoom, right now

    # draw the fan, then the picked card bigger and on top
    for i in range(len(hand)):
      if i != selected:
        draw_card(i, 1)
    draw_card(selected, scale)

    badge.update()
```

The loop reads top to bottom: pick the next card, then zoom it up and hold for 1.2 seconds before moving on. Each card is drawn by `draw_card()`, which blits it into a `rect` sized `CARD_W × CARD_H` scaled by its `scale` — the sprite is sampled up to fill it, so one small sprite draws at any size, shadow and all. Neighbours stay at `1`× while the picked card's `scale` comes from the `tween`, settling at exactly **2×** — a whole number, so each source pixel maps to a clean 2 × 2 block and the pixel art stays crisp. It's drawn last so it sits above its neighbours, and `tween.BACK_OUT` adds a little overshoot as it grows — only in motion; it comes to rest bang on 2×. Passing a negative width or height in the `rect` flips the sprite as it scales, too — handy for mirroring rather than storing a second copy.

# Transforming sprites

`blit()` into a `rect` scales and flips, but it stays axis-aligned — it can't **rotate** a sprite or skew it. For an arbitrary transform, fill a **shape** with an [**image brush**](/api/brush.md#image-brushes) and drive both from the same [`mat3`](/api/mat3.md) matrix. `brush.image(sprite, matrix)` paints the sprite through the matrix, and a `shape` carries a `transform` of its own — give them the same matrix and the sprite lands exactly inside the shape. Make that shape a rectangle the size of the card and it fills cleanly. Here a card spins and pulses in the middle of the screen:

```python
import math

deck = image.load("/system/assets/cards.png")
deck.spritesheet(13, 6)
card = deck.sprite(0, 0)     # the Ace of Spades
cw = card.width
ch = card.height

while True:
  screen.pen = color.green
  screen.clear()

  angle = badge.ticks / 12                # spin, in degrees
  s = 2 + math.sin(badge.ticks / 500)     # pulse between 1x and 3x

  # centre the card on its own middle, scale it, spin it, then place it
  m = mat3().translate(80, 60).rotate(angle).scale(s, s).translate(-cw / 2, -ch / 2)

  outline = shape.rectangle(0, 0, cw, ch)
  outline.transform = m                   # the shape follows the matrix...
  screen.pen = brush.image(card, m)       # ...and so does the sprite that fills it
  screen.shape(outline)

  badge.update()
```

The matrix is built by chaining, and applies **right to left**: `translate(-cw / 2, -ch / 2)` shifts the card so its centre is at the origin, then `scale()` and `rotate()` act about that centre, and finally `translate(80, 60)` drops it in the middle of the screen. Because the outline rectangle carries the *same* matrix, it lands right on the sprite's edges — and that's what stops the brush tiling, since an image brush repeats to cover any of the shape that spills past the image. Swap in any `mat3` — a non-uniform `scale(2, 1)`, a skew, a wobble driven by `badge.ticks` — and both the shape and the sprite filling it move together.

For the full reference on `load()`, `sprite()` and the different `blit()` forms, see the [`image` API](/api/image.md#spritesheets).

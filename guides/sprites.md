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
  <img src="/docs/guides/assets/cards-2x.png" alt="A pixel-art deck-of-cards spritesheet: thirteen columns of ranks across four suit rows, then a row of patterned card backs, then a row of jokers" style="display: block; margin: 0 auto; max-width: 100%; height: auto;">
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

Nothing on the badge stays still for long. `badge.ticks` counts upwards in milliseconds, and by working out *where* to draw from it you can move things around. Let's **deal the hand for real** — sliding each card out from a face-down deck into its place in the fan:

```python
deck = image.load("/system/assets/cards.png")
deck.spritesheet(13, 6)

shadow = deck.sprite(12, 4)
shadow.alpha = 100
back = deck.sprite(0, 4)   # a face-down card back
hand = [(0, 1), (12, 0), (11, 2), (10, 3), (9, 1)]   # A♥  K♠  Q♦  J♣  10♥

DECK_X, DECK_Y = 128, 4   # top of the face-down deck; cards deal from here

# one tween per card: deck -> its slot in the fan, with an overshoot settle
deals = []
for i in range(len(hand)):
  start = vec2(DECK_X, DECK_Y)
  slot = vec2(6 + i * 30, 60)
  deals.append(tween(start, slot, easing=tween.BACK_OUT))

# solid green felt, then dark + light specks softly over the top
def draw_background():
  screen.pen = color.green
  screen.clear()
  screen.pen = brush.pattern(color.rgb(0, 0, 0, 20), color.rgb(0, 0, 0, 0), 8)
  screen.clear(0, 0, screen.width, screen.height)

while True:
  draw_background()

  # the face-down deck the cards are dealt from (a short stack + shadow)
  screen.blit(shadow, DECK_X + 4, DECK_Y + 4)
  for d in range(2, -1, -1):
    screen.blit(back, DECK_X + d, DECK_Y + d)

  t = badge.ticks % 3000   # loop the whole deal every 3s

  for i, (rank, suit) in enumerate(hand):
    # this card starts 250ms after the last, then slides for 300ms
    p = min(1.0, (t - i * 250) / 300)
    if p <= 0:
      continue

    pos = deals[i].at(p)   # eased position from the deck to the slot
    screen.blit(shadow, pos + vec2(2, 2))
    screen.blit(deck.sprite(rank, suit), pos)

  # present this frame, then clear for the next
  badge.update()
```

Rather than lerp the position by hand, each card gets a **`tween`** — an object that maps a progress value to an eased point between two endpoints (here `vec2`s: the deck and the card's slot). A tween holds no clock of its own, so we still derive the progress `p` (0 → 1) from `badge.ticks` and read the eased position back with `at(p)`. Because progress comes from the clock, the deal takes the same real time however fast the badge draws — and swapping the easing curve (`tween.BACK_OUT` gives a little overshoot as each card settles) changes the *feel* without touching the timing. To animate a *character* you'd drive a frame index from the clock the same way — `sprite(int(badge.ticks / 80) % frames, row)`.

# Scaling

Blitting into a `rect` stretches the sprite to fill it, so you can draw a card at any size. Let's lift the middle card of the hand and blow it up, as if it's been picked out:

```python
deck = image.load("/system/assets/cards.png")
deck.spritesheet(13, 6)

shadow = deck.sprite(12, 4)
shadow.alpha = 100
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
    screen.blit(shadow, x + 2, 45)
    screen.blit(deck.sprite(rank, suit), x, 43)
    x += 22

  # lift the middle card out and draw it 1.6x larger, on top
  rank, suit = hand[2]
  screen.blit(deck.sprite(rank, suit), rect(42, 26, 40, 56))
  badge.update()
```

Passing a negative width or height in the `rect` flips the sprite as it scales, too — handy for mirroring a sprite rather than storing a second copy.

For the full reference on `load()`, `sprite()` and the different `blit()` forms, see the [`image` API](/api/image.md#spritesheets).

---
title: Reading the buttons
summary: Control how applications detect both single presses and continuous holds, enabling responsive controls for menus and interactivity.
icon: gamepad_down
---

# Detecting button state

Badgeware features five front-facing buttons — **A**, **B**, **C**, **UP**, and **DOWN** — along with a **HOME** button on the rear. In code, each is identified by a constant:

- `BUTTON_A`
- `BUTTON_B`
- `BUTTON_C`
- `BUTTON_UP`
- `BUTTON_DOWN`
- `BUTTON_HOME`

The `badge` module provides methods to read the state of these buttons:

| Method | Returns |
|---|---|
| `pressed([button])` | `True` if the button specified was pressed, or a list of all pressed buttons if no button specified |
| `released([button])` | `True` if the button specified was released, or a list of all released buttons if no button specified |
| `held([button])` | `True` if the button specified is held down, or a list of all held buttons if no button specified |
| `changed([button])` | `True` if the button specified just changed state, or a list of all changed buttons if no button specified |

```python-raw
# pass a button to test just that one
if badge.pressed(BUTTON_A):
  print("A was pressed")

# or call with no argument to get a list
for button in badge.held():
  print("holding", button)
```

These methods report the button state as of the most recent `badge.update()`. That call refreshes the display and takes a fresh reading of the buttons, so call it regularly — typically once each time round your loop — to keep things up to date.

There are two main ways to handle button input:

- Single press actions: for tasks like menu navigation or option selection, you typically want to respond only when a button is first pressed. Use **pressed**, **released**, and **changed** to handle button events like these.
- Continuous actions: for games or repeated interactions, you often want something to happen continuously while a button is held down. Use **held** each frame to determine if a button is currently pressed.

The example below makes the difference visible: each button lights up while it is **held**, and a line of text shows the most recent **pressed** or **released** event. Watch a button's box fill the whole time you hold it (continuous state), while the text updates only at the moment you press or let go (one-shot events).

```python
screen.font = rom_font.nope

# each button constant, with a label and where to draw its box — positioned to match
# the badge: A B C evenly spaced along the bottom, UP and DOWN up the right-hand edge
# (the display is 160 x 120)
BUTTONS = [
  (BUTTON_A,    "A",     16, 96),
  (BUTTON_B,    "B",     64, 96),
  (BUTTON_C,    "C",    112, 96),
  (BUTTON_UP,   "UP",   114, 26),
  (BUTTON_DOWN, "DOWN", 114, 62),
]

# the most recent one-shot event, shown beneath the buttons
last_event = "press a button"

while True:
  # pressed() and released() fire on a single frame — capture the latest one
  for button, name, x, y in BUTTONS:
    if badge.pressed(button):
      last_event = name + " pressed"
    if badge.released(button):
      last_event = name + " released"

  # draw each button, filled bright while held() is true, dim otherwise
  for button, name, x, y in BUTTONS:
    if badge.held(button):
      screen.pen = color.orange
    else:
      screen.pen = color.rgb(40, 44, 66)
    screen.rectangle(x, y, 42, 22)
    screen.pen = color.white
    screen.text(name, x + 5, y + 7)

  # show the latest press/release in the free space, top-left
  screen.pen = color.white
  screen.text(last_event, 8, 14)

  badge.update()
```

# Examples

## A simple menu

This example demonstrates a simple menu system for Badgeware. It shows how to draw a list of menu items on the display and navigate through them with the **UP** and **DOWN** buttons. The currently selected item is highlighted, and the menu index wraps around so you can cycle smoothly through all options.

```python {len=6}
screen.font = rom_font.nope

menu_items = [
  "Free loot!",
  "Bad idea, but ok.",
  "Thanks... I think.",
  "Welp. o_O"
]
selected = 0

while True:
  # move the selection up or down as those buttons are pressed
  if badge.pressed(BUTTON_UP):
    selected -= 1

  if badge.pressed(BUTTON_DOWN):
    selected += 1

  # wrap the index so it cycles around the ends of the menu
  selected %= len(menu_items)

  # write out the dialogue
  screen.pen = color.white
  screen.text("IT'S DANGEROUS TO GO", 10, 10)
  screen.text("ALONE! TAKE THIS.", 10, 22)

  # draw the menu of response options on the screen
  for i in range(len(menu_items)):
    screen.pen = color.taupe

    # if this is the selected item then highlight it
    if i == selected:
      screen.text(">", 10, i * 15 + 50)
      screen.pen = color.white

    # write the menu item label
    screen.text(menu_items[i], 20, i * 15 + 50)

  badge.update()
```

## A tiny snake game
This example steers a snake around the screen: **UP** and **DOWN** move it vertically, **A** and **C** move it left and right. The snake advances on its own — the buttons only change its direction, and it can't turn straight back on itself. It wraps around the edges of the display.

The snake moves on an 8-pixel grid, so its position is tracked in grid cells rather than pixels. Its body is just a list of cells; each step we add a new head and drop the tail, which slides it forward at a fixed length.

```python
screen.font = rom_font.nope

CELL = 8                          # size of one grid square, in pixels
COLS, ROWS = 160 // CELL, 120 // CELL

# the snake's body as a list of [col, row] cells — the head is the last one
snake = [[3, 7], [4, 7], [5, 7], [6, 7], [7, 7]]
dx, dy = 1, 0                      # current direction (moving right)

STEP_MS = 200                      # advance one cell every 200 milliseconds
last_step = badge.ticks           # badge.ticks is the clock in milliseconds

while True:
  # steer with the buttons, but never straight back on itself
  if badge.pressed(BUTTON_UP) and dy == 0:
    dx, dy = 0, -1
  if badge.pressed(BUTTON_DOWN) and dy == 0:
    dx, dy = 0, 1
  if badge.pressed(BUTTON_A) and dx == 0:
    dx, dy = -1, 0
  if badge.pressed(BUTTON_C) and dx == 0:
    dx, dy = 1, 0

  # advance one cell once enough time has passed
  if badge.ticks - last_step >= STEP_MS:
    last_step = badge.ticks
    head = snake[-1]
    new_x = (head[0] + dx) % COLS   # wrap around the edges
    new_y = (head[1] + dy) % ROWS
    snake.append([new_x, new_y])
    snake.pop(0)                    # drop the tail to keep a fixed length

  # draw each body cell, leaving a 1px gap so the segments are visible
  screen.pen = color.lime
  for col, row in snake:
    screen.rectangle(col * CELL, row * CELL, CELL - 1, CELL - 1)

  badge.update()
```

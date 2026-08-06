---
title: Let's write some code
summary: Build a small badge app one stage at a time — setup, a loading screen, a menu, and something to do.
icon: code
publish: true
sort: 2
---
# Let's write some code

Now you've met the hardware, let's build a small app one step at a time. A Badgeware app is just a Python script: you write it from top to bottom, and call `badge.update()` whenever you want to show what you've drawn and refresh the buttons. Draw, update, repeat, making screens and menus a breeze.

We'll write each part as its own little **function** — one for the loading screen, one for the menu, one for the action — then wire them together at the end. Breaking up your code this way keeps each piece simple, and the final program ends up reading almost like a to-do list.

> This one's written for **Tufty** and its full-colour screen. The ideas carry across to **Badger** and **Blinky** too, but the specifics won't — Badger's e-paper redraws differently, and Blinky's LED matrix is a lower resolution.

# 1. Basic setup

Every app starts by setting the stage. First, imports. For convenience, `screen`, `badge`, `color`, `font` and other essentials are **always available** — they're needed by every badge app, so Badgeware builds them in for you. Anything else — `time`, networking, and so on — you import yourself, just like normal Python.

We only need `time` here, for the pause on the loading screen. While we're at it, we'll choose a pen colour and font; once, up front, so the rest of the app can just draw without repeating itself:

```python-raw
import time                     # for the pause on the loading screen

screen.pen = color.white        # everything we draw will be white...
screen.font = font.smart    # ...in the built-in "smart" font
```

With those prepared ahead of time, each part below is just drawing and reading buttons.

# 2. A loading screen

Let's start with a title screen that appears for a moment when the app launches.

```python-raw
def loading_screen():
  screen.text("MY BADGE", 10, 40)
  screen.text("starting up...", 10, 70)

  badge.update()      # show what we've drawn
  time.sleep(1.5)     # ...and hold it for a moment and a half
```

See how linear it is?: draw, `badge.update()` to show it, then `time.sleep()` to pause. Because you're in charge of the flow, timing things is as simple as sleeping. And handily, `badge.update()` also wipes the framebuffer clean ready for the next frame — so you just draw what you want to see, with no need to clear the screen yourself.

# 3. A menu

Next, a menu you can navigate with **UP** and **DOWN**, picking an item with **A**. We'll write it to *return* the chosen item's number, so whoever calls it knows what was picked.

```python-raw
def menu(items):
  selected = 0
  while True:
    # draw the menu, with a marker next to the current choice
    for i in range(len(items)):
      marker = "> " if i == selected else "  "
      screen.text(marker + items[i], 10, 30 + i * 20)
    badge.update()

    # move the highlight, or pick the current item
    if badge.pressed(BUTTON_UP):
      selected = (selected - 1) % len(items)
    if badge.pressed(BUTTON_DOWN):
      selected = (selected + 1) % len(items)
    if badge.pressed(BUTTON_A):
      return selected     # hand the choice back to the caller
```

The key is `badge.pressed()`. It's `True` only on the `badge.update()` where a button *first* goes down — the moment of the press — not for the whole time it's held. So one tap moves the selection exactly one step, no matter how long your finger lingers.

So each time round the loop we redraw the menu, call `badge.update()`, then nudge `selected` if **UP** or **DOWN** was just pressed. The `% len(items)` wraps the selection neatly around the ends, and pressing **A** ends the loop by `return`ing the chosen number.

# 4. An action

Finally, something to *do* with the choice: show a screen for the picked item until **B** takes us back.

```python-raw
def show_item(selected):
  while not badge.pressed(BUTTON_B):
    if selected == 0:
      screen.text("Hello there!", 10, 40)
    elif selected == 1:
      screen.text("Zzz... counting sheep", 10, 40)
    else:
      screen.text("My Badgeware badge", 10, 40)

    screen.text("B to go back", 10, 90)
    badge.update()
```

It's just another loop — it runs until **B** is pressed, then returns to whoever called it. Writing each screen and sub-screen as its own function like this keeps the whole app tidy and easy to follow as it grows.

# Putting it together

With the setup done and those three functions written, the actual program is tiny — show the loading screen once, then loop forever: show the menu, then show whatever was picked.

```python-raw
loading_screen()

items = ["Say hello", "Count sheep", "About"]
while True:
  choice = menu(items)
  show_item(choice)
```

And that's the whole app. Here it is all in one place, ready to run:

```python
import time

screen.pen = color.white
screen.font = font.smart

def loading_screen():
  screen.text("MY BADGE", 10, 40)
  screen.text("starting up...", 10, 70)
  badge.update()
  time.sleep(1.5)

def menu(items):
  selected = 0
  while True:
    for i in range(len(items)):
      marker = "> " if i == selected else "  "
      screen.text(marker + items[i], 10, 30 + i * 20)
    badge.update()

    if badge.pressed(BUTTON_UP):
      selected = (selected - 1) % len(items)
    if badge.pressed(BUTTON_DOWN):
      selected = (selected + 1) % len(items)
    if badge.pressed(BUTTON_A):
      return selected

def show_item(selected):
  while not badge.pressed(BUTTON_B):
    if selected == 0:
      screen.text("Hello there!", 10, 40)
    elif selected == 1:
      screen.text("Zzz... counting sheep", 10, 40)
    else:
      screen.text("My Badgeware badge", 10, 40)
    screen.text("B to go back", 10, 90)
    badge.update()

# --- run the app ---
loading_screen()

items = ["Say hello", "Count sheep", "About"]
while True:
  choice = menu(items)
  show_item(choice)
```

# Run it on your badge

No need to save this to the badge yet — the quickest way to try it is to run it **straight onto the device** from an editor. Open it in [Thonny](https://thonny.org) or VS Code (with the [MicroPico](https://github.com/paulober/MicroPico) extension), plug your badge in over USB, and hit run. Your code runs live on the badge — no copying files, no reboot — so you can tweak and re-run in seconds.

If you don't have a badge yet, [try.badgewa.re](https://try.badgewa.re) has you covered!

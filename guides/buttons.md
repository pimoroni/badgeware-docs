---
title: Buttons
summary: Control how applications detect both single presses and continuous holds, enabling responsive controls for menus and interactivity.
icon: gamepad_down
---

# Introduction

The `badge` module provides all the functionality needed to detect button states and handle user input events in your application.

# User and Home buttons

Badgeware features five front-facing buttons — **A**, **B**, **C**, **UP**, and **DOWN** — along with a **HOME** button on the rear.

You can query the state of these buttons using the `badge` module, which provides four methods returning button activity during each frame:

- `pressed()`: returns buttons that were pressed during the current frame
- `released()`: returns buttons that were released during the current frame
- `held()`: returns buttons that are currently being held down
- `changed()`: returns buttons that have changed state this frame

Each button is represented by a constant (for example, `BUTTON_A`). The API allows you to check whether a button has been pressed, released, or held, and whether its state has changed during the current frame.

If you pass these methods a button constant as a parameter, they will return a bool representing whether that button fits the criteria. If you call them without a parameter as above, they will return a list of all button constants that fit the criteria.

> For the **pressed** and **released** lists, buttons are only included on the first frame in which the event occurs.

# Reset button
**RESET** is a special button which is used to put Badgeware into different modes and cannot be used within applications.

- **Tap**: Resets Badgeware and boots back into the launcher.
- **Double tap**: Puts Badgeware into Disk Mode which it will appear as a disk on any computer it is plugged into.
- **Long press**: Puts Badgeware into deep sleep. In this mode your badge will conserve battery but can be woken at any time by pressing any of the front buttons or scheduling an alarm.
- **Tap while holding down HOME**: Resets Badgeware and enters the RP2350 DFU bootloader, useful for updating the Badgeware firmware.

# Detecting button state

There are two main ways to handle button input:

- Single press actions: for tasks like menu navigation or option selection, you typically want to respond only when a button is first pressed. Use **pressed**, **released**, and **changed** to handle button events like these.
- Continuous actions: for games or repeated interactions, you often want something to happen continuously while a button is held down. Use **held** each frame to determine if a button is currently pressed.

By testing whether a button appears in the pressed, held, released, or changed lists, you can respond to input events as they occur. This approach lets you distinguish between single actions, continuous input, and general state changes, giving you fine control over how your application reacts to user interaction.

> Note: Click on the emulator to allow it to capture input. Use the arrow keys and space on your keyboard to try the example out!

```python
last_event = None

def update():
  global last_event

  # true only when button A is newly pressed this frame
  if badge.pressed(BUTTON_A):
    last_event = "BUTTON A PRESSED!"

  # true continuously while button B is being held
  if badge.held(BUTTON_B):
    last_event = "BUTTON B HELD!"

  # true only if button C has been released this frame
  if badge.released(BUTTON_C):
    last_event = "BUTTON C RELEASED!"

  # true only if button UP has changed state this frame
  if badge.changed(BUTTON_UP):
    last_event = "BUTTON UP CHANGED!"

  if last_event:
    screen.pen = color.white
    screen.text(last_event, 10, 10)

run(update)
```

# Examples

## Navigating a menu

This example demonstrates a simple menu system for Badgeware. It shows how to draw a list of menu items on the display and navigate through them with the **UP** and **DOWN** buttons. The currently selected item is highlighted, and the menu index wraps around so you can cycle smoothly through all options.

> Note: Click on the emulator to allow it to capture input. Use the arrow keys and space on your keyboard to try the example out!

```python {len=6}
screen.font = rom_font.nope

menu_items = [
  "Free loot!",
  "Bad idea, but ok.",
  "Thanks... I think.",
  "Welp. o_O"
]
selected = 0

def update():
  global selected

  # adjust selected item index based on button presses
  if badge.pressed(BUTTON_UP):
    selected -= 1

  if badge.pressed(BUTTON_DOWN):
    selected += 1

  # wrap and clamp selected index to the range of items in the menu
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

run(update)
```

## Controlling a character
This example demonstrates simple character movement on Badgeware, showing how to combine button input with basic motion and drawing. The character is represented as a small circle that can move left or right using the A and C buttons and jump with the B button.

Gravity and basic physics are simulated to create a natural sense of movement.

> Note: Click on the emulator to allow it to capture input. Use the arrow keys + space on your keyboard to try the example out!

```python
# character's position and motion vector
pos = vec2(80, 60)
vec = vec2(0, 0)

def update():
  global pos, vec

  if badge.held(BUTTON_A):
    vec.x = -1 # move left

  if badge.held(BUTTON_C):
    vec.x = 1 # move right

  if badge.pressed(BUTTON_B):
    vec.y = -3 # jump when B is pressed

  # dampen sideways movement
  vec.x *= 0.8

  # apply very rudimentary gravity
  vec.y += 0.15

  pos += vec

  # clamp to floor
  if pos.y > 90:
    vec.y = 0
    pos.y = 90

  # draw the floor
  screen.pen = color.white
  screen.rectangle(0, 96, 160, 26)

  # draw the character
  screen.pen = color.red
  screen.circle(pos, 5)

run(update)
```

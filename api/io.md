---
title: io
summary: Access to various system and hardware features such as the clock, battery status, and user buttons.
icon: build
publish: true
---
# `io` - access to hardware features

This module exposes helpful information about the state of the badge hardware including the buttons and clock.

## Timing

`io.ticks`\
The number of ticks (milliseconds) since the badge was powered on when `update()` was called.

`io.ticks_delta`\
The number of ticks (milliseconds) since the previous time `update()` was called. Useful for timing animations where the framerate isn't completely stable.

## Reading button state

There are two main ways to handle button input.
- For things like menu navigation, you usually want to respond only when a button is first pressed.
- For games or continuous actions, you often want something to happen as long as the button is held down.

The API lets you check the state of each button — whether it has been `pressed`, `released`, `held`, or `changed` during the current frame.

> Note: Click on the emulator to allow it to capture input. Use the arrow keys and space on your keyboard to try the example out!

```python
last_event = None

def update():
  global last_event

  # true only when button A is newly pressed this frame
  if io.BUTTON_A in io.pressed:
    last_event = "BUTTON A PRESSED!"

  # true continuously while button B is being held
  if io.BUTTON_B in io.held:
    last_event = "BUTTON B HELD!"

  # true only if button C has been released this frame
  if io.BUTTON_C in io.released:
    last_event = "BUTTON C RELEASED!"

  # true only if button UP has changed state this frame
  if io.BUTTON_UP in io.changed:
    last_event = "BUTTON UP CHANGED!"

  if last_event:
    screen.pen = color.white
    screen.text(last_event, 10, 10)
```

`io.pressed`\
A list of buttons that were just pressed during the current frame — that is, buttons that switched from not pressed last frame to pressed this frame.

To check which buttons are currently being held down, use `io.held` instead.

`io.released`\
A list of buttons that were just released during the current frame — that is, buttons that switched from pressed last frame to not pressed this frame.

To check which buttons are currently being held down, use `io.held` instead.

`io.held`\
A list of all buttons that are currently held down.

`io.changed`\
A list of all buttons whose state changed between the last frame and the current frame.

## Backlight LEDs

> TODO

## Battery status

> TODO

## Constants

`io.BUTTON_HOME`\
`io.BUTTON_A`\
`io.BUTTON_B`\
`io.BUTTON_C`\
`io.BUTTON_UP`\
`io.BUTTON_DOWN`

Identifiers for each of the software useable buttons.

`io.LED_TOP_LEFT`\
`io.LED_TOP_RIGHT`\
`io.LED_BOTTOM_RIGHT`\
`io.LED_BOTTOM_LEFT`

Identifiers for each of backlight LEDs.
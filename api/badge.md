---
title: badge
summary: Access to various system and hardware features such as the battery status and user buttons.
icon: badge
publish: true
---

# Introduction
The `badge` class offers access to the badge's hardware. Using this class you can find out important system information, access the buttons and control the rear lighting.

# Properties

## ticks
The number of ticks (milliseconds) since the badge was powered on when `update()` was called.

## ticks_delta
The number of ticks (milliseconds) since the previous time `update()` was called. Useful for timing animations where the framerate isn't completely stable.

## uid
Provides a unique ID for the badge, as a hex string.

## model
The model of badge the code is running on, as a string: `"tufty"`, `"badger"`, or `"blinky"`. Useful for adapting an app to the different displays — see [Coding for the different badges](/introduction/badge-differences.md).

## resolution
The display resolution of the badge as a tuple containing pixel width and height as ints.

# Buttons
There are two main ways to handle button input.
- For things like menu navigation, you usually want to respond only when a button is first pressed.
- For games or continuous actions, you often want something to happen as long as the button is held down.

The API lets you check the state of each button — whether it has been `pressed`, `released`, `held`, or `changed` during the current frame.

There are a couple of ways to check on button status. Using the following methods with no arguments will return the list of buttons with the respective status, but if you want to check a specific button quickly you can pass that button in as an argument and get back `True` or `False`.

Buttons are addressed one by one using the following constants:
`BUTTON_A`
`BUTTON_B`
`BUTTON_C`
`BUTTON_UP`
`BUTTON_DOWN`
`BUTTON_HOME`

## pressed()
Returns a list of buttons pressed during the current frame - that is, buttons that switched from not pressed last frame to pressed this frame - or tests a single button.

### Usage
- `.pressed()` - Returns a list of pressed buttons.
- `.pressed(button)` - Returns a boolean representing the pressed status of the button
        - `button` - Button constant.

### Returns
A list of button constants if no parameter was specified, otherwise a boolean.

## released()
Returns a list of buttons released during the current frame - that is, buttons that switched from pressed last frame to not pressed this frame - or tests a single button.

### Usage
- `.released()` - Returns a list of released buttons.
- `.released(button)` - Returns a boolean representing the released status of the button
        - `button` - Button constant.

### Returns
A list of button constants if no parameter was specified, otherwise a boolean.

## held()
Returns a list of all buttons that are currently held down, or tests a single button.

### Usage
- `.held()` - Returns a list of held buttons.
- `.held(button)` - Returns a boolean representing the held status of the button
        - `button` - Button constant.

### Returns
A list of button constants if no parameter was specified, otherwise a boolean.

## changed()
Returns a list of all buttons whose state changed between the last frame and the current frame, or tests a single button.

### Usage
- `.changed()` - Returns a list of changed buttons.
- `.changed(button)` - Returns a boolean representing the changed status of the button
        - `button` - Button constant.

### Returns
A list of button constants if no parameter was specified, otherwise a boolean.

### Example
> Note: Click on the emulator to allow it to capture input. Use the arrow keys and space on your keyboard to try the example out.

```python
last_event = None

while True:
  # true only when button A is newly pressed this frame
  if badge.pressed(BUTTON_A):
    last_event = "BUTTON A PRESSED!"

  # true continuously while button B is being held
  if badge.held(BUTTON_B):
    last_event = "BUTTON B HELD!"

  # true only if button C has been released this frame
  if badge.released(BUTTON_C):
    last_event = "BUTTON C RELEASED!"

  # true only if button UP has changed state this frame. Note that we are here using changed()
  # with no parameters and checking the returned list.
  if BUTTON_UP in badge.changed():
    last_event = "BUTTON UP CHANGED!"

  if last_event:
    screen.pen = color.white
    screen.text(last_event, 10, 10)

  badge.update()
```

# Program flow
The functions in this section are for use if you're 'rolling your own' software without the use of Badgeware's app and menu system.

## screen.update()
This method is on the `screen` image rather than in `badge`, but is listed here for completeness. This will take the current contents of the `screen` image, and update the physical display. Used if you are creating your own program loop without using the `update()` ecosystem and instead creating your own program loop - if you're working within the Badgeware menu system, `screen.update()` is called automatically every update and you don't need to use this.

### Returns
None

## clear()
This resets the framebuffer, clearing the `screen` image to the colour specified by `badge.default_clear()` and setting `screen.pen` to the colour specified in `badge.default_pen()`. If the former is set to `None` the screen will not be cleared.

### Returns
None

## poll()
If you are creating your own program without the use of the Badgeware menu and app system, you will need to poll the badge using this method to get updated status on the buttons and other features. If you're working within the Badgeware menu system, `badge.poll()` is called automatically every update and you don't need to use this.

### Returns
None

## update()
This is a convenient method which simply runs `screen.update()`, `badge.clear()` and `badge.poll()` together.

### Returns
None

# Battery status
Badgeware includes several methods to allow you to monitor the battery.

## battery_level()
Returns an int representing the battery level as a percentage from 0 to 100.

## battery_voltage()
Returns a float representing the current battery voltage.

## usb_connected()
Returns a boolean reflecting whether the USB cable is currently connected.

## is_charging()
Returns a boolean reflecting whether the battery is currently charging.

# Graphics

## default_clear
An attribute holding the colour the display will be cleared to before each `update()` loop, for example `badge.default_clear = color.black`. Set it to `None` to disable clearing the screen between updates.

## default_pen
An attribute holding the colour that `screen.pen` will be set to at the start of every `update()`, for example `badge.default_pen = color.white`. This will not accept `None`, only a colour.

## mode()
Gets or changes the display mode of the badge. Called with no arguments it returns the current mode; called with a mode it switches to it. You can apply more than one mode at once, where applicable, by using the pipe symbol, e.g. `badge.mode(HIRES | VSYNC)`.

### Usage
- `.mode()` - Returns the current display mode.
- `.mode(modes)`
        - `LORES` (Tufty only) - puts the badge into 160x120 low resolution mode.
        - `HIRES` (Tufty only) - puts the badge into 320x240 high resolution mode.
        - `VSYNC` (Tufty only) - enables vertical sync, preventing screen tearing.
        - `FAST_UPDATE` (Badger only) - sets the badge to update quickly at the cost of slight ghosting
        - `FULL_UPDATE` (Badger only) - sets the badge to update fully each time at the cost of speed.
        - `MEDIUM_UPDATE` (Badger only) - a middle ground between the above two.
        - `DITHER` - applies an ordered dither to the framebuffer before writing to the screen, equivalent to running [dither()](/api/image.md#dither) after every update. Available on all models, but most useful for Badger.

### Returns
The current mode when called with no argument, otherwise `None`.

# Memory
These methods monitor the badge's flash space and RAM, so you can check how full your Badge is with software and assets.

## disk_free()
### Usage
- `.disk_free()`
    - Returns a tuple containing total flash size, used flash and free flash in bytes for the `/system` mountpoint.
- `.disk_free(mountpoint)`
    - Returns as above, but for the specified mountpoint. Defaults to `/system`.

### Returns
A tuple of three ints: `(total, used, free)` in bytes.

## free()
Prints to console the amount of free RAM, prepended with the message if specified.

> Note: `free()` is a global helper, not part of the `badge` class, so you call it as `free()` — with no `badge.` prefix. See [helpers](/api/helpers.md#free) for details.

# Lighting
Badgeware is fitted with four onboard white LEDs on the back of the board. These can be used as indicators, decoration or anything else you can think of. Tufty also has a front-mounted light sensor.

## caselights()
Gets and sets the brightness value for the rear lighting on the badge.

### Usage
- `.caselights()` - Returns the current level of the rear LEDs as a tuple.
- `.caselights(level)`
        - `level` - Brightness to set on all rear LEDs (0-1)
- `.caselights(level1, level2, level3, level4)`
        - `level1`, `level2`, `level3`, `level4` - Brightness to set for each rear LED individually (0-1)

### Returns
`None`, or a tuple if no parameter specified.

## light_level() [TUFTY ONLY]
Returns the level detected by the front light sensor as a raw u16 value (0–65535). Only Tufty has a light sensor — calling this on Badger or Blinky raises a `RuntimeError`.

# Sleep and waking
Badgeware has the ability to go into a very low power mode, conserving battery power for a very long time. These are the basic commands to deal with this; other commands to deal with timings can be found in the `rtc` article.

## sleep()
Forces the badge into sleep mode. This will lose data contained in RAM, and will act as a reset on wakeup, restarting main.py and, on the default firmware, returning the user to the menu.

### Usage
- `.sleep()`
    - Puts the badge into sleep mode indefinitely.
- `.sleep(duration)`
    - Puts the badge into sleep mode, to awaken after `duration` seconds.

## woken_by_button()
Returns True if the badge was woken up by a button being pressed, False otherwise.

## woken_by_reset()
Returns True if the badge was woken by being reset, False otherwise.

## wake_reason()
Returns a value describing why the badge last woke from sleep. Use the helpers `woken_by_button()` and `woken_by_reset()` for the common cases, or compare this value yourself for finer control.

## pressed_to_wake()
Tests whether a specific button was the one held down that woke the badge from sleep. Useful for offering different behaviour depending on which button the user pressed to wake the device.

### Usage
- `.pressed_to_wake(button)`
    - `button` - A button constant such as `BUTTON_A`.

### Returns
`bool`

# Reference

## Constants
```python-raw
BUTTON_A: input
BUTTON_B: input
BUTTON_C: input
BUTTON_UP: input
BUTTON_DOWN: input
BUTTON_HOME: input
LORES: binary
HIRES: binary
VSYNC: binary
FAST_UPDATE: binary
FULL_UPDATE: binary
MEDIUM_UPDATE: binary
DITHER: binary
```

## Properties
```python-raw
badge.default_clear: color | None
badge.default_pen: color
badge.resolution: tuple
badge.model: string
badge.ticks: int
badge.ticks_delta: int
badge.uid: hex
```

## Methods
```python-raw
badge.battery_level() -> int
badge.battery_voltage() -> float
badge.changed() -> tuple
badge.changed(button: input) -> bool
badge.caselights() -> tuple
badge.caselights(level: float) -> None
badge.caselights(light1: float, light2: float, light3: float, light4: float) -> None
badge.clear() -> bool
badge.disk_free(mountpoint: string="/system") -> tuple
badge.held() -> tuple
badge.held(button: input) -> bool
badge.is_charging() -> bool
badge.light_level() -> int
badge.mode() -> int | None
badge.mode(modes: binary) -> None
badge.poll() -> None
badge.pressed() -> tuple
badge.pressed(button: input) -> bool
badge.pressed_to_wake(button: input) -> bool
badge.released() -> tuple
badge.released(button: input) -> bool
badge.sleep(duration: int=None) -> None
badge.update() -> bool
badge.usb_connected() -> bool
badge.wake_reason() -> int
badge.woken_by_button() -> bool
badge.woken_by_reset() -> bool
```

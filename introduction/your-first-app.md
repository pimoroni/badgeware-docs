---
title: Creating your first app
summary: Learn how to build a Badgeware app
icon:
sort: 3
---

# Creating your first app

Badgeware's default menu system makes it easy to create a new app. Each app is contained in its own folder. If you're using disk mode to copy files to Badgeware, that folder will be inside `/apps`. If you're connecting via Thonny or other IDEs, you'll find it under `/system/apps`, but we recommend using disk mode.

```bash
/apps
  /my_application
    icon.png
    __init__.py
    /assets
      ...
```

The home menu will detect each folder inside `/apps` as an app, as long as it has the minimum structure detailed below. If it does, it will automatically appear in the menu. The name given to it in the menu is the folder name, with automatic capitalisation and with underscores changed to spaces. For example, the app in the folder `my_application` would show up in the menu as "My Application".

Each application has a simple minimum structure:

- `icon.png` is the icon shown for your app in the main menu. It should be a 24x24 PNG image.
- `__init__.py` is the entry point of your app. It will run when your app is started from the menu and contains the main program loop of your app.
- `assets/` is a folder which will contain any assets such as image files that your app uses.

## Anatomy of __init__.py

There are certain things your `__init__.py` will need to work, and certain things which will be optional depending on what you wish to include in your app.

First you'll need to import relevant modules as in any Python program. Badgeware takes care of all the importing of system modules, and changes your working directory to your app's directory. Changing the working directory means that you can now import assets and other python files using paths relative to `__init__.py`, like so:

```bash
import my_module

my_image = image.load("assets/my_image.png")
```

That way you can keep all of your app's files in one folder, and easily move that folder from unit to unit or zip it if you want to share it.

Any code you write at the top level of `__init__.py` runs once when your app launches — this is where you set things up: import modules, load images and fonts, restore saved state, and set initial conditions.

After that comes the **main loop**. A Badgeware app runs a `while True:` loop that draws a frame and then calls `badge.update()`, which pushes your drawing to the display, clears the screen ready for the next frame, and reads the buttons. The loop runs endlessly until the program is ended, either by pressing the `HOME` button to return to the menu or by resetting the unit.

NOTE: Badger uses the loop in a slightly different way — it draws once and then sleeps. This is explained [here](/introduction/badge-differences.md).

One optional extra is an `on_exit()` function. If you define one, it's called when you leave the app by pressing the `HOME` button, and is the last thing that the program will do before closing — useful for saving state and so forth. Define it *before* your `while True:` loop (since the loop never falls through to code below it). Note that a power loss, like resetting the unit, going into disk mode or running out of battery, won't fire this function and data won't be saved.

```python
# example __init__.py for an application
import math

# select a font to use
screen.font = rom_font.nope

# called when you leave the app via HOME, to save state etc. (optional)
def on_exit():
  pass

# the main loop - runs until you press HOME or reset
while True:
  # clear the framebuffer to a dark blue
  screen.pen = color.rgb(20, 40, 60)
  screen.clear()

  # calculate and draw an animated sine wave
  y = (math.sin(badge.ticks / 100) * 20) + 80
  screen.pen = color.rgb(0, 255, 0)
  for x in range(160):
    screen.rectangle(x, y, 1, 1)

  # write a message
  screen.pen = color.rgb(255, 255, 255)
  screen.text("hello badge!", 10, 10)

  # push the frame to the display and read the buttons
  badge.update()
```

> Prefer to structure your app around a function instead? The [run()](/api/run.md) helper wraps exactly this loop — you write an `update()` function and call `run(update)`. It's what the built-in menu system uses, and it's handy when you want the loop to stop on a condition or after a set time.
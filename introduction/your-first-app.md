---
title: Creating your first app
summary: Learn how to build a Badgeware app
icon: shapes
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

The first optional element of your app is the `init()` method. This will run once automatically when your app is launched.

Anything you want to set up, such as loading in a saved state or setting initial conditions for the app, is performed here.

Next up is your `update()` method. This one forms the main program loop. `update()` will loop endlessly, until the program is ended either by pressing the `HOME` button to return to the menu or by resetting the unit. This is paired with `run(update)` at the very end of the code - this will start the loop when your app starts.

NOTE: Badger uses `update()` in a slightly different way. This is explained [here](/introduction/badge-differences.md).

Another optional method is `on_exit()`. This will be called when you leave the app by pressing the `HOME` button, and is the last thing that the program will do before closing, so it is useful for things like saving the program's state and so forth. Note that a power loss, like resetting the unit, going into disk mode or running out of battery, won't fire this method and data won't be saved.

```python
# example __init__.py for an application
import math

# select a font to use
screen.font = rom_font.nope

# called once when your app launches (optional)
def init():
  pass

# called every frame, do all your stuff here! (required!)
def update():
  # clear the framebuffer
  screen.pen = color.rgb(20, 40, 60)
  screen.clear()

  # calculate and draw an animated sine wave
  y = (math.sin(io.ticks / 100) * 20) + 80
  screen.pen = color.rgb(0, 255, 0)
  for x in range(160):
    screen.rectangle(x, y, 1, 1)

  # write a message
  screen.pen = color.rgb(255, 255, 255)
  screen.text("hello badge!", 10, 10)

# called before returning to the menu to allow you to save state (optional)
def on_exit():
  pass

run(update)
```
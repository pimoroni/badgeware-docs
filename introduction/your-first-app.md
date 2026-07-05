---
title: Creating your first app
summary: Turn the app you just wrote into a proper Badgeware app — installed on your badge, in the menu, with its own icon.
icon: shapes
publish: true
sort: 3
---

# Creating your first app

In the last guide you wrote some code and ran it straight from your editor — great for tinkering, but it lives on your computer. To turn it into a real Badgeware app — one that installs onto your badge, appears in the menu with its own icon, and launches like anything else — you just need to give it the right shape and copy it across. The code itself barely changes.

# What makes an app

An app is simply a **folder** inside `/apps`. Give it the right pieces and the badge finds it and adds it to the home menu automatically:

```bash
/apps
  /my_first_app
    __init__.py
    icon.png
    /assets
```

- **`__init__.py`** — your code; it runs when the app launches.
- **`icon.png`** — a 24×24 PNG shown next to the app in the menu.
- **`assets/`** — an optional folder for images, fonts and anything else the app needs.

The menu name comes from the folder name — underscores become spaces and each word is capitalised — so `my_first_app` becomes **My First App**.

Let's build one, straight onto the badge.

# 1. Enter disk mode

Plug your badge in over USB and **double-tap RESET**. It mounts on your computer as a USB drive named **TUFTY**, **BLINKY** or **BADGER** — that's the badge's filesystem, and it's where apps live.

Open it up and find the `/apps` folder.

# 2. Create your app folder

Inside `/apps`, make a new folder called `my_first_app`. Everything your app needs will live in here — which is also what makes an app easy to back up, move between badges, or zip up to share.

Remember, the folder name becomes the menu name, so this one will show up as **My First App**.

# 3. Add your code

Inside that folder, save your program as `__init__.py` — that exact name, because it's the file Badgeware runs when the app launches. It's the same script from the last guide, unchanged:

```python {static}
import time

screen.pen = color.white
screen.font = rom_font.smart

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

loading_screen()

items = ["Say hello", "Count sheep", "About"]
while True:
  choice = menu(items)
  show_item(choice)
```

# 4. Add an icon

Finally, drop an `icon.png` in next to `__init__.py`. The home menu is a grid of these icons — your icon *is* your app on screen, with the highlighted app's name shown in an overlay along the bottom. It's a **24×24 PNG**, so keep it bold and simple — one clear shape or a couple of letters reads far better than fine detail. Any image editor will do.

# 5. Launch it

Eject the drive and reset the badge. Your app is now in the home menu, icon and all — select it to launch, and press **HOME** to come back.

That's it — you've gone from a snippet in an editor to a real app living on your badge. 🎉

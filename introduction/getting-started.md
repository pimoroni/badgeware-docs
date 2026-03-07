---
title: "Getting Started"
summary: Get up and running with your first Badgeware app in minutes.
icon: rocket
publish: true
---
# Getting Started

Just got your badge? Let's get something on that screen. This quick guide will walk you through creating your very first app — from plugging in to seeing your code running. No prior experience with Badgeware is needed, just a basic familiarity with editing text files.

# What You'll Need

- Your Badgeware badge (Tufty, Badger, or Blinky)
- A USB-C cable
- A computer (any OS)
- A text editor — anything from Notepad to VS Code will do

# Step 1: Connect Your Badge

Plug your badge into your computer with the USB-C cable. To copy files onto it, you'll need to put it into Disk Mode:

- Press the **RESET** button on the back **twice** quickly
- The screen will show that it's in USB Disk Mode
- Your badge should appear as a drive on your computer (named BADGER, TUFTY, or BLINKY)

Open the drive and you'll see an `/apps` folder — this is where your code will live.

# Step 2: Create Your App Folder

Inside `/apps`, create a new folder called `hello`. This folder name becomes your app's name in the menu, so it will show up as "Hello".

Your app needs a minimum of two things:

- `__init__.py` — your code
- `icon.png` — a 24x24 pixel PNG icon for the menu

For now, you can grab a copy of `icon.png` from one of the other app folders on the badge. We'll focus on the code.

# Step 3: Write Your First App

Create a file called `__init__.py` inside your `hello` folder and open it in your text editor. Type in the following:

```python
def update():
    screen.pen = color.navy
    screen.clear()

    screen.pen = color.white
    screen.font = rom_font.smart
    screen.text("Hello, world!", 10, 50)

run(update)
```

Save the file. That's it — that's a complete Badgeware app!

# Step 4: Run It

Eject the badge drive safely from your computer. Your badge will reboot back to the menu. Navigate to your new "Hello" app and select it.

You should see a navy blue screen with "Hello, world!" written on it in white. Congratulations, you've just made your first app!

# What Just Happened?

Let's break down what that code does:

- **`def update():`** — This is the heart of every Badgeware app. The badge calls this method over and over in a loop, once per frame. Everything you want to draw goes in here.

- **`screen.pen = color.navy`** — Sets the drawing colour. Think of it like picking up a pen.

- **`screen.clear()`** — Fills the entire screen with the current pen colour.

- **`screen.pen = color.white`** — Switches to a new colour for the text.

- **`screen.font = rom_font.smart`** — Picks one of the 30+ built-in pixel fonts to write with.

- **`screen.text("Hello, world!", 10, 50)`** — Draws text at position x=10, y=50 on the screen.

- **`run(update)`** — This sits at the very end and tells the badge to start running your `update()` loop.

# Step 5: Make It Interactive

Now let's add a button press. We'll make the text change when you press a button:

```python
messages = ["Hello, world!", "Badgeware rocks!", "Press a button!"]
current = 0

def update():
    global current

    if badge.pressed(BUTTON_UP):
        current = (current + 1) % len(messages)

    screen.pen = color.navy
    screen.clear()

    screen.pen = color.white
    screen.font = rom_font.smart

    text = messages[current]
    width, _ = screen.measure_text(text)
    x = (screen.width / 2) - (width / 2)

    screen.text(text, x, 50)

run(update)
```

Save, eject, and run the app again. Each time you press the **Up** button, the message will cycle through the list. We're also centring the text on screen now by measuring its width first.

# Step 6: Add Some Colour

Let's make things a bit more visual by adding a coloured rectangle behind the text:

```python
messages = ["Hello, world!", "Badgeware rocks!", "Press a button!"]
current = 0

def update():
    global current

    if badge.pressed(BUTTON_UP):
        current = (current + 1) % len(messages)

    screen.pen = color.navy
    screen.clear()

    # draw a lighter rectangle as a banner
    screen.pen = color.rgb(60, 80, 120)
    screen.rectangle(rect(5, 40, screen.width - 10, 30))

    # draw the text centred inside the banner
    screen.pen = color.white
    screen.font = rom_font.smart

    text = messages[current]
    width, _ = screen.measure_text(text)
    x = (screen.width / 2) - (width / 2)

    screen.text(text, x, 45)

run(update)
```

Now your app has a banner with centred, cycling text — all in about 20 lines of code.

# Where To Go From Here

You've got the basics down. Here are some good next steps:

- **[Creating an App](your-first-app.md)** — Learn about the full app structure, including `init()` and `on_exit()` methods.
- **[Tutorial 1: A Simple Badge](tutorial_1.md)** — A longer, guided project that adds images, more text, and deeper interaction.
- **[The Hardware](hardware.md)** — Find out what's under the hood of your badge.
- **[Badge Differences](badge-differences.md)** — Understand how Tufty, Badger, and Blinky differ and how to code for each.
- **[Badge Modes](editing-on-device.md)** — Learn about Disk Mode, deep sleep, and firmware updates.

Once you're comfortable, dive into the **[Guides](/README.md#guides)** for features like sprites, vector shapes, animation, and more — or browse the **[API reference](/README.md#api)** when you need the details.

Happy hacking!

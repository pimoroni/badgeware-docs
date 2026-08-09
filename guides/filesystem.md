---
title: The filesystem
summary: Provides storage for apps, as well as the ability to read and write saved data from them.
icon: save
publish: true
---
# Using files

Reading and writing files on Badgeware works just like it does in standard Python. You open a file with the built-in `open()` function, read from or write to it, then close it again - and the tidiest way to do that is with a `with` block, which closes the file for you automatically:

```python-raw
# Write some text to a file
with open("/notes.txt", "w") as f:
    f.write("hello badge\n")

# Read it back
with open("/notes.txt", "r") as f:
    print(f.read())
```

The second argument to `open()` is the *mode*: `"r"` to read, `"w"` to write (replacing whatever was there), or `"a"` to append to the end of an existing file.

This is how your app keeps data between runs - the user's settings, a high score, a cached download, a screenshot. There's one catch: while your code is running it can only write to the root volume `/` (paths like `/notes.txt` above). The other volumes are read-only to Badgeware, as the [next section](#volumes) explains. Anything you save under `/` persists across resets, so it's the right home for settings, caches, save games and logs.

# Saving your app's data

Writing plain text is fine, but most of the time you'll want to save structured data - a dictionary of settings, a list of high scores, the state of a game. The `json` module makes this really handy: it turns Python objects like dictionaries and lists straight into text you can write to a file, and back again when you load them.

```python-raw
import json

settings = {"name": "Ada", "brightness": 80, "sound": True}

# Save the dictionary to a file
with open("/settings.json", "w") as f:
    json.dump(settings, f)

# Load it back later
with open("/settings.json", "r") as f:
    settings = json.load(f)

print(settings["brightness"])  # 80
```

`json.dump()` writes an object to an open file and `json.load()` reads it back. This works for anything made of the basic types - dictionaries, lists, strings, numbers and booleans - so it's a quick, readable way to keep an app's data between runs. It's worth wrapping the load in a `try`/`except` so a missing or empty file falls back to sensible defaults the first time your app runs:

```python-raw
defaults = {"name": "", "brightness": 100, "sound": True}

try:
    with open("/settings.json", "r") as f:
        settings = json.load(f)
except (OSError, ValueError):
    settings = defaults
```

# Volumes

Badgeware's 16MB of flash is split into a few separate storage areas, or *volumes*. Opening Badgeware in an IDE such as Thonny, you'll see three of them mounted as top-level folders:

| Folder | Holds | Writeable by |
| --- | --- | --- |
| `/` | Saved data and caches written by apps | Badgeware |
| `/system` | Apps, assets and your own `main.py` | The host, in disk mode |
| `/rom` | Built-in content, such as the bundled fonts | Nothing (read-only) |

The remaining flash is reserved for Badgeware's firmware and isn't visible as a folder. Each volume is described in more detail below.

> **Note:** Editors like Thonny don't write to these volumes the way the host does in disk mode - they hand files to Badgeware and let *it* do the writing. Because of that, they follow the same rules as your own code: they can write to `/`, but not to the read-only `/system` and `/rom` volumes.

## `/` — the writeable root

`/` is a 1MB LittleFS filesystem and the only volume your app can write to at runtime. Use it to save settings, cache data, or keep anything you need to persist across resets (and firmware updates), as shown in [Using files](#using-files) above.

## `/system` and disk mode

`/system` is a 12MB FAT filesystem, and it's the only volume the host computer can write to. When Badgeware is connected in **disk mode** it appears as a USB drive (labelled after your device, such as `TUFTY`, `BADGER` or `BLINKY`), and you can add, remove, rename and edit files freely. No filesystem is perfect, so always keep an off-device backup of anything you're working on.

Importantly, `/system` is **read-only to code running on Badgeware**. The host can change it over USB in disk mode, but an app cannot write to its own folder at runtime. This split keeps the user software safe from corruption while a program is running.

## `/rom`

`/rom` is a genuinely read-only, 1MB volume baked into the firmware. It holds the built-in fonts that apps can load without shipping their own font files. Neither Badgeware nor the host can write to it.

# Limitations

Flash storage on Badgeware is small and works a little differently to a hard drive or SD card. None of this is anything to worry about - you just get better results if you keep a few things in mind while designing your app.

- **Space is tight, and it's shared.** The writeable `/` volume is only 1MB, and *every* app on Badgeware shares it. Treat it as a communal cupboard rather than your own room: clean up files you no longer need, and avoid logging or caching without some sort of upper limit.

- **Files are stored in 4KB blocks.** LittleFS hands out storage one 4KB block at a time, and a file always takes at least one whole block - so even a 10-byte file costs 4KB. With a 1MB volume that works out to around **256 blocks in total** (a little fewer once the filesystem's own bookkeeping is taken into account), which means you can only ever have a couple of hundred files, no matter how small they are. The *number* of files matters just as much as their total size. Where you can, gather lots of little pieces of data into one file - a single JSON file, say, rather than one per item.

- **Use efficient file formats.** With both space and block count limited, compact assets go a long way. Store images at the resolution you'll actually display them at, reach for binary or packed formats over verbose text where it makes sense, and strip out anything you don't need before copying it across to Badgeware.

- **Flash wears out (eventually).** Flash memory can only be rewritten so many times. You're very unlikely to hit this in normal use, but it's a good reason not to rewrite the same file in a tight loop - buffer your data in memory and save it every now and then, rather than on every frame or sensor reading.

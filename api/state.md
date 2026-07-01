---
title: State
summary: Save and load small pieces of app data to flash so they survive resets, sleep and power-off.
icon: save
publish: true
---
# Introduction
`State` gives your app a simple way to remember things between runs. Because a badge often sleeps or resets between uses — and always loses RAM when it does — anything you want to keep (a high score, a settings choice, the last screen the user was on) needs to be written to flash. `State` handles that for you as JSON.

Each app stores its state under its own name, so different apps won't clobber each other's data. State is stored as a JSON file at `/state/<app>.json`, which means your data must be JSON-serialisable — dictionaries, lists, strings, numbers and booleans are all fine.

`State` is available globally, so there's no need to import it.

# Methods

## save()
Saves a dictionary of data for the named app, replacing anything previously stored. The `/state` directory is created automatically the first time you save.

### Usage
- `State.save(app, data)`
    - `app`: A name for your app, used as the storage key.
    - `data`: A JSON-serialisable dictionary to save.

### Returns
`None`

## load()
Loads previously saved data for the named app into a `defaults` dictionary. Pass a dictionary of default values; any saved values are merged in on top, so keys you've added since the data was saved keep their defaults. If no state exists yet, the defaults are saved as the starting state.

### Usage
- `State.load(app, defaults)`
    - `app`: The app name the data was saved under.
    - `defaults`: A dictionary of default values. Updated in place with any saved values.

### Returns
`True` if saved data was found and loaded, otherwise `False`.

## modify()
A convenience method that loads the current state, updates it with the supplied values, and saves it again. Use this when you only want to change a few keys without rewriting the whole state.

### Usage
- `State.modify(app, data)`
    - `app`: The app name.
    - `data`: A dictionary of values to merge into the saved state.

### Returns
`None`

## delete()
Deletes the saved state for the named app. Does nothing if there's no state to delete.

### Usage
- `State.delete(app)`
    - `app`: The app name whose state should be removed.

### Returns
`None`

### Example
```python
# start from defaults, then load any saved values on top
state = {"count": 0}
State.load("counter", state)

while True:
  # bump the counter each time A is pressed and persist it
  if badge.pressed(BUTTON_A):
    state["count"] += 1
    State.save("counter", state)

  screen.pen = color.white
  screen.font = rom_font.more
  screen.text(f"{state['count']}", 60, 45)

  screen.font = rom_font.sins
  screen.text("Press A to count", 30, 100)

  badge.update()
```

# Reference

## Static Methods
```python-raw
State.save(app: string, data: dict) -> None
State.load(app: string, defaults: dict) -> bool
State.modify(app: string, data: dict) -> None
State.delete(app: string) -> None
```

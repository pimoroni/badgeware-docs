---
title: The Filesystem
summary: Provides storage for apps, as well as the ability to read and write saved data from them.
icon: disc
publish: true
---
# Introduction

The Badgeware file system is fairly simple - opening it in an IDE such as Thonny, you can see that there's a `rom` folder containing the built-in read only content accessible by apps, a `state` folder that contains saved data from all apps, and a `system` folder containing the user software on the device. It is this `system` folder which is mounted as a USB drive when the badge is connected in disk mode.

In disk mode, you can alter files in `system` however you want, adding, removing, renaming and opening/editing/saving them directly from their folder - although remember, no filesystem is perfect and you should always keep an off-device backup of your work if you're working directly on the device. You can also upload and download files from the other folders in Thonny and similar editors, but you cannot save files directly to the device there - in this aspect it is kept read-only to prevent file corruption.

# Loading and Saving at runtime
That's all very well for you to create and edit your programs on Badgeware, but what about the programs saving and loading their own data? It might be to remember the user's settings between different runs, it might be for logging data, taking screenshots or for saved games, but data needs to be saved.

During runtime, everything in `/system/` is read-only, so you cannot save data into your app folder. However, `/state/` is accessible, and the usual MicroPython file reading and writing methods will work in this folder. However, there is another way to store simple data quickly and conveniently:

# The State module
The `State` module is a quick way of writing JSON data to a reserved area of the unit's flash, and load it back in as variables. It's useful for small pieces of data that need to persist in between restarts of the program - often just settings or preferences, but in the case of Badger, where the program might often sleep and restart between every update, you might need to retain data such as a previous set of values to add new data to, or the player's current position in the level.

## State.save()
This is used to simply save the state. It takes a dictionary, which will be saved in JSON form in the `state` folder.

### Usage
- `State.save(app_name, data)`
	- `app_name` - The name of the JSON file to output. This can be found in `/state/`.
	- `data` - The data to save, in the form of a dictionary. This dictionary can include any basic types.

### Returns
`None`.

## State.load()
This writes the data from the specified save file into the specified dictionary. It's a sensible idea to create the dictionary first containing default values, then overwrite the data using `State.load()`, in case there is no saved state file to load from. If there is no saved state, the default values will be kept and a save state will be created using the current data in the target dictionary.

### Usage
- `State.load(app_name, dictionary)`
	- `app_name` - The name of the JSON file to load. This can be found in `/state/`.
	- `dictionary` - The dictionary into which to place the loaded data.

### Returns
`True` if data was loaded successfully, otherwise `False`.

## state.delete()
This deletes the specified JSON file. Next time `State.load()` is used, it will revert to defaults as described above.

### Usage
- `State.load(app_name)`
	- `app_name` - The name of the JSON file to delete. This can be found in `/state/`.

### Returns
`None`.
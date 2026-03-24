---
title: Badge modes
summary: Put your badge into Disk mode to make transferring files easy
icon: function
---

# Putting your badge into Disk mode

The easiest way to edit the code on the device is to put it into mass storage mode:

- Connect your badge to your computer via a USB-C cable
- Press the **RESET** button twice
- The USB Disk Mode screen will appear
- The badge should appear as a disk named "BADGER" on your computer

In this mode you can see the contents of the FAT32 `/system/` mount. This is where all your application code should live.

# Running your code

There are two ways to run your code:

- Save it as `main.py` and it'll run when the badge starts up
- Create a [complete app](/introduction/your-first-app.md)

# Deep sleep

To put your badge to sleep, press and hold the **RESET** button on the back until the lights turn off.

In sleep mode your badge will sip battery power. In fact it will last for over 100 days, but it'll be ready to go at the press of any front button.

# Firmware update

To update your firmware:

- Connect your badge to your computer via a USB-C cable
- Hold down the **BOOT** button
- Tap **RESET**
- The badge should appear as a disk named "RP2350" on your computer
- Drag and drop the new firmware (`.uf2` file) onto this disk
- Your badge should reboot into the new firmware

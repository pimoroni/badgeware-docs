---
title: Update Your Firmware
summary: Keep your badge up to date with the latest Badgeware firmware.
icon: download
publish: true
---

> **Back up your code! The new firmware update will rebuild the filesystem on your badge!**

# Update Your Firmware

Before you start coding, make sure your badge is running the latest firmware. New releases include bug fixes, performance improvements, and new features — if something isn't working the way the docs describe, an outdated firmware is often the reason.

## Latest Release: v2.0.1 (28th February 2026)

This release fixes FAT filesystem corruption, vector rendering clipping, image blitting overflow, and power consumption during sleep mode. It also introduces the new `badge` module which replaces the previous `io` module with expanded functionality.

Download the correct firmware for your badge:

- **Badger:** [badger-v2.0.1-micropython-with-filesystem.uf2](https://github.com/pimoroni/badger2350/releases/download/v2.0.1/badger-v2.0.1-micropython-with-filesystem.uf2)
- **Tufty:** [tufty-v2.0.1-micropython-with-filesystem.uf2](https://github.com/pimoroni/tufty2350/releases/download/v2.0.1/tufty-v2.0.1-micropython-with-filesystem.uf2)
- **Blinky:** [blinky-v2.0.1-micropython-with-filesystem.uf2](https://github.com/pimoroni/blinky2350/releases/download/v2.0.1/blinky-v2.0.1-micropython-with-filesystem.uf2)

## How to Update

### Step 1: Back Up Your Code

Since the firmware update rebuilds the filesystem, any apps or files on your badge will be erased. Put your badge into Disk Mode (double-tap **RESET**), then copy your `/apps` folder to your computer.

### Step 2: Enter Bootloader Mode

- Connect your badge to your computer with a USB-C cable
- Hold down the **BOOT** button on the back of the badge
- While holding **BOOT**, tap the **RESET** button
- Release **BOOT** — your badge should appear as a drive called **RP2350**

### Step 3: Flash the Firmware

- Drag and drop the `.uf2` file you downloaded onto the **RP2350** drive
- Your badge will automatically reboot into the new firmware

The whole process takes a couple of minutes.

### Step 4: Restore Your Code

Once the badge has rebooted, go back into Disk Mode (double-tap **RESET**) and copy your apps back onto the badge.

## Troubleshooting

- **The RP2350 drive doesn't appear?** Make sure you're holding **BOOT** before you tap **RESET**. Hold BOOT first, then tap RESET, then release BOOT.
- **Badge isn't responding at all?** Try a different USB-C cable. Some cables are charge-only and don't carry data.

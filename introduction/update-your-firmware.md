---
title: Firmware updates
summary: Keep your badge up to date with the latest Badgeware firmware.
icon: save
publish: true
---

# Update your firmware

Before you start coding, it's worth making sure your badge is running the latest firmware. New releases bring bug fixes, performance improvements and new features. If something isn't behaving the way the docs describe, out-of-date firmware is a common culprit.

# Latest firmware

Grab the build for your badge below — these links come straight from our GitHub releases, so they're always the current version:

```firmware
```

> **Back up your code first!** Updating the firmware resets the badge's filesystem, so anything stored on it will be wiped — save a copy of any code you want to keep before you start.

# How to update

### 1. Back up your code

The update resets the filesystem, so everything on the badge will be erased. Put the badge into disk mode (double-tap **RESET**) and copy out any of *your own* apps or files that you want to keep. No need to save the built-in apps — the update ships fresh versions of those, so grabbing the whole `/apps` folder would only overwrite them with older copies later.

### 2. Enter bootloader mode

- Connect the badge to your computer with a USB-C cable.
- Hold down the **BOOT** button on the back of the badge.
- Keeping **BOOT** held, tap **RESET**, then release **BOOT**.
- The badge appears as a drive called **RP2350**.

### 3. Flash the firmware

- Drag the `.uf2` file you downloaded onto the **RP2350** drive.
- The badge flashes it and reboots into the new firmware automatically.

The whole thing takes a couple of minutes.

### 4. Restore your code

Once it's rebooted, go back into disk mode (double-tap **RESET**) and copy your own apps and files back into `/apps`.

> If one of your apps misbehaves after updating, it may be leaning on something that changed in the new firmware. Have a look at the release notes above and tweak your code to match.

# Troubleshooting

- **No RP2350 drive?** Make sure you hold **BOOT** *before* tapping **RESET** — hold BOOT, tap RESET, then release BOOT.
- **Badge not responding at all?** Try a different USB-C cable; some are charge-only and don't carry data.

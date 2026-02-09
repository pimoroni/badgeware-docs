---
title: Framebuffer
summary: A working canvas where you build up the screen image before copying it to the display.
sort: 1
icon: screenshot_monitor
publish: false
---

# Working with the screen

The framebuffer is a 160 × 120 true colour `Image` named `screen`. [Click here for full documentation of the `Image` class](api/image.md).

Your application can draw to the screen during the update() function.
After your code finishes executing, the badge automatically pixel-doubles the framebuffer to fit the display.

The screen supports drawing vector shapes, blitting other images, and rendering text using pixel fonts.

---
title: Keeping time
summary: Measure elapsed time for animations and timing, and keep the real date and time using Badgeware's clocks, alarms and NTP.
icon: timer
---

# Time on Badgeware

There are two quite different questions you might be asking about time:

- **How much time has passed?** - for animating things, timing events, or keeping movement smooth. This is handled by Badgeware's *system clocks*, which count up from when it was powered on.
- **What is the actual date and time?** - for a clock, a calendar, or timestamping data. This is handled by two *real-time clocks* that track the wall-clock time and date.

We'll look at each in turn.

# Measuring elapsed time

Most apps only care about *how much* time has passed - how long an animation has been running, or how much time went by since the last frame. The easiest way to get this is from the `badge` object, which samples the clock once per frame so every part of your `update()` sees a consistent value.

`badge.ticks`\
The number of milliseconds since Badgeware was powered on, as of when the current frame started. Handy as a steadily increasing value to drive animations and blinking.

`badge.ticks_delta`\
The number of milliseconds that passed since the *previous* frame. This is the key to smooth, frame-rate independent movement (see below).

```python-raw
# Blink something twice a second
blink = round(badge.ticks / 250) % 2 == 0

# A value that gently oscillates over time, for bobbing or pulsing
wobble = math.sin(badge.ticks / 250)
```

## Frame-rate independence

Badgeware won't always render at exactly the same rate, so if you move something by a fixed amount every frame it'll speed up and slow down as the framerate changes. Instead, multiply by `ticks_delta` to move by an amount of time rather than an amount of frames:

```python-raw
SPEED = 60  # pixels per second

def update():
    # ticks_delta is in milliseconds, so divide by 1000 to get seconds
    x += SPEED * (badge.ticks_delta / 1000)
```

However fast or slow Badgeware is drawing, the object now moves at a steady 60 pixels per second.

## Lower-level timers

If you need finer control than the per-frame values, MicroPython's built-in `time` module is available:

- `time.ticks_ms()` - milliseconds since power on, as a live reading rather than the per-frame `badge.ticks`.
- `time.ticks_us()` - the same in microseconds, for timing short operations.
- `time.time_ns()` - the current time in nanoseconds.

The `ticks_ms()` and `ticks_us()` counters wrap back around to zero when they overflow, so don't subtract them directly - use `time.ticks_diff()` to get a correct difference:

```python-raw
import time

start = time.ticks_ms()
do_something_slow()
elapsed = time.ticks_diff(time.ticks_ms(), start)  # milliseconds taken
```

# The real date and time

Badgeware has **two** real-time clocks working together:

- **The RP2350's internal clock.** This is part of the main chip and keeps the date and time while Badgeware is powered. It's what MicroPython's `time` module reads from, but it loses track the moment power is removed.
- **The onboard RTC.** This is a separate low-power chip (a PCF85063A) with its own backup power, so it keeps time through sleep and even when Badgeware is switched off, as long as there's charge left in the battery. It can also wake Badgeware with alarms and timers.

The two are kept in sync automatically. When Badgeware starts up, it copies the time from whichever clock has a sensible value into the other, so the battery-backed onboard RTC effectively restores the correct time to the main chip after Badgeware has been off.

You reach the onboard RTC through the global `rtc` object, which is always available in your apps.

## Reading and setting

`rtc.datetime()`\
Called with no arguments, returns the current date and time as a tuple:

```python-raw
year, month, day, hour, minute, second, dow = rtc.datetime()
```

`dow` is the day of the week. Pass the same shape of tuple in to *set* the clock:

```python-raw
# Set the clock to 2026-07-13, 14:30:00
rtc.datetime((2026, 7, 13, 14, 30, 0, 0))
```

`rtc.localtime_to_rtc()`\
Copies the RP2350's current time into the onboard RTC. Use this after setting the system time so the battery-backed clock keeps the new value.

`rtc.rtc_to_localtime()`\
The reverse - copies the onboard RTC's time back into the RP2350's internal clock.

## Alarms and timers

The onboard RTC can raise an alarm at a future time, which is useful for waking Badgeware from sleep or triggering something at a set moment.

`rtc.set_alarm(hours=0, minutes=0, seconds=0)`\
Sets an alarm to go off after the given amount of time from now. The parameters are all optional, but pass at least one.

`rtc.alarm_status()`\
Returns `True` once the alarm has fired, `False` otherwise.

`rtc.clear_alarm()`\
Disables the alarm interrupt, clears the flag and unsets the alarm.

```python-raw
rtc.set_alarm(minutes=5)   # wake me in five minutes

# ...later...
if rtc.alarm_status():
    rtc.clear_alarm()
    # the alarm went off - do something
```

There's also a countdown timer, handy for repeating intervals:

`rtc.set_timer(seconds, enable_interrupt=True)`\
Starts a countdown of the given number of seconds.

`rtc.timer_elapsed()`\
Returns `True` if the timer has finished since you last checked, clearing the flag as it does.

## Syncing time with NTP

If Badgeware is connected to Wi-Fi, it can fetch the correct time from an internet time server (NTP) rather than having you set it by hand.

`rtc.time_from_ntp()`\
Fetches the current time over the network and writes it to both clocks. Requires a working Wi-Fi connection (see the [Networking guide](networking.md) for connecting).

```python-raw
rtc.time_from_ntp()
year, month, day, hour, minute, second, dow = rtc.datetime()
```

NTP provides the time in **UTC**, with no timezone or daylight-saving adjustment - if you need local time you'll have to apply your own offset after fetching it.

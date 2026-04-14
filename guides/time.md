---
title: Time
summary: Process the passing of time and scale changes your application state based on elapsed frame time.
icon: timer
---

## Timing

There are a number of ways of measuring time. As well as the RP2350's own RTC, there is a built in RTC on the badge which allows you to set alarms and the current time and date, which will persist through the badge's sleep cycle as long as there is charge left in the battery.

`badge.ticks`\
The number of ticks (milliseconds) since the badge was powered on when `update()` was called.

`badge.ticks_delta`\
The number of ticks (milliseconds) since the previous time `update()` was called. Useful for timing animations where the framerate isn't completely stable.

`alarm_status()`
Returns True if the alarm interrupt pin has been set, False otherwise.

`clear_alarm()`
Disables the alarm interrupts, clears the alarm flag and unsets the alarm.

`datetime()`
Gets or sets the current date and time. You can either call it without parameters to get the current date and time as a tuple of form `(year, month, day, hour, minute, second, dow)`, or pass in the same tuple to set the date and time.

`localtime_to_rtc()`
Copies the badge's local date and time to the RTC.

`rtc_to_localtime()`
Copies the RTC date and time to the badge's local date and time.

`set_alarm()`
Sets an alarm to trigger after the desired hours, minutes and seconds. These parameters are all optional, but at least one must be present.

`time_from_ntp()`
Sets the time from an online NTP server. Requires an internet connection.
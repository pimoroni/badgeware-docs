---
title: rtc
summary: Access to the Realtime Clock functions.
icon: build
publish: true
---

# Introduction

The Badgeware RTC is a realtime clock which will continue running while the unit is in sleep mode. It can be set to wake up the unit after a particular amount of time has elapsed.

# Methods

## alarm_status()
Returns True if the alarm interrupt pin has been set, False otherwise.

## clear_alarm()
Disables the alarm interrupts, clears the alarm flag and unsets the alarm.

## datetime()
Gets or sets the current date and time. This is stored as a tuple of form `(year, month, day, hour, minute, second, dow)`.

### Usage
- `rtc.datetime()` - Returns the current date and time as a tuple.
- `rtc.datetime(dt)` - Sets the RTC time to the provided date and time.
        - `dt` - Tuple containing the new date and time.

### Returns
A tuple if no parameters passed in, otherwise `None`

## localtime_to_rtc()
Copies the badge's local date and time to the RTC.

## rtc_to_localtime()
Copies the RTC date and time to the badge's local date and time.

## set_alarm()
Sets an alarm to trigger after the desired hours, minutes and seconds. These parameters are all optional, but at least one must be present.

### Usage
- `rtc.set_alarm(hours, minutes, seconds)`
        - `hours` - The desired hours to set the alarm for. Default 0.
        - `minutes` - The desired minutes to set the alarm for. Default 0.
        - `seconds` - The desired seconds to set the alarm for. Default 0.

### Returns
`None`

## time_from_ntp()
Sets the time from an online NTP server. Requires an internet connection.



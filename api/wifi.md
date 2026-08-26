---
title: wifi
summary: Connect Badgeware to a Wi-Fi network without the usual MicroPython boilerplate.
icon: wifi
publish: true
---

# Introduction

The `wifi` module handles connecting Badgeware to a wireless network. It wraps up the underlying MicroPython `network` calls - setting up the interface, connecting, retrying and timing out - so apps can get online in a couple of lines.

Connecting is non-blocking: calling `connect()` repeatedly both starts the attempt and moves it along, so your app can keep drawing while it waits. With no arguments, `connect()` reads `WIFI_SSID` and `WIFI_PASSWORD` from `secrets.py`.

For a walkthrough of getting online and making requests, see the [Networking guide](/guides/networking.md).

# Methods

## connect()
Attempts to connect to a Wi-Fi network, and reports whether the connection is up yet. Called with no arguments it uses the network details from `secrets.py`.

### Usage
`wifi.connect()` \
`wifi.connect(ssid, psk)` \
`wifi.connect(ssid, psk, timeout, retries)`

| Parameter | Type | Description |
|---|---|---|
| `ssid` | `str` | *Optional.* The network name. Defaults to `WIFI_SSID` from `secrets.py`. |
| `psk` | `str` | *Optional.* The network password. Defaults to `WIFI_PASSWORD` from `secrets.py`. |
| `timeout` | `int` | *Optional.* Seconds to wait for each connection attempt. Default 60. |
| `retries` | `int` | *Optional.* Number of times to retry before giving up. Default 5. |

### Returns
`True` if Badgeware is connected, otherwise `False`.

## is_connected()
Reports whether Badgeware is currently connected to a network.

### Returns
`True` if connected, otherwise `False`.

## status()
Gets the current connection status as a code paired with a human-readable description, useful for showing progress or diagnosing a failed connection.

### Returns
A `tuple` of `(status_code, description)`.

## disconnect()
Disconnects from the network and powers down the Wi-Fi interface. Turning Wi-Fi off when it isn't needed saves battery.

## ip()
Gets Badgeware's IPv4 address on the network. An alias for `ipv4()`.

### Returns
A `str` containing the IPv4 address, or `None` if not connected.

## ipv4()
Gets Badgeware's IPv4 address on the network.

### Returns
A `str` containing the IPv4 address, or `None` if not connected.

## ipv6()
Gets Badgeware's IPv6 address on the network.

### Returns
A `str` containing the IPv6 address, or `None` if not connected.

## subnet()
Gets the network's subnet mask.

### Returns
A `str` containing the subnet mask, or `None` if not connected.

## gateway()
Gets the network's gateway address.

### Returns
A `str` containing the gateway address, or `None` if not connected.

## nameserver()
Gets the network's DNS nameserver address.

### Returns
A `str` containing the nameserver address, or `None` if not connected.

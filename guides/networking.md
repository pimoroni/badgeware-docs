---
title: Getting online
summary: Connect Badgeware to Wi-Fi and get online, using the built-in wifi module to skip the usual boilerplate.
icon: cloud_sync
publish: true
---

# Getting online

Badgeware has Wi-Fi built in, so your apps can fetch data from the web, sync the time, or talk to other services. MicroPython gives you the full `network` stack if you want it, but Badgeware also includes a small `wifi` module that wraps up the fiddly boilerplate - setting up the interface, connecting, retrying and timing out - so most apps only need a couple of lines.

# Setting your Wi-Fi details

Rather than putting your network name and password in every app, Badgeware keeps them in one place: a `secrets.py` file. To edit it, put Badgeware into **disk mode** (tap `RESET` twice), open the drive that appears, and edit `secrets.py`:

```python-raw
WIFI_SSID = "my-network"
WIFI_PASSWORD = "super-secret-password"
REGION = "eu"     # your Wi-Fi region, e.g. us, eu, australia, nz
TIMEZONE = 0      # offset from GMT in hours, e.g. 0, 1, -7
```

The `wifi` module reads `WIFI_SSID` and `WIFI_PASSWORD` from here automatically. `REGION` and `TIMEZONE` are used by some apps (such as the clock) for regional and time handling. If you try to connect without filling these in, Badgeware will show a friendly reminder to go and edit `secrets.py`.

# Connecting to Wi-Fi

Connecting is done through the `wifi` module. Importantly, connecting **doesn't happen instantly** - it can take a few seconds. You kick off the connection with `wifi.connect()`, then call `wifi.tick()` repeatedly until it reports you're online:

```python-raw
import wifi

wifi.connect()                  # start connecting, using the details from secrets.py

while not wifi.is_connected():
    wifi.tick()                 # keep the attempt moving until we're online

print("Connected! IP address:", wifi.ip())
```

`wifi.connect()` starts the connection off, and `wifi.tick()` drives it along - handling retries and timeouts - so you call it in a loop until `wifi.is_connected()` returns `True`. With no arguments it uses the details from `secrets.py`, but you can also pass a network name and password directly, or tune the timeout and retry count - see the [`wifi` API reference](../api/wifi.md) for the full list of arguments.

Once you're finished with the network, `wifi.disconnect()` drops the connection and powers the radio down. It's worth doing when you no longer need to be online, since Wi-Fi uses a fair bit of battery. The module can also report the current connection status and your network addresses - the [API reference](../api/wifi.md) covers those too.

# Fetching data from the web

Once you're connected, you can make HTTP requests with the `requests` module, which works much like the popular library of the same name on desktop Python:

```python-raw
import requests

r = requests.get("https://api.example.com/data")
data = r.json()      # parse a JSON response into a dict/list
print(data)
```

Use `r.json()` for JSON responses, or `r.text` for plain text. It's a good idea to wrap requests in a `try`/`except` block, since anything can go wrong on a network:

```python-raw
try:
    r = requests.get(API_URL)
    data = r.json()
except (OSError, ValueError):
    data = None   # request failed or the response wasn't valid JSON
```

# Syncing the time

A common reason to get online is to set Badgeware's clock from an internet time server. The `rtc` object has this built in - see the [Time guide](time.md) for `rtc.time_from_ntp()` and working with the date and time.

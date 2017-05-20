#!/usr/bin/env python
from machine import Pin, I2C
from neopixel import NeoPixel
from network import WLAN, STA_IF
from ssd1306 import SSD1306_I2C
from urequests import get
from utime import sleep_ms
from writer import Writer
import Lato

# Connect to WiFi
sta_if = WLAN(STA_IF)
sta_if.active(True)
sta_if.ifconfig(('<IP>', '<NETMASK>', '<GATEWAY>', '<DNS>'))
sta_if.connect('<SSID>', '<PSK>')

# Display
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)

# LED
np = NeoPixel(Pin(14), 12)

def color(x, y, z):
    n = np.n
    for i in range(5 * n):
        for j in range(n):
            np[j] = (x, y, z)
            np[i % n] = (0, i, 0)
        np.write()
        sleep_ms(50)
	for i in range(np.n):
            np[i] = (x, y, z)
	np.write()

# Check for departures
def checkDepartures():
    oled.fill(0)
    departures = get('http://tripox.dk/dsb/index.php').json()

    name = departures[0]['name']
    direction = departures[0]['direction']
    time = departures[0]['time']
    cancelled = departures[0]['cancelled']

    line = 'Linje %s' % (name)
    wri2 = Writer(oled, Lato, False)
    wri2.printstring(line + '\n' + direction + '\n' + time)
    oled.show()

    if cancelled:
        color(255, 0, 0)
    else:
        color(0, 128, 0)

while True:
    checkDepartures()
    sleep_ms(60 * 1000)


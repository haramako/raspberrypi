from machine import Pin

import time

led = Pin(25, Pin.OUT)

while True:
    time.sleep(0.08) #1秒待機
    led.value(1)

    time.sleep(0.01) #1秒待機
    led.value(0)

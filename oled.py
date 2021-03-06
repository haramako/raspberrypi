from machine import SPI,Pin,Timer
from ssd1306 import SSD1306_SPI
import utime

import time
import framebuf
import random

"""
!!! From Raspberry Pi Pico Documentation
    **spi** is an SPI object, which has to be created beforehand and tells the ports for SCLJ and MOSI. MISO is not used.

    **dc** is the GPIO Pin object for the Data/Command selection. It will be initialized by the driver.

    **res** is the GPIO Pin object for the reset connection. It will be initialized by the driver. If it is not needed, it can be set to None or omitted. In this case the default value of None applies.

    **cs** is the GPIO Pin object for the CS connection. It will be initialized by the driver. If it is not needed, it can be set to None or omitted. In this case the default value of None applies.


# ------------ SPI ------------------ 
# Pin Map SPI 
# - VCC - xxxxxxx - Vcc 
# - GND - xxxxxxx - Gnd 
# - D0  - GPIO 10 - Clk / Sck fixed 
# - D1  - GPIO 11 - Din / MOSI fixed 
# - RES - GPIO 13 - Res
# - DC  - GPIO 14 - D/C 
# - CS  - GPIO 15 - CS (optional, if the only connected device) 


# - GPIO 16 - button 0
# - GPIO 17 - button 1
# - GPIO 18 - button 2
# - GPIO 19 - button 3
"""

spi = SPI(1, polarity=0, phase=0, bits=8, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
oled = SSD1306_SPI(128, 64, spi, res=Pin(13), dc=Pin(14), cs=Pin(15))

btn = [
 Pin(16, Pin.IN, Pin.PULL_UP),
 Pin(17, Pin.IN, Pin.PULL_UP),
 Pin(18, Pin.IN, Pin.PULL_UP),
 Pin(19, Pin.IN, Pin.PULL_UP),
]

btn_val = [1 for x in range(4)]
btn_pushed = [False for x in range(4)]

fb = framebuf.FrameBuffer(bytearray(8), 8,8, framebuf.MONO_VLSB)
for x in range(8):
    for y in range(8):
        fb.pixel(x,y, random.randint(0,1))

class StopWatch:
    def __init__(self):
        self.edit_sec = 0
        self.count = 0
        self.changed = True
        self.running = False
        self.start_at = None
        self.finish_at = None
        self.rest_sec = -1
        self.blink = False
        
    def update(self):
        if btn_pushed[0]:
            self.edit_sec += 60
            self.changed = True
        if btn_pushed[1]:
            self.edit_sec += 1
            self.changed = True
        if btn_pushed[2]:
            self.run()
            self.changed = True
        if btn_pushed[3]:
            self.running = False
            self.changed = True
        # Running stop watch
        if self.running:
            rest_sec = (self.finish_at - utime.ticks_ms() ) // 1000
            if self.rest_sec != rest_sec:
                self.rest_sec = rest_sec
                self.changed = True
            blink = ((self.finish_at - utime.ticks_ms() ) % 1000) > 500
            if blink != self.blink:
                self.blink = blink
                self.changed = True
        if self.changed:
            self.redraw(oled)
            self.changed = False

    def run(self):
        self.running = True
        self.start_at = utime.ticks_ms()
        self.finish_at = self.start_at + self.edit_sec * 1000
        
    def redraw(self, oled):
        self.count += 1
        oled.fill(0)
        #oled.text('Count {}'.format(self.count), 0, 0)
        min = self.edit_sec // 60
        sec = self.edit_sec % 60
        oled.text('{:3d}:{:02d}'.format(min, sec), 0, 8)
        # oled.text('{}'.format(utime.ticks_ms()), 0, 16)
        
        if self.running:
            min = self.rest_sec // 60
            sec = self.rest_sec % 60
            separator = ':' if self.blink else ' '
            oled.text('{:3d}{}{:02d}'.format(min, separator, sec), 0, 32)
        # oled.blit(fb, 0, 0)
        oled.show()
        
        
stop_watch = StopWatch()

def update_buttons():
    for n in range(4):
        v = btn[n].value()
        btn_pushed[n] = (btn_val[n] == 1 and v == 0)
        btn_val[n] = v
    
def on_timer(t):
    update_buttons()
    stop_watch.update()


print("start")

timer = Timer()
timer.init(period = 100, mode=Timer.PERIODIC, callback = on_timer)


#for b in btn:
#    b.irq(handler=on_timer, trigger=Pin.IRQ_FALLING)

# machine.lightsleep(3000)


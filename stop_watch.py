from machine import SPI,Pin,Timer
from ssd1306 import SSD1306_SPI

import math
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

fb = None

class StopWatch:
    def __init__(self):
        self.edit_sec = 180
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
        if btn_pushed[0] and btn_pushed[1]:
            self.edit_sec = 0
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
        
    def draw_font(self, oled, x, y, chr):
        if font[chr]:
            oled.blit(font[chr], x, y)
            
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
            blink = self.blink
        else:
            min = self.edit_sec // 60
            sec = self.edit_sec % 60
            blink = True
            
        if True:
            separator = ':' if self.blink else ' '
            self.draw_font(oled, 0, 16, min // 10)
            self.draw_font(oled, 24, 16, min % 10)
            if blink:
                self.draw_font(oled, 48, 16, 10)
            self.draw_font(oled, 72, 16, sec // 10)
            self.draw_font(oled, 96, 16, sec % 10)
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


print("load")

def read_font(path):
    with open(path, 'rb') as f:
        bin = f.read()
        w = bin[0]
        h = bin[1]
        return framebuf.FrameBuffer(bytearray(bin[2:]), w, h, framebuf.MONO_VLSB)

font = [read_font('font_{}.bin'.format(n)) for n in range(11)]

print('loaded')

print("start")
timer = Timer()
timer.init(period = 50, mode=Timer.PERIODIC, callback = on_timer)


#for b in btn:
#    b.irq(handler=on_timer, trigger=Pin.IRQ_FALLING)

# machine.lightsleep(3000)


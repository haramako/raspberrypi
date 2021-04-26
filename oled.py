from machine import SPI
from machine import Pin
from ssd1306 import SSD1306_SPI
import utime

"""
!!! From Raspberry Pi Pico Documentation
    **spi** is an SPI object, which has to be created beforehand and tells the ports for SCLJ and MOSI. MISO is not used.

    **dc** is the GPIO Pin object for the Data/Command selection. It will be initialized by the driver.

    **res** is the GPIO Pin object for the reset connection. It will be initialized by the driver. If it is not needed, it can be set to None or omitted. In this case the default value of None applies.

    **cs** is the GPIO Pin object for the CS connection. It will be initialized by the driver. If it is not needed, it can be set to None or omitted. In this case the default value of None applies.


# ------------ SPI ------------------ 
# Pin Map SPI 
# - 3v - xxxxxx - Vcc 
# - G - xxxxxx - Gnd 
# - D7 - GPIO 13 - Din / MOSI fixed 
# - D5 - GPIO 14 - Clk / Sck fixed 
# - D8 - GPIO 4 - CS (optional, if the only connected device) 
# - D2 - GPIO 5 - D/C 
# - D1 - GPIO 2 - Res

"""

spi = SPI(0, polarity=0, phase=0, bits=8, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
oled = SSD1306_SPI(128, 64, spi, res=Pin(13), dc=Pin(14), cs=Pin(15))

i = 0
while True:
    i += 1
    oled.fill(0)
    #oled.fill(1)
    oled.pixel(10,10,1)
    oled.text('Micropython {}'.format(i), 0, 0)
    oled.text('works fine!', 0, 10)
    oled.show()
    print(i)


led = machine.Pin(25, machine.Pin.OUT)

while True:
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)

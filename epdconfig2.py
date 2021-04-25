# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI 
import time

class RaspberryPi:
    # Pin definition

    def __init__(self):
        self.spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.RST_PIN = Pin(22)
        self.DC_PIN          = Pin(21)
        self.CS_PIN          = Pin(20)
        self.BUSY_PIN        = Pin(26)


    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def spi_writebyte2(self, data):
        self.spi.write(bytearray(data))

    def module_init(self):
        #self.GPIO.setmode(self.GPIO.BCM)
        #self.GPIO.setwarnings(False)
        self.RST_PIN.init(self.RST_PIN.OUT)
        self.DC_PIN.init(self.DC_PIN.OUT)
        self.CS_PIN.init(self.CS_PIN.OUT)
        self.BUSY_PIN.init(self.BUSY_PIN.IN)

        return 0

    def module_exit(self):
        # self.SPI.close()

        self.RST_PIN.value(0)
        self.DC_PIN.value(0)

        # self.GPIO.cleanup()


if __name__ == "__main__":
    implementation = RaspberryPi()
    print(1)

### END OF FILE ###

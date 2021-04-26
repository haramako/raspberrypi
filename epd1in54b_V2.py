# *****************************************************************************
# * | File        :	  epd1in54b.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
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

# Display resolution
EPD_WIDTH       = 200
EPD_HEIGHT      = 200


class Config:
    # Pin definition

    def __init__(self, spi, rst = None, dc = None, cs = None, busy = None):
        self.spi = spi
        self.RST_PIN = Pin(22)
        self.DC_PIN = Pin(21)
        self.CS_PIN = Pin(20)
        self.BUSY_PIN = Pin(26)


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

epdconfig = None

class EPD:
    def __init__(self, spi, rst = None, dc = None, cs = None, busy = None):
        global epdconfig
        epdconfig = Config(spi, rst, dc, cs, busy)
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT


    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, 0) # module reset
        epdconfig.delay_ms(5)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        #logging.debug("e-Paper busy")
        while(epdconfig.digital_read(self.busy_pin) == 1):
            epdconfig.delay_ms(100)    
        #logging.debug("e-Paper busy release")
        
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        
        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0xC7)
        self.send_data(0x00)
        self.send_data(0x01)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x01)

        self.send_command(0x44) #set Ram-X address start/end position   
        self.send_data(0x00)
        self.send_data(0x18)    #0x18-->(24+1)*8=200

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0xC7)    #0xC7-->(199+1)=200
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00) 

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x05)

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)

        self.send_command(0x4E)   # set RAM x address count to 0
        self.send_data(0x00)
        self.send_command(0x4F)   # set RAM y address count to 0X199    
        self.send_data(0xC7)
        self.send_data(0x00)
        self.ReadBusy()
        return 0

    def getbuffer(self, image):
        buf = [0xFF] * int(self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] == 0:
                    buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        return buf

    def display(self, blackimage, redimage):
        # send black data
        if (blackimage != None):
            self.send_command(0x24) # DATA_START_TRANSMISSION_1
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(~blackimage[i])
                
        # send red data        
        if (redimage != None):
            self.send_command(0x26) # DATA_START_TRANSMISSION_2
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(redimage[i])  

        self.send_command(0x22) # DISPLAY_REFRESH
        self.send_data(0xF7)
        self.send_command(0x20) # DISPLAY_REFRESH
        self.ReadBusy()

    def Clear(self):
        self.send_command(0x24) # DATA_START_TRANSMISSION_1
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
            
        self.send_command(0x26) # DATA_START_TRANSMISSION_2
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0x00)

        self.send_command(0x22) # DISPLAY_REFRESH
        self.send_data(0xF7)
        self.send_command(0x20) # DISPLAY_REFRESH
        self.ReadBusy()


    def sleep(self):
        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01) 

        epdconfig.delay_ms(2000)
        epdconfig.module_exit()


if __name__ == "__main__":
    spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    epd = EPD(spi, dc=Pin(21), rst=Pin(22), cs=Pin(20), busy=Pin(26))
    epd.init()
    
### END OF FILE ###


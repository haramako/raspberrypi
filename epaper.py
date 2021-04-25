from machine import Pin, SPI
from epd1in54b_V2 import EPD
import framebuf

buf = bytearray(int(200 * 200 / 8))
fbuf = framebuf.FrameBuffer(buf, 200, 200, framebuf.MONO_HLSB)

fbuf.rect(10,10,100,100,1)

print(1)
#spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
#epd = EPD(spi, dc=Pin(21), rst=Pin(22), cs=Pin(20), busy=Pin(26))
epd = EPD()
epd.init()
epd.display(buf, buf)
#epd.fill(0)
#epd.text('ESP8266', 0, 0)
#epd.text('Waveshare ePaper', 0, 10)
#epd.show()
print(2)
    
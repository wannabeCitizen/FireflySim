from neopixel import *
import time

def blink(strip):
    for i in range(255):
        for j in range(10):
            strip.setPixelColorRGB(j, 0, i, 0)
        time1 = time.time()
        strip.show()
        time2 = time.time()
        print "It took: {0}".format(time2 - time1)
    for i in range(255, 0, -1):
        for j in range(10):
            strip.setPixelColorRGB(j, 0, i, 0)
        print "It took: {0}".format(time2 - time1)
        strip.show()

if __name__ == "__main__":
    strip = Adafruit_NeoPixel(10, 18)
    strip.begin()
    while True:
        blink(strip)

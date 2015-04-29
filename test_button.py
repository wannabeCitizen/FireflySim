#!/usr/bin/python

import RPi.GPIO as GPIO
import time

last_press = 10
runny = True
counter = 0

def re_runner(pin):
    start = time.time()
    #global last_press
   # global runny
    global counter
    counter += 1
    print counter
    #if start - last_press > 4:
    #    last_press = start
   # else:
       # runny = False
       # print "\n\nWe're all done\n\n"
        
    #print "Killed it at {0}".format(time.time())



def run_test():
    global runny

    #Set GPIO mode to board layout, listening to pin 23 for a Falling Edge
    #Callback to re_runner function
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(21, GPIO.FALLING, re_runner, 500)

    while runny:
        make_words(1)
        time.sleep(1.5)

    GPIO.cleanup()


def make_words(x):
    global counter
    words = ["going {0}".format(counter), "grandma", "popsicle", "cheese", "siren", "quagmire", "troll", "medula ablingata", "Jesus"]
    for i in range(x):
        print words[i]


if __name__ == "__main__":
    run_test()

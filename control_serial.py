#!/usr/bin/python
import time
import sys
import serial
import array

import ff_sim as ffs

def runner(per_strip, strip, my_flies, port, t):
    #update state of all ffs
    my_flies1 = ffs.update_state(my_flies, t, strip, per_strip)

    #fill buffer
    r_val = []
    g_val = []
    for i in xrange(strip):
        for j in xrange(per_strip):
            r_val.append(my_flies1[i][j].brightnessR)
            g_val.append(my_flies1[i][j].brightnessG)
    
    #pass signal
    for i in r_val:
        port.write(chr(i))
    for j in g_val:
        port.write(chr(j))
        
    return my_flies1


#Expects to run with 2 arguments:
#num of strips and num of ff's per strip
if __name__ == '__main__':
    #Grab input arguments
    ff_num = int(raw_input("How many fireflies are on a strip?:  "))
    strip_num = int(raw_input("How many strips?:  "))
    stim_w = float(raw_input("Stimulus Period?:  "))
    A_min = float(raw_input("Minimum Reset Strength A?:  "))
    A_max = float(raw_input("Maximum Reset Strength A?:  "))
    w_min = float(raw_input("Minimum Period:  "))
    w_max = float(raw_input("Maximum Period?:  "))
    update_time = float(raw_input("What time step would you like to use? (takes about .003s to pass message):  "))
    t_up = float(raw_input("Blink up time?:  "))
    t_down = float(raw_input("Blink down time?:  "))

    #Create FF Agents
    FFs = ffs.make_ff_array(ff_num, strip_num, A_max, A_min, stim_w, w_max, w_min, update_time, t_up, t_down)


    #Set up serial port
    port = serial.Serial(port="/dev/ttyAMA0", baudrate=115200)
    port.open()
    port.flushOutput()
    #May eventually need a reset so that memory doesn't overflow
    #Start Running
    print "Press Ctrl-C to stop at any time"
    while True:
        FFs = runner(ff_num, strip_num, FFs, port, update_time)
        time.sleep(update_time)


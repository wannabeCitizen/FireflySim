#!/usr/bin/python
import numpy as np


class FireFly:
    
    # Firefly period is set in seconds
    def __init__(self, T, A):
        self.T = T
        self.w0 = ((2*np.pi)/T)
        self.wn = ((2*np.pi)/T)
        self.A = A
        self.theta = 0
        self.theta1 = -1
        self.blink = 0
        self.brightnessR = 0
        self.brightnessG = 0
        self.count = 0

    def next_state(self, t):
        self.theta1 = self.theta + self.wn * t
        if (np.sin(self.theta) < 0) and (np.sin(self.theta1) >= 0):
            self.blink = 1
            self.brightnessR = 1
            self.brightnessG = 1
        self.theta = self.theta1
        if self.blink == 1:
            self.count += 1
            self.brightnessR += .85
            self.brightnessG += .33
            if self.count  == 255:
                self.blink = 0
        elif (self.brightnessR > 0):
            self.brightnessR -= .51
            self.brightnessG -= .2
            if self.count == 510:
                self.count = 0
                self.brightnessR = 0
                self.brightnessG = 0
                

    def update(self, theta_stim):
        self.wn = self.wn + (self.A * np.sin(theta_stim - self.theta1))

#Expects number of FF's to evenly divide into strips
#This is because this is meant to work with LED or other lighting strips
#Thus, if you ask for more FF's than LEDs, we need to pitch a few (or do unnecessary computational work)
def make_ff_array(strip_length, num_strips, A_max, A_min, w_stim, w_max, w_min):
    ff_arrays = {}

    ff_arrays['stim'] = FireFly(w_stim, A_min)
    for i in xrange(num_strips):
        ff_strip = []
        for j in range(strip_length):
            _w = (np.random.random() * (w_max - w_min)) + w_min
            _A = (np.random.random() * (A_max - A_min)) + A_min

            next_ff = FireFly(_w, _A)
            ff_strip.append(next_ff)
        ff_arrays[i] = ff_strip
    return ff_arrays

def update_state(ff_array, t, num_strips, strip_length):
    phase1 = ff_array['stim'].theta
    ff_array['stim'].next_state(t)
    phase2 = ff_array['stim'].theta1
    for i in xrange(num_strips):
        for j in xrange(strip_length):
            ff_array[i][j].next_state(t)
    if (np.sin(phase1) < 0) and (np.sin(phase2) >= 0):
        for i in xrange(num_strips):
            for j in xrange(strip_length):
                ff_array[i][j].update(phase2)
    return ff_array

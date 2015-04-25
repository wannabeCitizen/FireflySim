#!/usr/bin/python
import numpy as np

class FireFly:
    
    # Firefly period is set in seconds
    def __init__(self, T, A):
        self.T = T
        self.w0 = ((2*np.pi)/T)
        self.wn = ((2*np.pi)/T)
        self.A = A
        self.theta = -np.pi
        self.theta1 = -np.pi
        self.blink = 0

    def next_state(self, t):
        if self.blink:
            self.blink = 0
        self.theta1 = self.theta + self.wn * t
        if (np.sin(self.theta) < 0) and (np.sin(self.theta1) >= 0):
            self.blink = 1
        self.theta = self.theta1                

    def update(self, theta_stim):
        self.wn = self.wn + (self.A * np.sin(theta_stim - self.theta1))

class FireFlyLock:
    
    # Firefly period is set in seconds
    def __init__(self, T, A, Tmin, Tmax):
        self.T = T
        self.w0 = ((2*np.pi)/T)
        self.wn = ((2*np.pi)/T)
        self.wmin = ((2*np.pi)/Tmin)
        self.wmax = ((2*np.pi)/Tmax)
        self.A = A
        self.theta = -np.pi
        self.theta1 = -np.pi
        self.blink = 0

    def next_state(self, t):
        if self.blink:
            self.blink = 0
        self.theta1 = self.theta + self.wn * t
        if (np.sin(self.theta) < 0) and (np.sin(self.theta1) >= 0):
            self.blink = 1
        self.theta = self.theta1                

    def update(self):
        self.wn = self.wn + (np.log(self.w0/self.wn)*.1) + ( max( np.sin(self.theta1), 0)*(self.wmin - self.wn) ) - ( min(np.sin(self.theta1), 0)*(self.wmax - self.wn) )

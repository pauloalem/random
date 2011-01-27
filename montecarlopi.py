# -*- coding: utf-8 -*-
import random
from rnd import *
from math import pow,sqrt

"""
Calculando pi usando metodo monte carlo
http://www.eveandersson.com/pi/monte-carlo-circle
"""

def calcPi(rng):
    hits = 0
    for i in xrange (0, 1000000):
        x = rng.random()
        y = rng.random()
        dist = sqrt(pow(x, 2)+pow(y, 2))
        if dist <= 1.0:
            hits = hits + 1.0

    # hits / i = 1/4 Pi
    pi = 4 * (hits / i)
    return pi


print calcPi(LinearCongruential())
print calcPi(ParkMiller())
print calcPi(MersenneTwister())

#Usando o modulo random da biblioteca padrao do python, que nada mais é do que um mersenne twister em C
print calcPi(random)

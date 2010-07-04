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
        x = random.random()
        y = random.random()
        dist = sqrt(pow(x, 2)+pow(y, 2))
        if dist <= 1.0:
            hits = hits + 1.0

    # hits / i = 1/4 Pi
    pi = 4 * (hits / i)

    print "pi = %s" %(pi)


calcPi(LinearCongruential())
calcPi(ParkMiller())
calcPi(MersenneTwister())

#Usando o modulo random da biblioteca padrao do python, que nada mais é do que um mersenne twister em C
calcPi(random.random)

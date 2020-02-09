# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:48:10 2020

@author: ZHEZH
"""

import math
import cmath

print("Here's the quation to be solved: a*x^2+b*x+c=0")
a, b, c = float(input("Please enter the value of a:")), float(input("Please enter the value of b:")), float(input("Please enter the value of c:"))

print()

d = b**2 - 4*a*c
if d==0:

    print("There's only one root:", -b/(2*a))
elif d>0:
    print("There're two real roots:", (-b + math.sqrt(d)) / (2*a), "and", (-b- math.sqrt(d)) / (2*a) )
elif d<0:
    print("There're two imaginary roots:", (-b + cmath.sqrt(d))/(2*a), "and", (-b - cmath.sqrt(d))/(2*a))


input("Press enter to exit")

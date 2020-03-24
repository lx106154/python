# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:48:10 2020

@author: ZHEZH
"""

import math
import cmath

# input the parameters for the quadric equation
print("Here's the quation to be solved: a*x^2+b*x+c=0")
x, y, z = float(input("Please enter the value of a:")), float(input("Please enter the value of b:")), float(input("Please enter the value of c:"))

# define a function to give the roots of equation
def quadric(a, b, c) :
    d = b ** 2 - 4 * a * c
    if d == 0:
        x1 = x2 = -b/(2 * a)
    elif d > 0:
        x1, x2 = (-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a)
    elif d < 0:
        x1, x2 = (-b + cmath.sqrt(d)) / (2 * a), (-b - cmath.sqrt(d)) / (2 * a)
    roots = [x1, x2]
    return roots

# use the quadric() funtion to find the roots
print("The roots of the quadric equation are", quadric(x, y, z)[0], "and", quadric(x, y, z)[1])

input("Press enter to exit")

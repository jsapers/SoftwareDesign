# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 23:34:37 2014

@author: ubuntu
"""

def fermatCheck(a,b,c,n):
    if a**n + b**n == c**n and n>2:
        print "Holy smokes, Fermat was wrong!"
    else:
        print "No, that doesn't work"

def fermatPrompt():
    a = int(raw_input("input a"))
    b = int(raw_input("input b"))
    c = int(raw_input("input c"))
    n = int(raw_input("input n"))
    fermatCheck(a,b,c,n)
            
fermatPrompt()

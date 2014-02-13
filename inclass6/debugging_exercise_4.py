# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 17:52:54 2014

@author: pruvolo
"""

def get_doubles_then_triples(L):
    """ Returns a new list containing the original list with each element
    	multiplied by 2 concatenated with the original list with each element
	multiplied by 3 """
    L1 = L
    L2 = L
    L1 = get_multiple_of_list(L1,2)
    L2 = get_multiple_of_list(L2,3)
    return L1 + L2

def get_multiple_of_list(L2,n):
    L2 = list(L2)
    for i in range(len(L2)):
        L2[i] *= n
    return L2

if __name__ == '__main__':
    print get_doubles_then_triples([1, 4, 8])

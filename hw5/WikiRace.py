# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/josh/.spyder2/.temp.py
"""

from bs4 import BeautifulSoup
import requests
import re
def getLinks(url):
    """
    Scans through article in wikipedia and finds all hyperlinked
    texts, then stores them inside a dictionary.
    
    Input: The article's URL
    Output: A dicsatellitetionary of all links in the page.
    """
    d={}
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data) 
    for link in soup.find_all('a'):
        l =link.get('href')
        if l != None:
            if l[0:6]=="/wiki/":
                if not(":"in l or "Main_Page"in l):
                    d[l[6:]]="http://en.wikipedia.org"+l
    return d
def compareLinks(start,prev,targetName,targetText):
    """
    Recursively compares the current link's words to the goal's
    words and selects the next article based similarity.
    
    Input: start (previous article) prev (list of all previous)
            targetName (the goal) targetText (the goal's words)
    Output: Name of preceding and next articles 
    """    
    d = getLinks("http://en.wikipedia.org/wiki/"+start)
    l= d.keys()
    print "\n\n"+start+"\n\n\n"     

    mostcommon=0
    for keys in d:
        if keys.lower() == targetName.lower():
            return keys
    if len(l)<100:
        max=len(l)
    else:
        max = 100
    for i in range(0,max):
        r  = requests.get(d[l[i]])
        data = r.text
        soup = BeautifulSoup(data) 
        text1 = soup.get_text()
        words = re.findall("[\w]+",text1)
        if targetName in words and not(l[i]in prev):
            prev.append(l[i])
            return l[i]+","+ compareLinks(l[i],prev,targetName,targetText)
        common = list(set(words) & set(targetText))
        if len(common)>mostcommon:
            if not(l[i]in prev):
                mostcommon = len(common)
                nextkey = l[i]
                prev.append(nextkey)
    return nextkey+","+ compareLinks(nextkey,prev,targetName,targetText)
    

def Navigate(start,end):
    """
    Main code, for starting the recursion.
    
    Input: start(beginning article) end(ending article (goal))
    Output: Prints path
    """    
    r1= requests.get("http://en.wikipedia.org/wiki/"+end)
    data1 = r1.text
    soup1 = BeautifulSoup(data1) 
    text1 = soup1.get_text()
    words = re.findall("[\w]+",text1)
    print compareLinks(start,[start],end,words)
    
start = raw_input("Start")
end = raw_input("end")
Navigate(start,end)
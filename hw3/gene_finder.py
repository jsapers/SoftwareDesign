# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Josh Sapers and Paul Ruvolo
(from replacement code for code lost)
"""

from numpy import argmax
from random import shuffle

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    retval = ""
    for i in range(0,len(dna),3):
        for j in range(len(codons)):
            if dna[i:i+3] in codons[j]:
                retval += aa[j]
                break
    return retval

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    print "input: ATGCGA, expected output: MR, actual output: " + coding_strand_to_AA("ATGCGA")
    print "input: ATGCCCGCTTT, expected output: MPA, actual output: " + coding_strand_to_AA("ATGCCCGCTTT")

def get_complementary_base(B):
    """ Returns the complementary nucleotide to the specified nucleotide. """
    if B == 'A':
        return 'T'
    elif B == 'C':
        return 'G'
    elif B == 'G':
        return 'C'
    elif B == 'T':
        return 'A'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    retval = ""
    for i in reversed(dna):
        retval += get_complementary_base(i)
    return retval
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
    print "input: ATGCCCGCTTT, expected output: AAAGCGGGCAT, actual output: " + get_reverse_complement("ATGCCCGCTTT")
    print "input: CCGCGTTCA, expected output: CCGCGTTCA, actual output: " + get_reverse_complement("CCGCGTTCA")

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    retval = ""
    for i in range(0,len(dna),3):
        if dna[i:i+3] in ['TAG', 'TAA', 'TGA']:
            break
        retval += dna[i:i+3]
    return retval

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    print "input: ATGTGAA, expected output: ATG, actual output: " + rest_of_ORF("ATGTGAA")
    print "input: ATGAGATAGG, expected output: ATGAGA, actual output: " + rest_of_ORF("ATGAGATAGG")
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    retval = []
    i = 0
    while i < len(dna):
        if dna[i:i+3] == 'ATG':
            retval.append(rest_of_ORF(dna[i:]))
            i += len(retval[-1])
        i += 3
    return retval

def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
    print "input: ATGCATGAATGTAGATAGATGTGCCC, expected output: ['ATGCATGAATGTAGA', 'ATGTGCCC'], actual output: " + str(find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC"))

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    return find_all_ORFs_oneframe(dna) + find_all_ORFs_oneframe(dna[1:]) + find_all_ORFs_oneframe(dna[2:])

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
    print "input: ATGCATGAATGTAG, expected output: ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG'], actual output: " + str(find_all_ORFs("ATGCATGAATGTAG"))

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """
    print "input: ATGCGAATGTAGCATCAAA, expected output: ['ATGCGAATG', 'ATGCTACATTCGCAT'], actual output: " + str(find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA"))
    # YOUR IMPLEMENTATION HERE

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""
    ORFs = find_all_ORFs_both_strands(dna)
    ind = argmax(map(len,ORFs))
    return ORFs[ind]


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    #import random
    for i in range(num_trials):
        ORF = ""
        dna_temp = []
        dna_string = ""
        for char in dna:
            dna_temp.append(char)
        shuffle(dna_temp)
        for item in dna_temp:    
            dna_string +=item
        if longest_ORF(dna_string)>ORF:
            longest_ORF(dna_string)
            ORF = longest_ORF(dna_string)
    return len(ORF)
        

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    protiens = []
    protein = ""
    ORFs = find_all_ORFs_both_strands(dna)
    for item in ORFs:
        if len(item)>threshold:
            protiens+=coding_strand_to_AA(item)
    for items in protiens:
        protein += items
    return protein
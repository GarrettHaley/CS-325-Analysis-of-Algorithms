#!/usr/bin/python

# Authors: Garrett Haley, Matthew Baker
# Date: February 20th 2017
# Description: Computes weighted edit distance table and backtrace

import numpy as np
from numpy import array
import sys
import fileinput
import re
from itertools import islice
import random

A = 1
T = 2
G = 3
C = 4

int_to_char = {1:'A', 2:'T', 3:'G', 4:'C'}
char_to_int = {'A':1, 'T':2, 'G':3, 'C':4}

#Array holds the weight for each edit
scoring = [[0,1,2,1,3],
            [1,0,1,5,1],
            [2,1,0,9,1],
            [1,5,9,0,1],
            [3,1,1,1,0]]

#Print finished sequences
def print_sequences(pairs, score):
    f = open("imp2output.txt", "a")
    top_seq = []
    bottom_seq = []
    for (b, t) in pairs:
        bottom_seq.append(b)
        top_seq.append(t)

    for n in bottom_seq:
        f.write(n)
    f.write(",")
    for n in top_seq:
        f.write(n)

    f.write(":")
    f.write(str(score))
    f.write("\r\n")
    f.close()

#Read the input file (Not the cost file)
def read_file_input(f_name):
    myList = []
    f = open(f_name, 'r')
    for line in f:
        line = line.rstrip('\n\r')
        split_line = line.split(',')
        split_line = tuple(split_line)
        myList.append(split_line)

    return myList

#Class that finds the optimal alignment of the two strings
class find_align(object):

    #Initialize the class
    def __init__(self, start, target):
        self.start = start
        self.target = target
        self.D = None

    #Function will return the weighted distance between two values
    def get_amount(self, i, j):
        return scoring[self.start[i - 1]][self.target[j - 1]]

    #Returns the pair of two characters
    def get_pair(self, i, j):
        xVar = int_to_char[self.start[i-1]] if i > 0 else '-'
        yVar = int_to_char[self.target[j-1]] if j > 0 else '-'
        return (xVar, yVar)

    #Traces back through the filled table to find the optimal route
    def back_trace(self):
        calibration= []
        score = 0
        i = len(self.start)
        j = len(self.target)
        while i > 0 and j > 0:
            if self.D[i][j - 1] + scoring[0][self.target[j-1]] == self.D[i][j]: #Insertion      #Swapped this If statement with the last else if
                score = score + scoring[0][self.target[j-1]]
                calibration.append(self.get_pair(0, j))
                j = j - 1
            elif self.D[i - 1][j] + scoring[self.start[i-1]][0] == self.D[i][j]: #Deletion
                score = score + scoring[self.start[i-1]][0]
                calibration.append(self.get_pair(i, 0))
                i = i - 1
            elif self.D[i - 1][j - 1] + self.get_amount(i, j) == self.D[i][j]: #Substitution
                calibration.append(self.get_pair(i, j))
                score = score + self.get_amount(i, j)
                i = i - 1
                j = j - 1
        while i > 0:
            calibration.append(self.get_pair(i, 0))
            score = score + scoring[self.start[i-1]][0]
            i = i - 1
        while j > 0:
            calibration.append(self.get_pair(0, j))
            score = score + scoring[0][self.target[j-1]]
            j = j - 1
        calibration.reverse()
        return calibration, score

    #Computes the optimal alignment and edit distance, main function of class
    def find_alignment(self):
        self.compute_array()
        return self.back_trace()

    #Computes the 2D table
    def compute_array(self):
        self.D = []

        for i in xrange(0, len(self.start) + 1):
            self.D.append([i])
        self.D[0] = range(0, len(self.target) + 1)

        #Updated initialization for weighted
        self.D[0][0] = 0

        for i in range(1, len(self.start) + 1):
            self.D[i][0] = self.D[i-1][0] + scoring[self.start[i-1]][0]

        for j in range(1, len(self.target) + 1):
            self.D[0][j] = self.D[0][j-1] + scoring[0][self.target[j-1]]

        for i in range(1, len(self.start) + 1):
            for j in range(1, len(self.target) + 1):
                self.D[i].append(min( self.D[i-1][j-1] + self.get_amount(i, j),       #Substitution
                                      self.D[i-1][j] + scoring[self.start[i-1]][0],   #Deletion
                                      self.D[i][j-1] + scoring[0][self.target[j-1]])) #Insertion


#Wrapper function that sets up the right formatting for edit dist
def edit_distance_wrapper(list_of_tuples):

    for tup in list_of_tuples:
        int_list0 = []
        int_list1 = []
        for ele in tup[0]:
            for char in ele:
                int_list0.append(char_to_int[char])
        for ele in tup[1]:
            for char in ele:
                int_list1.append(char_to_int[char])

        align = find_align(int_list0, int_list1)
        pairs, score = align.find_alignment()
        print_sequences(pairs, score)

    return

#Reads the data from the cost file into the matrix
def read_into_matrix():
    f = open("imp2cost.txt")
    file_list = []
    arr = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
    for line in f:
        for e in line:
            if e != 'T' and e != 'A' and e != 'C' and e != 'G' and e != ',' and e != '*' and e != '-' and e != '\n' and e != '\r':
                file_list.append(e)
    for i in range(len(file_list)):
        file_list[i] = int(file_list[i])

    z = 0
    for i in range(0, 5, 1):
        for j in range(0, 5, 1):
            arr[i][j] = file_list[z]
            z = z + 1

    return arr

#main; wrapper function for entire program
def main():
    input_file = "imp2input.txt"
    scoring = read_into_matrix()
    list_of_tuples = read_file_input(input_file)
    edit_distance_wrapper(list_of_tuples)
    return

main()

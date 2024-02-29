
#=============================================================================
import sys
import time
from collections import OrderedDict
import itertools
import pandas as pd
from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser





#=============================================================================
# FUNCTIONS

# itemset / iset: an ordered list of int's representing an itemset
#                 we use int's not strings to make this more efficient


def istrClean(istr):
    istr = ' '.join(istr.strip('\n').split())
    for token in istr.split():
        if not token.isnumeric():
            print('Item "%s" is not an integer!' % token)
            exit(-1)
    return istr

def string2iset(istr):
    return [int(token) for token in istr.split()]

def iset2string(iset):
    itok = [str(item) for item in iset]
    return ' '.join(itok)
 
def findsubsets(s, n):
    return list(itertools.combinations(s, n))



#   This function takes all the frequent sets as the input and generates combinations for the association rules
def generateCombinations(freqSet,k):
    rules = []
    for i in freqSet:
        if isinstance(i, list):
            if len(i) != 0:
                length = len(i) - k
                while length > 0:
                    combos = list(itertools.combinations(i, length))
                    t = []
                    LHS = []
                    for right in combos:
                        left = set(i) - set(right)
                        t.append(list(left))
                        t.append(list(right))
                        #print(temp)
                        rules.append(t)
                        t = []
                        length = length -1
    return rules



#   This function creates the final output of the algorithm by taking Association Rules as the input
def Output(rules, dataSet, minimumSupport, minimumConfidence):
    minimumConfidence = minimumConfidence * 100
    Output = []
    suppX = 0
    suppXP = 0
    suppXY = 0
    suppXYP = 0
    for rule in rules:
        for t in dataSet:
            if set(rule[0]).issubset(set(t)):
                suppX = suppX + 1
            if set(rule[0] + rule[1]).issubset(set(t)):
                suppXY = suppXY + 1
        suppXP= (suppX * 1.0 / 5) * 100
        suppXYP = (suppXY * 1.0 / len(dataSet)) * 100
        confidence = (suppXYP / suppXP) * 100
        if confidence >= minimumConfidence:
            supportOfXAppendString = "Support Of X: " + str(round(suppXP, 2))
            supportOfXandYAppendString = "Support of X & Y: " + str(round(suppXYP))
            confidenceAppendString = "Confidence: " + str(round(confidence)) + "%"

            Output.append(supportOfXAppendString)
            Output.append(supportOfXandYAppendString)
            Output.append(confidenceAppendString)
            Output.append(str(rule[0])+ "-->"+ str(rule[1]))

    return Output
#=============================================================================
# MAIN

if __name__ == '__main__':
    k       = 0 # length of itemsets in input level file
    preCNT  = 0 # running tally of pre-candidates produced
    candCNT = 0 # running tally of candidates (after apriori)
    itemset1 = []

    # read first line of level file to measure itemset length
    with open(sys.argv[1], 'r', encoding='utf-8') as inLev:
        for line in inLev:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            itemset.pop(0)
            k = len(itemset)
            itemset1.append(itemset)


itemset2 = []
difference = []

with open(sys.argv[2], 'r', encoding='utf-8') as inLev:
    for line in inLev:
        line = istrClean(line)
        itemset = string2iset(line.strip('\n'))
        itemset.pop(0)
        itemset2.append(itemset)


        
rules = generateCombinations(itemset2,k)
output = Output(rules, itemset2, 0, float(sys.argv[3]))

for i in output:
    print(i)

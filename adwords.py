#!/usr/bin/env python

import csv

import sys
reload(sys)
from collections import defaultdict
import math
import random

if len(sys.argv) != 2:
    print "Enter a method: greedy, mssv, balance"
    exit(1)
method = sys.argv[1]


class AdTransaction:
	def __init__(self):
		self.advertiserID = ""
		self.bid = "0"
		
	def __str__(self):
		return "advertiserID: %s , bid: %s " % (self.advertiserID, self.bid)

	def __repr__(self):
		return "advertiserID: %s , bid: %s " % (self.advertiserID, self.bid)

	def convertAdTransaction(self, row):
		
		self.advertiserID = str(row[0])
		self.bid = str(row[2])

def createAdTransactions():
	Transactions = defaultdict(list)
	budget = {}

	with open('bidder_dataset.csv', 'rb') as csvfile:
	     next(csvfile)
   	     reader = csv.reader(csvfile, delimiter=',')
   	     for row in reader:
	     	 a = AdTransaction()
		 a.convertAdTransaction(row)

		 if str(row[0]) not in budget:
			budget[str(row[0])] = str(row[3])

		 Transactions[str(row[1])].append(a)
	
	return Transactions, budget

def greedy(adTransactions, budget, queries, totalBudget):
	sumRevenue = 0.0
	original = dict(budget)

	for num in range(0,100):
		budget = dict(original)
		random.shuffle(queries)
		for query in queries:
			maximum = 0.0
			bidder = ''	
	
			for transaction in adTransactions.get(str(query)):				
				if float(budget[str(transaction.advertiserID)]) > 0.0:
					if float(transaction.bid) > maximum:
						maximum = float(transaction.bid)
						bidder = str(transaction.advertiserID)
	
			sumRevenue += maximum
			if bidder != '':
				budget[bidder] = str(float(budget[bidder]) - maximum)	
	
	meanRevenue = float(sumRevenue/100)
	print 'Revenue: ' + str(meanRevenue) + ', Competitive Ratio: ' +  str(meanRevenue/totalBudget)

def MSVV(adTransactions, budget, queries, totalBudget):
	sumRevenue = 0.0
	weight = {}
	cumulative = {}

	for num in range(0,100):
		for b in budget:
			weight[b] = 1.00 - math.exp(0.00 - 1.00)
			cumulative[b] = 0.00
		random.shuffle(queries)
		for query in queries:
			maximum = 0.0
			max_weight = 0.0
			bidder = ''	
		
			for transaction in adTransactions.get(str(query)):				
				if cumulative[str(transaction.advertiserID)] < float(budget[str(transaction.advertiserID)]):
					if (float(transaction.bid) * weight[str(transaction.advertiserID)]) > max_weight:
						max_weight = float(transaction.bid) * weight[str(transaction.advertiserID)]
						maximum = float(transaction.bid)
						bidder = str(transaction.advertiserID)
	
			sumRevenue += maximum
		
			if bidder != '':
				cumulative[bidder] += maximum
				weight[bidder] = 1.00 - math.exp((cumulative[bidder]/float(budget[bidder])) - 1.00)	
	
	meanRevenue = float(sumRevenue/100)
	print 'Revenue: ' + str(meanRevenue) + ', Competitive Ratio: ' +  str(meanRevenue/totalBudget)

def balance(adTransactions, budget, queries, totalBudget):
	sumRevenue = 0.0
	original = dict(budget)

	for num in range(0,100):
		budget = dict(original)
		random.shuffle(queries)
		for query in queries:
			maximum = 0.0
			remaining = 0.0
			bidder = ''	
	
			for transaction in adTransactions.get(str(query)):				
				if float(budget[str(transaction.advertiserID)]) > 0.0:
					if float(budget[str(transaction.advertiserID)]) > remaining:
						maximum = float(transaction.bid)
						remaining = float(budget[str(transaction.advertiserID)])
						bidder = str(transaction.advertiserID)
	
			sumRevenue += maximum
			if bidder != '':
				budget[bidder] = str(float(budget[bidder]) - maximum)	
	
	meanRevenue = float(sumRevenue/100)
	print 'Revenue: ' + str(meanRevenue) + ', Competitive Ratio: ' +  str(meanRevenue/totalBudget)

def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    wordList = []
    f = open(filename, 'rU')
    for line in f:
	wordList.append(line.strip())
    f.close()
    return wordList

def main():
 	
	adTransactions, budget = createAdTransactions()
	queries = load_wordlist("queries.txt")
	totalBudget = 0.0

	for key in budget:
		totalBudget += float(budget[key])
	
	if method == 'greedy':
		greedy(adTransactions, budget, queries, totalBudget)
	elif method == 'mssv':
		MSVV(adTransactions, budget, queries, totalBudget)
	elif method == 'balance':
		balance(adTransactions, budget, queries, totalBudget)
	else:
		print "Enter a valid method- greedy, mssv, balance"	
	

if __name__=="__main__":
    	main()

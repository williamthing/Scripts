#!/bin/python

# William Thing

# Calculate my Stock Portfolio's Dividends by taking in a CSV file of
# my stock portfolio's information

import csv

input_file = csv.DictReader(open("stock-portfolio.csv"))

total = 0.00
annual_div = []

for row in input_file:
    share_val = float(row["share_val"])
    num_shares = float(row["num_shares"])
    compound_div = float(row["div_yield"]) * 4 * num_shares
    annual_div.append(compound_div)
    total += share_val

# calc dividend percentage
# calc annual dividend yield
annual_div_yield = 0.00     # annual div yield is in percentage
for div in annual_div:
    annual_div_yield += div / total

print "-----Portfolio Statistics-----"
print 'Annual Dividend Yield: {0:.2f}%'.format(annual_div_yield * 100)
print 'Annual Payout: ${0:.2f}'.format(annual_div_yield * total)
print "Total Value: ${0:.2f}".format(total)

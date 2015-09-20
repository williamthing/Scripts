#!/bin/python

# William Thing

# Calculate my Stock Portfolio's Dividends by taking in a CSV file of
# my stock portfolio's information

import csv

input_file = csv.DictReader(open("stock-portfolio.csv"))

total = 0.00
annual_div = []

print "<----- Stock Portfolio ----->"
for row in input_file:
    share_val = float(row["share_val"])
    compound_div = float(row["div_yield"]) * 4 * share_val
    annual_div.append(compound_div)
    total += share_val
    print "{} - ${}".format(row["stock_name"], row["div_yield"])

# calc dividend percentage
# calc annual dividend yield
annual_div_yield = 0.00
for div in annual_div:
    annual_div_yield += div / total

print ""
print annual_div_yield
print annual_div_yield / total * 100
print "Total Value: ${}".format(total)


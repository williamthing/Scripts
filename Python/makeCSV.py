import csv
# makes csv according to dictonary of fields
with open('ex.csv', 'w') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'first_name': 'Jake', 'last_name': 'Garrison'})
    writer.writerow({'first_name': 'Will', 'last_name': 'Thing'})

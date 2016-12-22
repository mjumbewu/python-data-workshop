import csv
import sys

# Open and read from a CSV file
infile = open("turnout.csv")
rowiter = csv.DictReader(infile)
rows = list(rowiter)

# Create a new table containing Precinct Code, Political Party,
# and Voter Count.
cleanrows = []
for oldrow in rows:
    newrow = {'Precinct Code': oldrow['Precinct Code'],
              'Political Party': oldrow['Political Party'],
              'Voter Count': oldrow['Voter Count']}
    cleanrows.append(newrow)

cleanheader = ['Precinct Code', 'Political Party', 'Voter Count']

# Split the precinct code into ward and division
splitrows = []
for oldrow in cleanrows:
    newrow = oldrow.copy()
    code = newrow.pop('Precinct Code')
    ward, div = code[:2], code[2:]
    newrow['Ward'] = ward
    newrow['Division'] = div
    splitrows.append(newrow)

splitheader = cleanheader[1:] + ['Ward', 'Division']

# Write the new table to standard output
outputter = csv.DictWriter(sys.stdout, fieldnames=splitheader)
outputter.writerows(splitrows)

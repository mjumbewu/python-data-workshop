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
    newrow = [oldrow['Precinct Code'],
              oldrow['Political Party'],
              oldrow['Voter Count']]
    cleanrows.append(newrow)

cleanheader = ['Precinct Code', 'Political Party', 'Voter Count']

# Write the new table to standard output
outputter = csv.writer(sys.stdout)
outputter.writerow(cleanheader)
outputter.writerows(cleanrows)

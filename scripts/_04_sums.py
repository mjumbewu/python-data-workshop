import csv
import sys

# Open and read from a CSV file
infile = open("registry.csv")
rowiter = csv.DictReader(infile)
rows = list(rowiter)

# Count the total number of voters in each political party
summaries = {}
for row in rows:
    ward = row['Ward']
    if ward not in summaries:
        summaries[ward] = {'Sum_Dem': 0, 'Sum_Rep': 0, 'Sum_Total': 0,
                           'Ward': ward}
    summaries[ward]['Sum Dem'] += int(row['Dem'])
    summaries[ward]['Sum Rep'] += int(row['Rep'])
    summaries[ward]['Sum Total'] += int(row['Total'])

summaryrows = summaries.values()
summaryheader = ['Ward', 'Sum Dem', 'Sum Rep', 'Sum Total']

# Write the new table to standard output
outputter = csv.DictWriter(sys.stdout, fieldnames=summaryheader)
outputter.writerows(summaryrows)

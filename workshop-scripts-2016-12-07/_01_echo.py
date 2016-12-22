import csv
import sys

infile = open("turnout.csv")
rowiter = csv.reader(infile)
header = next(rowiter)
rows = list(rowiter)

outputter = csv.writer(sys.stdout)
outputter.writerow(header)
outputter.writerows(rows)

# NOTE: The above line with the "writerows" function is
#       the same as looping over each of the rows and
#       outputting each one individually, like this:
#
# for row in rows:
#     outputter.writerow(row)

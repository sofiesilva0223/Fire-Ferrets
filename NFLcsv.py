import csv

with open('NFL.txt', 'r') as infile:
     lineSep = (line.strip() for line in infile)
     lineSpace = (line.split(",") for line in lineSep if line)
     with open('NFL.csv', 'w') as outfile:
         write = csv.writer(outfile)
         write.writerows(lineSpace)



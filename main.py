import csv
import json
import xml
#HW2
#Fire Ferrets: Cassidy Chu, Sofia Silva, Edin Schneider, Matt Borja
#CMPE 131, section 01

#Reads filename as an argument
def readTxt (filename):
    with open(filename) as fileObject:
        contents = fileObject.read()
    #print(contents)  #will print contents of NFL.txt
readTxt('NFL.txt')

#Second argument for coverting file to c, j and x based on user input
def userchoice():
    # Prompt user to choose c,j,x code:
    choice = input('Enter your choice for file you want:\n c for csv file\n j for json file\n x for xml file\n')
    print(choice)
    #choice outcomes
    if choice == 'c':
        with open('NFL.txt', 'r') as infile:
            lineSep = (line.strip() for line in infile)
            lineSpace = (line.split(",") for line in lineSep if line)
            with open('NFL.csv', 'w') as outfile:
                write = csv.writer(outfile)
                write.writerows(lineSpace)
    elif choice == 'j':
        with open('NFL.txt', 'r') as infile:
            lineSep = (line.strip() for line in infile)
            lineSpace = (line.split(",") for line in lineSep if line)
            with open('NFL.csv', 'w') as outfile:
                write = csv.writer(outfile)
                write.writerows(lineSpace)
        csvf = open('NFL.csv', 'r')
        jsonf = open('NFL.json', 'w')

        read = csv.DictReader(csvf)
        for row in read:
            json.dump(row, jsonf)
            jsonf.write('\n')
    #elif choice == 'x':
    else:
        print("Goodbye")
userchoice() #call function
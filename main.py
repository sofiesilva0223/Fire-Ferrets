import csv
import json
import xml
from xml.etree.ElementTree import Element, SubElement, tostring, parse, ElementTree
import xml.etree.ElementTree as ET
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
        with open('NFL.txt', 'r') as infile: #need to take out spaces from txt file
            lineSep = (line.strip() for line in infile)
            lineSpace = (line.split(",") for line in lineSep if line)
            with open('NFL.csv', 'w') as outfile: #create csv
                write = csv.writer(outfile)
                write.writerows(lineSpace)
                
        csvf = open('NFL.csv', 'r',encoding='utf-8')
        jsonf = open('NFL.json', 'w',encoding='utf-8', newline='\n')
        read = csv.DictReader(csvf)  #convert csv to json
        for row in read:
            jsonf.write(json.dumps(row,skipkeys=True, allow_nan=True, indent=6))

    elif choice == 'x':
        with open('NFL.txt', 'r') as infile:
            keys = infile.readline().split("\t")
            lines = infile.readlines()
            root = Element('Data')
            #loops through each line to collect the data and place them accordingly
            for line in lines:
                lineElement = SubElement(root, "Line")
                line = line.split("\t")
                for i, key in enumerate(keys):
                    child = SubElement(lineElement, keys[i])
                    child.text = line[i]
            tree = ElementTree(root)
            with open ("NFL.xml", "wb") as outfile :
                tree.write(outfile)
    else:
        print("Goodbye")
userchoice() #call function

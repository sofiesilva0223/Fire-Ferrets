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
    print(contents)  #will print contents of NFL.txt
readTxt('NFL.txt')

#Prompt user to choose c,j,x code:

#Function for coverting file to c, j and x based on letter chosen from user input:



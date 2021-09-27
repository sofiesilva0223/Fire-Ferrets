import csv
import json
import xml

def txt_convert(filename, convert_to):
    
    fileA = open("football.txt", "r")   #open file in read only mode
    data = fileA.readlines()            #data gets all text in file in a list of strings  
    fileA.close()

    if convert_to is 'c':
        writer = csv.writer(open("output", 'w'))
        for row in data:
            writer.writerow(row)
    elif convert_to is 'j':
        with open('output.txt', 'w') as json_file:
            json.dump(data, json_file)
    elif convert_to is 'x':
    else:
        #invalid input
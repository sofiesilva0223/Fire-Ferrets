import csv
import json
import xml

def txt_convert(filename, convert_to):
    
    with open(filename) as file_object:
        contents = file_object.read()

    if convert_to is 'c':
        writer = csv.writer(open("output", 'w'))
        for row in contents:
            writer.writerow(row)
    elif convert_to is 'j':
        with open('output.txt', 'w') as json_file:
            json.dump(contents, json_file)
    elif convert_to is 'x':
    else:
        #invalid input
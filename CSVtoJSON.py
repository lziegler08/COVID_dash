import csv
import json
 
# Function to convert a CSV to JSON
# Inputs: file path of the csv file and file path of json
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        
        # Convert each row of the csv to a dictionary key with next rows as info
        for rows in csvReader:
             
            # Primary key == Country
            key = rows['Country']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
        

# Test out the function:
csvFilePath = r'TestCSV.csv'
jsonFilePath = r'TestJSON.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)
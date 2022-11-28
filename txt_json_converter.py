#%%
import json
# test
# the file to be converted
filename = 'img1toimg0.txt'

# resultant dictionary
dict1 = {"points": []}

# fields in the sample file
fields =['x_coord', 'y_coord']

with open(filename) as fh:
    coordinates = []
	
    for line in fh:
        description = list(line.strip().split()) # reading line by line from the text file
        coordinates.append([description[0],description[1]]) # append x,y coordinate	
        print(description) # display output for each lines

dict1["points"].append(coordinates)

# creating json file		
out_file = open("test.json", "w")
json.dump(dict1, out_file, indent = 4) # tab
out_file.close()
#%%
with open("test.json") as f:
    mydata = json.load(f)

mydata['points']
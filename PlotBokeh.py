# Python code to create interactive COVID dashboard
# Output: HTML
# Input: json data files

import json
from bokeh.plotting import figure, show

# function to convert a json file to dictionary
def jsonToDict(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


# Open json files and convert to a dictionary
files = ['world-o-meter_2022-12-01.json','world-o-meter_2022-12-02.json','world-o-meter_2022-12-03.json']
wom01 = jsonToDict(files[0])
wom02 = jsonToDict(files[1])
wom03 = jsonToDict(files[2])


# Create plots
# Line plot to show total deaths
p1 = figure(title="Total Death", x_axis_label = "Date", y_axis_label = "Total Death")
p1.line(wom01['name'][0],wom01['total deaths'][0], legned_label="USA", line_width = 3)
show(p1)
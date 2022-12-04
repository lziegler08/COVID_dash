# Python code to create interactive COVID dashboard
# Output: HTML
# Input: json data files

import json
from bokeh.plotting import figure, show
from bokeh.models import CheckboxGroup, ColumnDataSource
from bokeh.layouts import column, row

# output_file()

# function to convert a json file to dictionary
def jsonToDict(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

# function to get certain data from dictionaries
def getData(files,type,pos,norm = 0):
    results = []
    for file in files:
        temp = file[type][pos]
        if norm == 1: #normalize for population
            temp = temp/(file['population'][pos])
        results.append(temp)
    return results


# Open json files and convert to a dictionary
files = ['world-o-meter_2022-12-01.json', 'world-o-meter_2022-12-02.json','world-o-meter_2022-12-03.json']
jsonWOM = [jsonToDict(files[0]),jsonToDict(files[1]),jsonToDict(files[2])]


# Create plots
# Universal data:
datesWOM = getData(jsonWOM,'date collected',0)
countries = ['USA','France','Brazil','Austria','Greece','Monaco']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

USAdeathsWOM = getData(jsonWOM,'total deaths',0,1)
FrancedeathsWOM = getData(jsonWOM,'total deaths',1,1)
BrazildeathsWOM = getData(jsonWOM,'total deaths',2,1)
AustriadeathsWOM = getData(jsonWOM,'total deaths',3,1)
GreecedeathsWOM = getData(jsonWOM,'total deaths',4,1)
MonacodeathsWOM = getData(jsonWOM,'total deaths',5,1)

# Line plot to show total deaths
#p1 = figure(x_range = datesWOM, title="Total Deaths Normalized by Population", x_axis_label = "Date", y_axis_label = "Total Deaths")
#p2.circle(datesWOM,FrancedeathsWOM, legend_label="France", color="red", size = 10)
#p1.circle(datesWOM,BrazildeathsWOM, legend_label="Brazil", color="green", size = 10)
#p1.circle(datesWOM,AustriadeathsWOM, legend_label="Austria", color="purple", size = 10)
#p1.circle(datesWOM,GreecedeathsWOM, legend_label="Greece", color="pink", size = 10)
#p1.circle(datesWOM,MonacodeathsWOM, legend_label="Monaco", color="orange", size = 10)
#show(p1)

# Stacked Bar Plot for total Deaths
bar_data = {'countries': countries,
            '2022-12-01': [USAdeathsWOM[0], FrancedeathsWOM[0], BrazildeathsWOM[0], AustriadeathsWOM[0], GreecedeathsWOM[0], MonacodeathsWOM[0]],
            '2022-12-02': [USAdeathsWOM[1], FrancedeathsWOM[1], BrazildeathsWOM[1], AustriadeathsWOM[1], GreecedeathsWOM[1], MonacodeathsWOM[1]],
            '2022-12-03': [USAdeathsWOM[2], FrancedeathsWOM[2], BrazildeathsWOM[2], AustriadeathsWOM[2], GreecedeathsWOM[2], MonacodeathsWOM[2]]}

source_data = {'countries': countries,
            '2022-12-01': [USAdeathsWOM[0], FrancedeathsWOM[0], BrazildeathsWOM[0], AustriadeathsWOM[0], GreecedeathsWOM[0], MonacodeathsWOM[0]],
            '2022-12-02': [USAdeathsWOM[1], FrancedeathsWOM[1], BrazildeathsWOM[1], AustriadeathsWOM[1], GreecedeathsWOM[1], MonacodeathsWOM[1]],
            '2022-12-03': [USAdeathsWOM[2], FrancedeathsWOM[2], BrazildeathsWOM[2], AustriadeathsWOM[2], GreecedeathsWOM[2], MonacodeathsWOM[2]]}

p2 = figure(x_range = countries, height = 250, title="Total Deaths Normalized by Population", toolbar_location = None, tools="")
p2.vbar_stack(datesWOM, x='countries', width = 0.9, color = colors, source = source_data, legend_label=datesWOM)
p2.xgrid.grid_line_color = None
p2.y_range.end = 2.6
p2.legend.location = "top_left"
p2.legend.orientation = "horizontal"
p2.legend.click_policy = "hide"
show(p2)
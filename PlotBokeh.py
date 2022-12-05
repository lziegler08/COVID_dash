# Python code to create interactive COVID dashboard
# Output: HTML
# Input: json data files

import json
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, CustomJS, FactorRange, HoverTool
from bokeh.layouts import column, row, gridplot
from bokeh.models.widgets import Panel, Tabs
from operator import truediv
import math

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

# function to get the start and end angles for pie charts
def getPieAngles(case):
    start_angle = [0, death_rad[case], case_rad[0]+death_rad[case]]
    end_angle = [death_rad[case], case_rad[case]+death_rad[case],0]
    return start_angle, end_angle


# Open json files and convert to a dictionary
files = ['world-o-meter_2022-12-01.json', 'world-o-meter_2022-12-02.json','world-o-meter_2022-12-03.json']
jsonWOM = [jsonToDict(files[0]),jsonToDict(files[1]),jsonToDict(files[2])]

# Create plots
# Universal data:
datesWOM = getData(jsonWOM,'date collected',0)
datesWOM = [i.replace('-','_') for i in datesWOM]
datesWOM = [j.replace('2022_','') for j in datesWOM]
countries = ['USA','France','Brazil','Austria','Greece','Monaco']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

USAdeathsWOM = getData(jsonWOM,'total deaths',0,0)
FrancedeathsWOM = getData(jsonWOM,'total deaths',1,0)
BrazildeathsWOM = getData(jsonWOM,'total deaths',2,0)
AustriadeathsWOM = getData(jsonWOM,'total deaths',3,0)
GreecedeathsWOM = getData(jsonWOM,'total deaths',4,0)
MonacodeathsWOM = getData(jsonWOM,'total deaths',5,0)

USAcasesWOM = getData(jsonWOM,'total cases',0,0)
FrancecasesWOM = getData(jsonWOM,'total cases',1,0)
BrazilcasesWOM = getData(jsonWOM,'total cases',2,0)
AustriacasesWOM = getData(jsonWOM,'total cases',3,0)
GreececasesWOM = getData(jsonWOM,'total cases',4,0)
MonacocasesWOM = getData(jsonWOM,'total cases',5,0)

USApopWOM = getData(jsonWOM,'population',0,0)
FrancepopWOM = getData(jsonWOM,'population',1,0)
BrazilpopWOM = getData(jsonWOM,'population',2,0)
AustriapopWOM = getData(jsonWOM,'population',3,0)
GreecepopWOM = getData(jsonWOM,'population',4,0)
MonacopopWOM = getData(jsonWOM,'population',5,0)

# Line dots to show total deaths
#p1 = figure(x_range = datesWOM, title="Total Deaths Normalized by Population", x_axis_label = "Date", y_axis_label = "Total Deaths")
#p2.circle(datesWOM,FrancedeathsWOM, legend_label="France", color="red", size = 10)
#p1.circle(datesWOM,BrazildeathsWOM, legend_label="Brazil", color="green", size = 10)
#p1.circle(datesWOM,AustriadeathsWOM, legend_label="Austria", color="purple", size = 10)
#p1.circle(datesWOM,GreecedeathsWOM, legend_label="Greece", color="pink", size = 10)
#p1.circle(datesWOM,MonacodeathsWOM, legend_label="Monaco", color="orange", size = 10)
#show(p1)

# Stacked Bar Plot for Total Deaths
source_data = {'countries': countries,
            '2022_12_01': [USAdeathsWOM[0], FrancedeathsWOM[0], BrazildeathsWOM[0], AustriadeathsWOM[0], GreecedeathsWOM[0], MonacodeathsWOM[0]],
            '2022_12_02': [USAdeathsWOM[1], FrancedeathsWOM[1], BrazildeathsWOM[1], AustriadeathsWOM[1], GreecedeathsWOM[1], MonacodeathsWOM[1]],
            '2022_12_03': [USAdeathsWOM[2], FrancedeathsWOM[2], BrazildeathsWOM[2], AustriadeathsWOM[2], GreecedeathsWOM[2], MonacodeathsWOM[2]]}

x = [(country,date) for country in countries for date in datesWOM]
counts = sum(zip(source_data['2022_12_01'], source_data['2022_12_02'], source_data['2022_12_03']),())

source = ColumnDataSource(data=dict(x=x,counts=counts))

p = figure(x_range=FactorRange(*x), height=250, title="Total Deaths", toolbar_location = "right", tools="hover,pan,box_zoom,reset")
p.vbar(x='x', top='counts', width=0.9, source=source, line_color = "white", fill_color=factor_cmap('x', palette=colors, factors=datesWOM, start=1, end=2))
hover = p.select(dict(type=HoverTool))
hover.tooltips = [("Deaths","@counts")]
p.xaxis.major_label_orientation = 1
#show(p)

# Pie Chart with Dropdown Menu
pie_data ={'countries': countries,
           'deaths': [USAdeathsWOM[2], FrancedeathsWOM[2], BrazildeathsWOM[2], AustriadeathsWOM[2], GreecedeathsWOM[2], MonacodeathsWOM[2]],
           'cases': [USAcasesWOM[2], FrancecasesWOM[2], BrazilcasesWOM[2], AustriacasesWOM[2], GreececasesWOM[2], MonacocasesWOM[2]],
           'population': [USApopWOM[2], FrancepopWOM[2], BrazilpopWOM[2], AustriapopWOM[2], GreecepopWOM[2], MonacopopWOM[2]]}

death_percent = list(map(truediv,pie_data['deaths'],pie_data['population']))
death_rad = [math.radians(percent*360) for percent in death_percent]
case_percent = list(map(truediv,pie_data['cases'],pie_data['population']))
case_rad = [math.radians(p*360) for p in case_percent]
sections = ['Deaths','Cases']
color = ["red","violet","lightblue"]

p1start, p1end = getPieAngles(0)
p1 = figure(height = 350, width = 350, title="USA", toolbar_location=None, tools="")
p1.wedge(x=0,y=0,radius=0.8,start_angle = p1start, end_angle = p1end, color=color)
p1.axis.visible = False
tab1 = Panel(child=p1, title="USA")
tabs = Tabs(tabs=[tab1])
#show(tabs)

# Put plots into a grid
grid = gridplot([[p], [tabs]])
show(grid)
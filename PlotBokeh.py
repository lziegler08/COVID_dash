# Python code to create interactive COVID dashboard
# Output: HTML
# Input: json data files

import json
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, CustomJS, FactorRange, HoverTool, Legend
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
        for i,c in enumerate(file['name']):
            if c == pos:
                temp = file[type][i]
                if norm == 1: #normalize for population per 1M
                    temp = (temp/(file['population'][i])*100000000)
                results.append(temp)
    return results

# function to get the start and end angles for pie charts
def getPieAngles(case):
    start_angle = [0, death_rad[case], case_rad[case]+death_rad[case]]
    end_angle = [death_rad[case], case_rad[case]+death_rad[case],0]
    return start_angle, end_angle


# Open json files and convert to a dictionary
files = ['world-o-meter_2022-12-01.json', 'world-o-meter_2022-12-02.json','world-o-meter_2022-12-03.json']
jsonWOM = [jsonToDict(files[0]),jsonToDict(files[1]),jsonToDict(files[2])]

# Create plots
# Universal data:
datesWOM = getData(jsonWOM,'date collected','USA')
datesWOM = [i.replace('-','_') for i in datesWOM]
datesWOM = [j.replace('2022_','') for j in datesWOM]
countries = ['USA','France','Brazil','Austria','Greece','Monaco']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

USAdeathsWOM = getData(jsonWOM,'total deaths','USA',0)
FrancedeathsWOM = getData(jsonWOM,'total deaths','France',0)
BrazildeathsWOM = getData(jsonWOM,'total deaths','Brazil',0)
AustriadeathsWOM = getData(jsonWOM,'total deaths','Austria',0)
GreecedeathsWOM = getData(jsonWOM,'total deaths','Greece',0)
MonacodeathsWOM = getData(jsonWOM,'total deaths','Monaco',0)

USAcasesWOM = getData(jsonWOM,'total cases','USA',0)
FrancecasesWOM = getData(jsonWOM,'total cases','France',0)
BrazilcasesWOM = getData(jsonWOM,'total cases','Brazil',0)
AustriacasesWOM = getData(jsonWOM,'total cases','Austria',0)
GreececasesWOM = getData(jsonWOM,'total cases','Greece',0)
MonacocasesWOM = getData(jsonWOM,'total cases','Monaco',0)

USApopWOM = getData(jsonWOM,'population','USA',0)
FrancepopWOM = getData(jsonWOM,'population','France',0)
BrazilpopWOM = getData(jsonWOM,'population','Brazil',0)
AustriapopWOM = getData(jsonWOM,'population','Austria',0)
GreecepopWOM = getData(jsonWOM,'population','Greece',0)
MonacopopWOM = getData(jsonWOM,'population','Monaco',0)

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

print(datesWOM)
x = [(country,date) for country in countries for date in datesWOM]
counts = sum(zip(source_data['2022_12_01'], source_data['2022_12_02'], source_data['2022_12_03']),())

source = ColumnDataSource(data=dict(x=x,counts=counts))

p = figure(x_range=FactorRange(*x), height=250, title="Total Deaths", toolbar_location = "right", tools="hover,pan,box_zoom,reset")
p.vbar(x='x', top='counts', width=0.9, source=source, line_color = "white", fill_color=factor_cmap('x', palette=colors, factors=datesWOM, start=1, end=2))
hover = p.select(dict(type=HoverTool))
hover.tooltips = [("Deaths","@counts")]
p.xaxis.major_label_orientation = 1
#show(p)

# PIE CHART WITH TABS FOR DIFFERENT COUNTRIES: DISPLAYS THE CUMULATIVE DEATHS
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
labels = ['Deaths', 'Cases', 'Healthy']

p1start, p1end = getPieAngles(0)
percent1 = [100*death_percent[0], 100*case_percent[0], 100-((100*death_percent[0]+100*case_percent[0]))]
source1 = ColumnDataSource(dict(p1start=p1start, p1end=p1end, labels=labels, color = color, percent1 = percent1))
p1 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p1.add_layout(Legend(),'right')
p1.wedge(x=0,y=0,radius=0.8,start_angle = 'p1start', end_angle = 'p1end', color='color', source=source1,  legend_group='labels')
hover = p1.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent1")]
p1.axis.visible = False
tab1 = Panel(child=p1, title="USA")

p2start, p2end = getPieAngles(1)
percent2 = [100*death_percent[1], 100*case_percent[1], 100-((100*death_percent[1]+100*case_percent[1]))]
source2 = ColumnDataSource(dict(p2start=p2start, p2end=p2end, labels=labels, color = color, percent2 = percent2))
p2 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p2.add_layout(Legend(),'right')
p2.wedge(x=0,y=0,radius=0.8,start_angle = 'p2start', end_angle = 'p2end', color='color', source=source2, legend_group='labels')
hover = p2.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent2")]
p2.axis.visible = False
tab2 = Panel(child=p2, title="France")

p3start, p3end = getPieAngles(2)
percent3 = [100*death_percent[2], 100*case_percent[2], 100-((100*death_percent[2]+100*case_percent[2]))]
source3 = ColumnDataSource(dict(p3start=p3start, p3end=p3end, labels=labels, color = color, percent3 = percent3))
p3 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p3.add_layout(Legend(),'right')
p3.wedge(x=0,y=0,radius=0.8,start_angle = 'p3start', end_angle = 'p3end', color='color', source=source3, legend_group='labels')
hover = p3.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent3")]
p3.axis.visible = False
tab3 = Panel(child=p3, title="Brazil")

p4start, p4end = getPieAngles(3)
percent4 = [100*death_percent[3], 100*case_percent[3], 100-((100*death_percent[3]+100*case_percent[3]))]
source4 = ColumnDataSource(dict(p4start=p4start, p4end=p4end, labels=labels, color = color, percent4 = percent4))
p4 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p4.add_layout(Legend(),'right')
p4.wedge(x=0,y=0,radius=0.8,start_angle = 'p4start', end_angle = 'p4end', color='color', source=source4, legend_group='labels')
hover = p4.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent4")]
p4.axis.visible = False
tab4 = Panel(child=p4, title="Austria")

p5start, p5end = getPieAngles(4)
percent5 = [100*death_percent[4], 100*case_percent[4], 100-((100*death_percent[4]+100*case_percent[4]))]
source5 = ColumnDataSource(dict(p5start=p5start, p5end=p5end, labels=labels, color = color, percent5 = percent5))
p5 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p5.add_layout(Legend(),'right')
p5.wedge(x=0,y=0,radius=0.8,start_angle = 'p5start', end_angle = 'p5end', color='color', source = source5, legend_group='labels')
hover = p5.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent5")]
p5.axis.visible = False
tab5 = Panel(child=p5, title="Greece")

p6start, p6end = getPieAngles(5)
percent6 = [100*death_percent[5], 100*case_percent[5], 100-((100*death_percent[5]+100*case_percent[5]))]
source6 = ColumnDataSource(dict(p6start=p6start, p6end=p6end, labels=labels, color = color, percent6 = percent6))
p6 = figure(height = 350, width = 500, title="Cumulative Death in the Population", toolbar_location=None, tools="hover")
p6.add_layout(Legend(),'right')
p6.wedge(x=0,y=0,radius=0.8,start_angle = 'p6start', end_angle = 'p6end', color='color', source=source6, legend_group='labels')
hover = p6.select(dict(type=HoverTool))
hover.tooltips = [('Category','@labels'),("Percentage","@percent6")]
p6.axis.visible = False
tab6 = Panel(child=p6, title="Monaco")

tabs = Tabs(tabs=[tab1,tab2,tab3,tab4,tab5,tab6])
#show(tabs)

# Put plots into a grid
grid = gridplot([[p], [tabs]])
show(grid)
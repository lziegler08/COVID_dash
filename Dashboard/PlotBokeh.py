# Python code to create interactive COVID dashboard
# Output: HTML
# Input: json data files

import json
from bokeh.plotting import figure, show, curdoc
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, FactorRange, HoverTool, Legend, Select, Paragraph, CustomJS, Div
from bokeh.layouts import column, row, gridplot, widgetbox
from bokeh.models.widgets import Panel, Tabs, Button
from bokeh.palettes import Spectral6,Spectral4,BuPu4,OrRd4
from operator import truediv
import math

# output_file()

# function to convert a json file to dictionary
def jsonToDict(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

# function to get certain data from dictionaries
def getData(files,type,pos,norm = 0,ny=0,daily=0):
    results = []
    for file in files:
        for i,c in enumerate(file['name']):
            if c == pos:
                temp = file[type][i]
                if norm == 1: #normalize for population per 1M
                    temp = (temp/(file['population'][i])*100000000)
                if ny == 1: #normaliz for population per 1M
                    temp = (float(temp)*100.0)
                if daily == 1:
                    temp = float(temp)*7.0
                results.append(temp)
    return results

# function to get the start and end angles for pie charts
def getPieAngles(case):
    start_angle = [0, death_rad[case], case_rad[case]+death_rad[case]]
    end_angle = [death_rad[case], case_rad[case]+death_rad[case],0]
    return start_angle, end_angle

# function to get deaths per day from cumulative deaths
def deathRateDaily(list):
    result = [item - list[idx - 1] for idx, item in enumerate(list)][1:]
    return result

def deathRateCum(input_list,wom=1,ny=0):
    if wom == 1:
        cumDeathRate = input_list[-1] - input_list[0]
    elif ny == 1:
        cumDeathRate = sum(input_list)
    return cumDeathRate


# Open json files and convert to a dictionary
files = ['world-o-meter_2022-12-01.json', 'world-o-meter_2022-12-02.json','world-o-meter_2022-12-03.json','world-o-meter_2022-12-04.json','world-o-meter_2022-12-05.json']
jsonWOM = [jsonToDict(files[0]),jsonToDict(files[1]),jsonToDict(files[2]),jsonToDict(files[3]),jsonToDict(files[4])]
nyfiles = ['ny_times_2022-12-02.json','ny_times_2022-12-03.json','ny_times_2022-12-04.json','ny_times_2022-12-05.json']
jsonNY = [jsonToDict(nyfiles[0]),jsonToDict(nyfiles[1]),jsonToDict(nyfiles[2]),jsonToDict(nyfiles[3])]

# Create plots
# Universal data:
datesWOM = getData(jsonWOM,'date collected','USA')
datesWOM = [i.replace('-','_') for i in datesWOM]
datesWOM = [j.replace('2022_','') for j in datesWOM]
datesNY = getData(jsonNY,'date collected','Brunei')
datesNY = [i.replace('-','_') for i in datesNY]
datesNY = [j.replace('2022_','') for j in datesNY]
countries = ['USA','France','Brazil','Austria','Greece','Monaco']
colors = ["#c9d9d3", "#718dbf", "#e84d60",'orange','maroon','green']

# Deaths
USAdeathsWOM = getData(jsonWOM,'total deaths','USA',0)
FrancedeathsWOM = getData(jsonWOM,'total deaths','France',0)
BrazildeathsWOM = getData(jsonWOM,'total deaths','Brazil',0)
AustriadeathsWOM = getData(jsonWOM,'total deaths','Austria',0)
GreecedeathsWOM = getData(jsonWOM,'total deaths','Greece',0)
MonacodeathsWOM = getData(jsonWOM,'total deaths','Monaco',0)

USAdeathsWOMnorm = getData(jsonWOM,'total deaths','USA',1)
FrancedeathsWOMnorm = getData(jsonWOM,'total deaths','France',1)
BrazildeathsWOMnorm = getData(jsonWOM,'total deaths','Brazil',1)
AustriadeathsWOMnorm = getData(jsonWOM,'total deaths','Austria',1)
GreecedeathsWOMnorm = getData(jsonWOM,'total deaths','Greece',1)
MonacodeathsWOMnorm = getData(jsonWOM,'total deaths','Monaco',1)

# Cases
USAcasesWOM = getData(jsonWOM,'total cases','USA',0)
FrancecasesWOM = getData(jsonWOM,'total cases','France',0)
BrazilcasesWOM = getData(jsonWOM,'total cases','Brazil',0)
AustriacasesWOM = getData(jsonWOM,'total cases','Austria',0)
GreececasesWOM = getData(jsonWOM,'total cases','Greece',0)
MonacocasesWOM = getData(jsonWOM,'total cases','Monaco',0)

# Population
USApopWOM = getData(jsonWOM,'population','USA',0)
FrancepopWOM = getData(jsonWOM,'population','France',0)
BrazilpopWOM = getData(jsonWOM,'population','Brazil',0)
AustriapopWOM = getData(jsonWOM,'population','Austria',0)
GreecepopWOM = getData(jsonWOM,'population','Greece',0)
MonacopopWOM = getData(jsonWOM,'population','Monaco',0)

# Death Rates - Daily
USAdailydeath = deathRateDaily(USAdeathsWOM)
Francedailydeath = deathRateDaily(FrancedeathsWOM)
Brazildailydeath = deathRateDaily(BrazildeathsWOM)
Austriadailydeath = deathRateDaily(AustriadeathsWOM)
Greecedailydeath = deathRateDaily(GreecedeathsWOM)
Monacodailydeath = deathRateDaily(MonacodeathsWOM)
Bruneidailydeath = getData(jsonNY,'daily deaths avg','Brunei',0,0,1)
HongKongdailydeath = getData(jsonNY,'daily deaths avg','Hong Kong',0,0,1)
Japandailydeath = getData(jsonNY,'daily deaths avg','Japan',0,0,1)
SouthKoreadailydeath = getData(jsonNY,'daily deaths avg','South Korea',0,0,1)
NewZealandailydeath = getData(jsonNY,'daily deaths avg','New Zealand',0,0,1)

# Death Rates - Daily - Normalized by population * 1M
USAdailydeathnorm = deathRateDaily(USAdeathsWOMnorm)
Francedailydeathnorm = deathRateDaily(FrancedeathsWOMnorm)
Brazildailydeathnorm = deathRateDaily(BrazildeathsWOMnorm)
Austriadailydeathnorm = deathRateDaily(AustriadeathsWOMnorm)
Greecedailydeathnorm = deathRateDaily(GreecedeathsWOMnorm)
Monacodailydeathnorm = deathRateDaily(MonacodeathsWOMnorm)
Bruneidailydeathnorm = getData(jsonNY,'per 100k','Brunei',0,1)
HongKongdailydeathnorm = getData(jsonNY,'per 100k','Hong Kong',0,1)
Japandailydeathnorm = getData(jsonNY,'per 100k','Japan',0,1)
SouthKoreadailydeathnorm = getData(jsonNY,'per 100k','South Korea',0,1)
NewZealandailydeathnorm = getData(jsonNY,'per 100k','New Zealand',0,1)

# Death Rates - Cumulative
USAcumdeath = deathRateCum(USAdeathsWOM)
Francecumdeath = deathRateCum(FrancedeathsWOM)
Brazilcumdeath = deathRateCum(BrazildeathsWOM)
Austriacumdeath = deathRateCum(AustriadeathsWOM)
Greececumdeath = deathRateCum(GreecedeathsWOM)
Monacocumdeath = deathRateCum(MonacodeathsWOM) 
Bruneicumdeath = deathRateCum(Bruneidailydeath)
HongKongcumdeath = deathRateCum(HongKongdailydeath)
Japancumdeath = deathRateCum(Japandailydeath)
SouthKoreacumdeath = deathRateCum(SouthKoreadailydeath)
NewZealancumdeath = deathRateCum(NewZealandailydeath)

# BAR PLOT FOR CUMULATIVE DEATHS BY POPULATION X 1M
source_data = {'countries': countries,
            '2022_12_05': [USAdeathsWOMnorm[4], FrancedeathsWOMnorm[4], BrazildeathsWOMnorm[4], AustriadeathsWOMnorm[4], GreecedeathsWOMnorm[4], MonacodeathsWOMnorm[4]]}

x = countries #[(country,date) for country in countries for date in datesWOM[4]]
counts = sum(zip(source_data['2022_12_05']),())

source = ColumnDataSource(data=dict(x=x,counts=counts,color=Spectral6))

p = figure(x_range=FactorRange(*x), height=400, title="Cumulative Deaths Normalized by Population x 1 Million", toolbar_location = "right", tools="hover,pan,box_zoom,reset")
p.vbar(x='x', top='counts', width=0.9, fill_color='color', source=source, line_color = "white")
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
color = ["maroon","orange","lightblue"]
labels = ['Deaths', 'New Cases', 'Healthy']

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

# BAR PLOT FOR DEATH RATES WITH AVERAGE SHOWN AS A LINE
sourceBar = ColumnDataSource(data=dict(x=datesNY,y=USAdailydeath,color=OrRd4))
pbar = figure(x_range=datesNY, width = 400, height = 400, title="Daily Death Rates", toolbar_location = "right", tools='pan')
pbar.vbar(x='x', top='y', width=0.9, fill_color='color', source=sourceBar, line_color = "white")
print(dict(x=datesNY,y=USAdailydeath,color=Spectral4))

# function for dropdown options
country = 'USA'

def update_plot(attr, old, new):
    country = menu.value
    if country == "USA":
        pbar.title.text = "USA Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=USAdailydeath,color=OrRd4)
    elif country =="France":
        pbar.title.text = "France Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Francedailydeath,color=OrRd4)
    elif country =="Brazil":
        pbar.title.text = "Brazil Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Brazildailydeath,color=OrRd4)
    elif country =="Austria":
        pbar.title.text = "Austria Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Austriadailydeath,color=OrRd4)
    elif country =="Greece":
        pbar.title.text = "Greece Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Greecedailydeath,color=OrRd4)
    elif country =="Monaco":
        pbar.title.text = "Monaco Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Monacodailydeath,color=OrRd4)
    elif country =="Brunei":
        pbar.title.text = "Brunei Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Bruneidailydeath,color=OrRd4)
    elif country =="Hong Kong":
        pbar.title.text = "Hong Kong Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=HongKongdailydeath,color=OrRd4)
    elif country =="Japan":
        pbar.title.text = "Japan Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=Japandailydeath,color=OrRd4)
    elif country =="South Korea":
        pbar.title.text = "South Korea Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=SouthKoreadailydeath,color=OrRd4)
    elif country =="New Zealand":
        pbar.title.text = "New Zealand Daily Death Rate [people per day]"
        sourceBar.data = dict(x=datesNY,y=NewZealandailydeath,color=OrRd4)

# dropdown menu
menu = Select(value = country, title='Daily Death Rates Normalized: Pick A Country', options=["USA","France","Brazil","Austria","Greece","Monaco","Brunei","Hong Kong","Japan","South Korea","New Zealand"])

menu.on_change('value', update_plot)
layoutpbar = column(menu,pbar)

# BAR PLOT FOR DEATH RATES WITH AVERAGE SHOWN AS A LINE
sourceBar2 = ColumnDataSource(data=dict(x=datesNY,y=USAdailydeathnorm,color=BuPu4))
pbar2 = figure(x_range=datesNY, width = 400, height = 400, title="Daily Death Rates Normalized", toolbar_location = "right", tools='pan')
pbar2.vbar(x='x', top='y', width=0.9, fill_color='color', source=sourceBar2, line_color = "white")

# function for dropdown options
country2 = 'USA'

def update_plot2(attr, old, new):
    country2 = menu2.value
    if country2 == "USA":
        pbar2.title.text = "USA Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=USAdailydeathnorm,color=BuPu4)
    elif country2 =="France":
        pbar2.title.text = "France Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Francedailydeathnorm,color=BuPu4)
    elif country2 =="Brazil":
        pbar2.title.text = "Brazil Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Brazildailydeathnorm,color=BuPu4)
    elif country2 =="Austria":
        pbar2.title.text = "Austria Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Austriadailydeathnorm,color=BuPu4)
    elif country2 =="Greece":
        pbar2.title.text = "Greece Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Greecedailydeathnorm,color=BuPu4)
    elif country2 =="Monaco":
        pbar2.title.text = "Monaco Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Monacodailydeathnorm,color=BuPu4)
    elif country2 =="Brunei":
        pbar2.title.text = "Brunei Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Bruneidailydeathnorm,color=BuPu4)
    elif country2 =="Hong Kong":
        pbar2.title.text = "Hong Kong Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=HongKongdailydeathnorm,color=BuPu4)
    elif country2 =="Japan":
        pbar2.title.text = "Japan Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=Japandailydeathnorm,color=BuPu4)
    elif country2 =="South Korea":
        pbar2.title.text = "South Korea Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=SouthKoreadailydeathnorm,color=BuPu4)
    elif country2 =="New Zealand":
        pbar2.title.text = "New Zealand Daily Death Rate Normalized x 1M"
        sourceBar2.data = dict(x=datesNY,y=NewZealandailydeathnorm,color=BuPu4)

# dropdown menu
menu2 = Select(value = country2, title='Daily Death Rates: Pick A Country', options=["USA","France","Brazil","Austria","Greece","Monaco","Brunei","Hong Kong","Japan","South Korea","New Zealand"])

menu2.on_change('value', update_plot2)
layoutpbar2 = column(menu2,pbar2)

# BUTTON

notifications = Div(text='')
button = Button(label="Click for information about data")
def button_call():
    notifications.text = "Data was collected from World-o-meter and the New York Times."
button.on_click(button_call)
box = widgetbox(button, notifications)

# Put plots into a grid
grid = gridplot([[tabs,p],[layoutpbar,layoutpbar2,box]])
curdoc().add_root(grid)

# bokeh serve --show PlotBokeh.py
# show(grid)
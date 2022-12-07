# COVID_dash:
COVID_dash is an interactive dashboard that displays COVID death data from different countries. This tool was built by scraping data from World-o-meter and the New York Times using the Python Library Beautiful Soup, and displayed using the Python library Bokeh. 

# Installation
* Download code form GitHub.
* Install Bokeh separately.
* Open a terminal and run code from the directory where you downloaded the code.
* Type in the terminal command: bokeh serve --show PlotBokeh.py
* A window in your internet browser should appear. 

# Widgets implemented:
* Pop-up: when the terminal command is entered, a new window in the internet browser should appear
* Tabs: can select which country data to visualize in a pie chart
* Drop-down menu: can select which country data to visualize in a bar graph.
* Different types of charts: pie chart and bar graphs

# Data
Data was collected from World-o-meter and the New York Times using the Python library Beautiful Soup for dates 12/1/2022 to 12/5/2022. The data displayed is cumulative death in population per country, cumulative deaths normalized by population per 1M people, raw daily death rates per country, and normalized death rates per country.

Sources: 
* https://www.nytimes.com/interactive/2021/us/covid-cases.html
* https://www.worldometers.info/coronavirus/





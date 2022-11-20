# COVID_dash

Project instructions link: https://utah.instructure.com/courses/821474/pages/project-covid-dashboard

# Important Dates - Deadlines
* Team and project organization: November 21th
* Data scraping: December 3rd
* Final submission (Data display + Project delivery): Sun 11

# Introduction
In this project, you will design and implement an interactive dashboard to support the visualization of coronavirus-related data. You will use Python as a programming language, the Bokeh library for displaying information and Github to deliver your project.

You are to work in teams of two or three.

# Project specification
There is a multitude of real-time statistics related to covid on the web. Some popular ones are worldometer Links to an external site.or nytimes Links to an external site.. I suggest that you visit these websites to get an understanding of the look-and-feel of a dashboard and how such a system is supposed to function.

The basic idea behind your dashboard is that it will allow users to compare the numbers between multiple countries in a dynamic fashion. Your website should allow users to visualize both static and dynamic graphs. It should also allow users to query your system for specific countries and their related stats.

Complex dashboards allow you to do a lot more than simply visualizing data. For example, you can subscribe to receive trends or do some correlations between different events. In the scope of this project, we will stick to visualizing death rates.

# Functional requirements
## Part 0: Team and project organization
The preparation of the project consists in gathering the members of your team, and suggesting a roadmap for delivering this project. It is highly suggested that you plan out the different features of the project, and separate tasks between members according to their respective profiles and schedule. For example, the project delivery can be set up in parallel with other activities by two different people. 

For this part, you are expected to send us a post through Piazza (private post to Instructors and team members) containing:

The team members names and UIDs
Expected role/tasks of each members
Envisioned Python tools, modules and classes for each part
Link to a newly created github project
This will allow us to give you early feedback, and suggest tools relevant to your approach.

## Part 1: Data scraping
In this phase, you will focus on collecting data from the web in order to compute the following metrics:

Daily death rates
Cumulative death rates
Data should be both "raw" (absolute numbers) and normalized by population (relative to 1M of people). Collected data should be separated by country, and stored on the disk in the JSON format to facilitate searching of information. You can aggregate data from multiple online sources, but you should keep track of the provenance from each data point.

For this part, you are expected to commit both your scrapping code, and the JSON file on github for at least two consecutive days. Your code must implement a module named ScrapeWebsite that contains a function scrape_country. scrape_country should have at least two input parameters: the name of a country, and a website for retrieving covid stats for said country. scrape_country should return data associated with a given country.

## Part 2: Data display
In this phase, you will focus on the User Interface of your project. Bokeh is a data visualization library in Python. It provides highly interactive graphs and plots. What makes it different from other Python plotting libraries is that the output from Bokeh will be on the web page, meaning if we run the code in python editor the resulting plot will be in the browser. This gives the advantage of embedding the Bokeh plot on any website. You are encouraged to use HTML features for creating pop-up and pull-down menus, value lists, input/output forms, labels and customized reports, and in the process come up with a system that caters to users with only limited computer knowledge. We don’t care about having a beautiful UI. It only has to work!

## Part 3: Project delivery
Github is a platform used to host open source software development projects. The frontpage of your github project (README) should contain all the information necessary to install your project. You are encouraged to use github during the whole process, not just to push your final code. We'll use your github repository to evaluate the project as a whole, but also quantify and evaluate individual contributions.

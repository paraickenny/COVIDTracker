# COVIDTracker
Scripts to automatically retrieve daily COVID19 data from Wisconsin State Dept of Health, analyze data at the level of census tracts, and generate a choropleth (heatmap) of 7 day rolling case numbers in census tracts in Western Wisconsin.

The initial script covidtracker.py was written in Python2.7. This is superseded by two Python3 scripts described below.

The optimal implmentation is to first run covidtracker_py3.py to compute all the necessary data, followed by choropleth_generator.py to output the heatmap.

A web implementation was located at http://lacrossecovid19.org (Terminated 04/26/2023 as reporting of test data to states has been unreliable for some time due to the utilization of home testing).


import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import requests
import csv
from arcgis import GIS

# import latest census tract data from DHS WI
#censusdatafile = "COVID-19_Historical_Data_by_Census_Tract.csv"
#censusdatafile = "heatmap.html"
#censusdatafile = "https://opendata.arcgis.com/datasets/89d7a90aafa24519847c89b249be96ca_13.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"


# assemble list of counties of interest

counties = []
counties.append(["La Crosse County", 55063, 114638])
counties.append(["Trempealeau County", 55121, 29649])
counties.append(["Vernon County", 55123, 30822])
counties.append(["Monroe County", 55081, 46253])
counties.append(["Juneau County", 55057, 26687])
counties.append(["Crawford County", 55023, 16131])
counties.append(["Richland County", 55103, 17252])
counties.append(["Grant County", 55043, 51439])
counties.append(["Adams County", 55001, 20220])
counties.append(["Buffalo County", 55011, 13031])

parameters = []

# Determine the relevant days to interrogate for the data
today = str(date.today())
weekago = str(date.today() - timedelta(days=7))
dayago = str(date.today() - timedelta(days=1))
twodaysago = str(date.today() - timedelta(days=2))
threedaysago = str(date.today() - timedelta(days=3))
fourdaysago = str(date.today() - timedelta(days=4))
fivedaysago = str(date.today() - timedelta(days=5))

eightdaysago = str(date.today() - timedelta(days=8))
tomorrow = str(date.today()+timedelta(days=1))
sixdaysago = str(date.today() - timedelta(days=6))

print ("today:")
print (today)
print (type(today))
#censusdatafile = "https://opendata.arcgis.com/datasets/81a5286520a44e2c8f3546c840265f63_13.csv"
censusdatafile = "https://opendata.arcgis.com/datasets/64d974da1bdd4b7a8a4aa8e83c2d3a49_13.csv"
censusdatacurrent = 0            # sets a flag if today's data are present in the census file download
countyvaxdatacurrent = 0                #sets a flag for use if county vax data not available

gis = GIS()
item = gis.content.get("64d974da1bdd4b7a8a4aa8e83c2d3a49") #census tract


flayer = item.layers[0]


#censusdata = pd.read_csv(censusdatafile)
#print ("dataframe size of censusdata download QC check:")
#print (censusdata.size)

#if censusdata.size > 10:
#print ("checking if I can retrieve census data file. File length is : "+str(len(censusdatafile))

#response = requests.get(censusdatafile)
#print (response)
#if len(response.text)>10000:

#censusdata = pd.read_csv(censusdatafile)

try:
    print (flayer)
    censusdata = flayer.query(where="RptDt > DATE \'2022-09-25\'").sdf  # Note query format for SQL-based data on arcgis hub
    print ("dataframe size of censusdata download QC check:")
    print (censusdata.size)

    print (censusdata.head())
    print (censusdata.dtypes)

    # add a column JUSTDATE to dataframe that just contains the date, formatted with - instead of / separators
    censusdata['RptDt'] = censusdata['RptDt'].astype(str)
    censusdata['JUSTDATE'] = censusdata['RptDt'].str.split(" ").str.get(0)
    print (censusdata['JUSTDATE'].dtype)
    censusdata['JUSTDATE'] = censusdata['JUSTDATE'].astype(str)
    print (censusdata['JUSTDATE'].dtype)
    censusdata['JUSTDATE'] = censusdata['JUSTDATE'].astype(str)

    print (censusdata['JUSTDATE'])
    censusdatacurrent = 1
    #if today in censusdata['JUSTDATE']:
    #    print ("Today's census tract data are available")
    #    censusdatacurrent = 1
    #else:
    #    print ("Today's census tract data are not available")

        #with open('/home/ec2-user/covidtracker/pygeo_heatmap/WI_tracts_GHSarea.txt', 'r') as f:  #change this file name to be your input file
    with open('/home/ec2-user/covidtracker/pygeo_heatmap/WI_tracts_GHSarea.txt', 'r') as f:  #change this file name to be your input file
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            GEOID10 = row[0]
            county = row [1]
            tractFIPS = row [2]
            TotPop  = int(row[3].replace(',',''))
            parameter_entry = [tractFIPS, county, GEOID10, TotPop]
            print (parameter_entry)
            parameters.append(parameter_entry)

    #print parameters

    summary = ""

    output = "County\tTract\tGEOID10\tCases per 100K\n"

    for region in parameters:       # Loop through list of regions to retrieve case counts and compute the rate per 100K
        geoid = str(region[2])
        region_pop = region[3]
        print ("working on ", geoid)
        print (type(geoid))
        # make a dataframe containing just the census tract of interest
        singletractdf = censusdata.loc[censusdata['GEOID'] == geoid]

        print (singletractdf.head())

        current_pos_df = singletractdf.query("JUSTDATE==@today")['POS_CUM_CP']

        print ("current_post_df")
        print (current_pos_df)

        current_pos = current_pos_df.iloc[0]

        weekago_pos_df = singletractdf.query("JUSTDATE==@weekago")['POS_CUM_CP']
        weekago_pos = weekago_pos_df.iloc[0]

        if current_pos == -999:  #error catching for dummy -999 cells in WIDHS data
            current_pos = 0
        if weekago_pos == -999:
            weekago_pos = 0
        #yesterday_pos_df = singletractdf.query("JUSTDATE==@yesterday")['POSITIVE']
        #yesterday_pos = yesterday_pos_df.iloc[0]

        cases_per_100k = round(100000*float(current_pos - weekago_pos)/float(region_pop)/7, 1)
        #print "Region: ", region[0], region[1], region[2]
        #print "Current total: ", current_pos
        #print "7 Days ago total: ", weekago_pos
        #print "7 day increase:",  current_pos - weekago_pos
        #print "Cases per 100,000: ", cases_per_100k
        if cases_per_100k < 0:              # to correct for tracts with no cases or too few for WIDHS to report
            cases_per_100k = 0
        summary = summary + region[0] +"\t Cases per 100,000: " + str(cases_per_100k)+"\n"
        output += region[1] + "\t" + region[0] +"\t" + region[2] + "\t" + str(cases_per_100k) + "\n"
    #print summary
    print (output)

    target = open("/home/ec2-user/covidtracker/pygeo_heatmap/output.txt",'w')
    target.write(output)
    target.close
except Exception:
    print ("failure to retrieve census data")
    censusdatacurrent = 0


#print singletractdf["JUSTDATE"]

#testdate = "2020-10-10"
#postoday = singletractdf.query("JUSTDATE==@testdate")['POSITIVE']
#print singletractdf.JUSTDATE == "2020/09/15"
#print "postoday: "
#print postoday

#postodayval = postoday.iloc[0]

#print "postodayval = ", postodayval


#print date.today()

#countydatafile = "COVID-19_Historical_Data_by_County.csv"
#countydatafile = "https://opendata.arcgis.com/datasets/5374188992374b318d3e2305216ee413_12.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"




countydatafile="https://opendata.arcgis.com/datasets/6496bdf64f7a44bba593862d04d01b2b_12.csv"
#censusdatafile = "heatmap.html"
countydata = pd.read_csv(countydatafile)

countyvaxfile =  "https://opendata.arcgis.com/datasets/d570bd5da98644abbfa01e259777efab_1.csv"
countyvaxdata = pd.read_csv(countyvaxfile)

if countyvaxdata.size > 50:
    countyvaxdatacurrent = 1

#print (countyvaxdata)

print ("Length QC check on county data download:")
print (countydata.size)
# print (countydata)

countydata['JUSTDATE'] = countydata['RptDt'].str.split(" ").str.get(0)
print (countydata['JUSTDATE'].dtype)
countydata['JUSTDATE'] = countydata['JUSTDATE'].astype(str)
print (countydata['JUSTDATE'].dtype)
countydata['JUSTDATE'] = countydata['JUSTDATE'].str.replace("/", "-")  #replacing date separators to match python format

print ("countydata:")
print (countydata.head())
print (countydata.dtypes)

county_results = ""
for county in counties:
    geoid = int(county[1])
    region_pop = county[2]
    print( "working on :", county)
    singlecountydf = countydata.loc[countydata['GEOID'] == geoid]
    print (singlecountydf.head())
    print (singlecountydf)
    current_pos_df = singlecountydf.query("JUSTDATE==@today")['POS_CUM_CP']
    print ("current_pos_df:")
    print (current_pos_df)
    current_pos = current_pos_df.iloc[0]

    weekago_pos_df = singlecountydf.query("JUSTDATE==@weekago")['POS_CUM_CP']
    print ("weekago_pos_df")
    print (weekago_pos_df.head())
    weekago_pos = weekago_pos_df.iloc[0]

    yesterday_pos_df = singlecountydf.query("JUSTDATE==@dayago")['POS_CUM_CP']
    yesterday_pos = yesterday_pos_df.iloc[0]

    cases_per_100k = round(100000*float(current_pos - weekago_pos)/float(region_pop)/7, 1)
    new_cases = current_pos - yesterday_pos

    #get last seven days


    county_week_history = "Daily case counts for past week (most recent first):"+str(new_cases)+", "+str(round(singlecountydf.query("JUSTDATE==@dayago")['POS_NEW_CP'].iloc[0]))+", "+str(round(singlecountydf.query("JUSTDATE==@twodaysago")['POS_NEW_CP'].iloc[0]))+", "+str(round(singlecountydf.query("JUSTDATE==@threedaysago")['POS_NEW_CP'].iloc[0]))+", "+str(round(singlecountydf.query("JUSTDATE==@fourdaysago")['POS_NEW_CP'].iloc[0]))+", "+str(round(singlecountydf.query("JUSTDATE==@fivedaysago")['POS_NEW_CP'].iloc[0]))+", "+str(round(singlecountydf.query("JUSTDATE==@sixdaysago")['POS_NEW_CP'].iloc[0]))+"."

    countyvaxpercentage = "NA"
    if countyvaxdatacurrent == 1:
        print ("working on vaccine data for " + str(geoid))
        print (countyvaxdata)
        countyvaxcomplete = countyvaxdata.query("GEOID==@geoid")['DOSE_COMPLETE_TOTAL']
        countyvaxpopulation = countyvaxdata.query("GEOID==@geoid")['POP']
        countyvaxpercentage = round(100*float(countyvaxcomplete)/float(countyvaxpopulation),1)
    #countyvaxpercentage = "WI DHS not currently reporting"
     #print "Region: ", region[0], region[1], region[2]
    #print "Current total: ", current_pos
    #print "7 Days ago total: ", weekago_pos
    #print "7 day increase:",  current_pos - weekago_pos
    #print "Cases per 100,000: ", cases_per_100k
    if cases_per_100k < 0:              # to correct for tracts with no cases or too few for WIDHS to report
        cases_per_100k = 0
    county_results += "<br>----------------------------------------------"

    county_results += "<br>"+ county[0] + "<br> New Cases today: " + str(new_cases)+ "<br> Total cases in last 7 days: " + str(current_pos-weekago_pos)+"<br>"+county_week_history +"<br>7-day rolling daily average per 100,000: " + str(cases_per_100k)+"<br>Completed Vaccination Rate: " + str(countyvaxpercentage)+"%"

    print (county, current_pos, yesterday_pos, weekago_pos, new_cases, cases_per_100k)



resultshtml = "<h1>La Crosse Region Daily COVIDTracker</h1>"
resultshtml += "<p>Data sources: https://www.dhs.wisconsin.gov/covid-19/data.htm (Updated Mon-Fri)<br>"
resultshtml += "Most recent update: " + str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) +"<br>"

if censusdatacurrent == 0:
    resultshtml += "Most recent update only includes county level data. Census tract level data for map from today not yet available.<br>"
resultshtml += "<iframe src=\"heatmap.html\" width=\"800\" height=\"500\" title=\"covidtracker\"></iframe>"


resultshtml += "<br>View large current heatmap <a href=\"heatmap.html\"> HERE</a><br>"
resultshtml += county_results

print (resultshtml)

targethtml = open("/home/ec2-user/covidtracker/pygeo_heatmap/index.html", 'w')
#targethtml = open("index.html", 'w')
targethtml.write(resultshtml)
targethtml.close()

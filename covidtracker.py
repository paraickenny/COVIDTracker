# Script to retrieve COVID19 case counts by region (e.g. census tract) from WI DHS in order to
# compute 7 day average case rates per 100K in those regions

import urllib
from datetime import date, datetime, timedelta

# Set up a list of regions, their GEOID and population
parameters = []
parameters.append(["La Crosse County", 55063, 114638])
parameters.append(["Census Tract 1, La Crosse County", 55063000100, 4615])
parameters.append(["Census Tract 2, La Crosse County", 55063000200, 4682])
parameters.append(["Census Tract 3, La Crosse County", 55063000300, 2352])
parameters.append(["Census Tract 4, La Crosse County", 55063000400, 6476])
parameters.append(["Census Tract 5, La Crosse County", 55063000500, 4669])
parameters.append(["Census Tract 6, La Crosse County", 55063000600, 2203])
parameters.append(["Census Tract 7, La Crosse County", 55063000700, 4510])
parameters.append(["Census Tract 8, La Crosse County", 55063000800, 3482])
parameters.append(["Census Tract 9, La Crosse County", 55063000900, 3443])
parameters.append(["Census Tract 10, La Crosse County", 55063001000, 3847])
parameters.append(["Census Tract 11.01, La Crosse County", 55063001101, 2004])
parameters.append(["Census Tract 11.02, La Crosse County", 55063001102, 3968])
parameters.append(["Census Tract 12, La Crosse County", 55063001200, 4075])
parameters.append(["Census Tract 101.01, La Crosse County", 55063010101, 5575])
parameters.append(["Census Tract 101.02, La Crosse County", 55063010102, 4793])
parameters.append(["Census Tract 102.01, La Crosse County", 55063010201, 10304])
parameters.append(["Census Tract 102.02, La Crosse County", 55063010202, 6704])
parameters.append(["Census Tract 102.03, La Crosse County", 55063010203, 2173])
parameters.append(["Census Tract 103, La Crosse County", 55063010300, 4543])
parameters.append(["Census Tract 104.01, La Crosse County", 55063010401, 5557])
parameters.append(["Census Tract 104.02, La Crosse County", 55063010402, 9537])
parameters.append(["Census Tract 105, La Crosse County", 55063010500, 5950])
parameters.append(["Census Tract 106, La Crosse County", 55063010600, 3473])
parameters.append(["Census Tract 107, La Crosse County", 55063010700, 5663])
parameters.append(["Census Tract 108, La Crosse County", 55063010800, 3252])

# Determine the relevant days to interrogate for the data
today = str(date.today())
weekago = str(date.today() - timedelta(days=7))
dayago = str(date.today() - timedelta(days=1))
eightdaysago = str(date.today() - timedelta(days=8))

summary = ""

def getpositive(input):         #function to extract number of positive test results from text string from server
    text = input
    a = text.split('"POSITIVE":')
    number = int(filter(str.isdigit, str(a[1])))    # This isolates the case number from the long text string
    return number

for region in parameters:       # Loop through list of regions to retrieve case counts and compute the rate per 100K
    geoid = str(region[1])
    region_pop = region[2]

    #Assemble the URL to retrieve current and 7 day old case count from  the DHS database
    current_url = "https://dhsgis.wi.gov/server/rest/services/DHS_COVID19/COVID19_WI/FeatureServer/10/query?where=DATE%20%3E%3D%20TIMESTAMP%20%27" + dayago + "%2000%3A00%3A00%27%20AND%20DATE%20%3C%3D%20TIMESTAMP%20%27" + today + "%2000%3A00%3A00%27%20AND%20GEOID%20%3D%20%27" + geoid + "%27&outFields=POSITIVE&outSR=4326&f=json"
    weekago_url = "https://dhsgis.wi.gov/server/rest/services/DHS_COVID19/COVID19_WI/FeatureServer/10/query?where=DATE%20%3E%3D%20TIMESTAMP%20%27" + eightdaysago + "%2000%3A00%3A00%27%20AND%20DATE%20%3C%3D%20TIMESTAMP%20%27" + weekago + "%2000%3A00%3A00%27%20AND%20GEOID%20%3D%20%27" + geoid + "%27&outFields=POSITIVE&outSR=4326&f=json"

    weboutput_current = urllib.urlopen(current_url).read()
    weboutput_weekago = urllib.urlopen(weekago_url).read()

    current_pos = getpositive(weboutput_current)
    weekago_pos = getpositive(weboutput_weekago)
    cases_per_100k = round(100000*float(current_pos - weekago_pos)/float(region_pop)/7, 2)
    print "Region: ", region[0]
    print "Current total: ", current_pos
    print "7 Days ago total: ", weekago_pos
    print "7 day increase:",  current_pos - weekago_pos
    print "Cases per 100,000: ", cases_per_100k

    summary = summary + region[0] +"\t Cases per 100,000: " + str(cases_per_100k)+"\n"

print summary



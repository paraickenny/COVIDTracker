import geopandas as gpd
import os
import numpy as np

#La Crosse census tract file
tracts1 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55063_tract10.zip')

print (tracts1)
#Trempealeau census tract file
tracts2 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55121_tract10.zip')
tracts3 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55001_tract10.zip')
tracts4 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55011_tract10.zip')
tracts5 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55023_tract10.zip')
tracts6 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55043_tract10.zip')
tracts7 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55053_tract10.zip')
tracts8 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55057_tract10.zip')
tracts9 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55081_tract10.zip')
tracts10 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55103_tract10.zip')
tracts11 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55123_tract10.zip')
tracts12 = gpd.read_file('zip://'+'/home/ec2-user/covidtracker/pygeo_heatmap/tl_2010_55077_tract10.zip')

print (tracts2)

tracts = tracts1
tracts = tracts.append(tracts2)
tracts = tracts.append(tracts3)
tracts = tracts.append(tracts4)
tracts = tracts.append(tracts5)
tracts = tracts.append(tracts6)
tracts = tracts.append(tracts7)
tracts = tracts.append(tracts8)
tracts = tracts.append(tracts9)
tracts = tracts.append(tracts10)
tracts = tracts.append(tracts11)
tracts = tracts.append(tracts12)


print (tracts)

#tracts = gpd.read_file('zip://'+'tl_2010_01_tract10.zip')

tracts.crs = {'datum': 'NAD83', 'ellps': 'GRS80', 'proj':'longlat', 'no_defs':True}

# print (tracts)

print (tracts.head(2))

headers = tracts.columns.tolist()

print (headers)

# tl_2010_55063_tract00.zip

#district23 = congr_districts[ congr_districts.GEOID == '5503' ]  # 36 = NY, 23 = District
tract_1 = tracts[ tracts.GEOID10 == '55063000100' ]
tract_2 = tracts[ tracts.GEOID10 == '55063000200' ]
tract_3 = tracts[ tracts.GEOID10 == '55063000300' ]
tract_4 = tracts[ tracts.GEOID10 == '55063000400' ]
tract_5 = tracts[ tracts.GEOID10 == '55063000500' ]

# convert it to the projection of our folium openstreetmap
tract_1 = tract_1.to_crs({'init':'epsg:3857'})
tract_2 = tract_2.to_crs({'init':'epsg:3857'})
tract_3 = tract_3.to_crs({'init':'epsg:3857'})
tract_4 = tract_4.to_crs({'init':'epsg:3857'})
tract_5 = tract_5.to_crs({'init':'epsg:3857'})


import pandas as pd
import folium
from folium.plugins import HeatMap

#for_map = pd.read_csv('campaign_contributions_for_map.tsv', sep='\t')
#for_map = pd.read_csv('covid.tsv', sep='\t')

#for_map = pd.read_csv('test_cities.tsv', sep='\t')
for_map = pd.read_csv('/home/ec2-user/covidtracker/pygeo_heatmap/output.txt', sep='\t')


#max_amount = float(for_map['Amount'].max())
max_amount = float(for_map['Cases per 100K'].max())

hmap = folium.Map(location=[43.816151, -91.264671], zoom_start=8, )

# convert the GEOID10 field in for_map dataframe from int64 to string to allow merge
for_map['GEOID10'] = for_map['GEOID10'].astype(str)

merged_table = for_map.merge(tracts, on="GEOID10")

print ("merged_table:")
print (merged_table.head(2))
print (merged_table.dtypes)
"""
hm_wide = HeatMap( list(zip(for_map.lat.values, for_map.lon.values, for_map.Amount.values)),
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=17, blur=15,
                   max_zoom=1,
                 )
"""
print ("for_map:")
print (for_map.head(2))
print (for_map.dtypes)
"""
folium.GeoJson(tract_1).add_to(hmap)
folium.GeoJson(tract_2).add_to(hmap)
folium.GeoJson(tract_3).add_to(hmap)
folium.GeoJson(tract_4).add_to(hmap)
folium.GeoJson(tract_5).add_to(hmap)
"""
"""
hmap.add_child(hm_wide)
"""
merged_table['GEOID10'] = merged_table['GEOID10'].astype(int)

merged_table2 = gpd.GeoDataFrame(merged_table, geometry = merged_table.geometry)
merged_table2.crs = {'datum': 'NAD83', 'ellps': 'GRS80', 'proj':'longlat', 'no_defs':True}

listofcasenumbers = merged_table2["Cases per 100K"]
highestcasenumber =int(listofcasenumbers.max())+5

#threshold_scale = [0,5,10,25,50,highestcasenumber]
# generate choropleth map

upperlimit = 200
if highestcasenumber > upperlimit:
    upperlimit = highestcasenumber + 1

hmap.choropleth(
    geo_data=merged_table2,
    data=merged_table2,
    columns=['GEOID10', 'Cases per 100K'],
    key_on='feature.properties.GEOID10',
    fill_color='YlOrRd',
    fill_opacity=0.6,
    threshold_scale = [0,5,10,25,50 ,upperlimit],
    line_opacity=1,
    legend_name='New Cases per 100K (rolling 7-day average)',
    smooth_factor=0
    )

folium.GeoJson(merged_table2, name = "covidtracker",
        style_function = lambda x: {"weight":1
            , "color":  '#545453'
            },
        highlight_function =lambda x: {'weight':3, 'color':'black', 'fillOpacity':0.2},
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Cases per 100K'])).add_to(hmap)



#hmap.choropleth.add_child(folium.feature.GeoJsonTooltip(['Cases per 100K'], labels=False)

#to save heatmap to file

hmap.save(os.path.join('/home/ec2-user/covidtracker/pygeo_heatmap/results', 'heatmap.html'))

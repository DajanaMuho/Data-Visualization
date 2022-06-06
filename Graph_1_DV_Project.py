# DATASET Source - https://www.dhs.gov/immigration-statistics/yearbook/2020
import warnings

warnings.filterwarnings("ignore")
import os
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import altair as alt
from vega_datasets import data
from altair import datum
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

geolocator = Nominatim(user_agent='b@yahoo.com')

path = os.getcwd()
ds_1 = pd.read_excel(path + '/datasets/fy2020_table3.xlsx', sheet_name='Table 3')

# Add manually USA for visualization purposes in CSV, so there was a row named Total, just changed to USA
ds_1.columns = ds_1.columns.astype(str)
ds_1['Latitude'] = np.array(0)
ds_1['Longitude'] = np.array(0)
ds_1['Color'] = np.array(0)
ds_1['x'] = np.array(0)
ds_1['y'] = np.array(0)
years = ds_1.columns[1:11].values  # Remove Region
regions = ds_1['Region'].values
color_map = {
    'Africa': '#71C2B9',
    'Asia': '#FAAF6E',
    'Australia': '#BDBEC2',
    'Canada': '#FA9182',
    'Europe': '#9BCD78',
    'South America': '#FFC25C',
    'US': '#000000'
}


def get_value(col_condition, col_name, filter_col='Region', df=ds_1):
    return df[df[filter_col] == col_condition][col_name].values[0]


def geolocate(country):
    loc = geolocator.geocode(country)
    return loc.latitude, loc.longitude


def update_ds():
    i_loop = 0
    for region in regions:
        name = geolocate(region)
        ds_1['Latitude'].loc[i_loop] = name[0]
        ds_1['Longitude'].loc[i_loop] = name[1]
        ds_1['Color'].loc[i_loop] = color_map[region]
        ds_1['x'].loc[i_loop] = get_value(region, 'Latitude')
        ds_1['y'].loc[i_loop] = get_value(region, 'Longitude')
        i_loop += 1


update_ds()

# -------------------------------- GRAPH 1 MAP CHART -------------------------------------#
# PERSONS OBTAINING LAWFUL PERMANENT RESIDENT STATUS BY REGION AND COUNTRY OF BIRTH: FISCAL YEAR 2020

source = alt.topo_feature(data.world_110m.url, 'countries')
sphere = alt.sphere()

background = alt.Chart(sphere).mark_geoshape(fill='lightblue')

continents_map = alt.Chart(source).mark_geoshape(fill='#FADDCB', stroke="black", strokeWidth=0.15)

lines = {}
points = {}
for i in ds_1.loc[ds_1.index != 0].index:
    lines[i] = alt.Chart(ds_1.loc[(ds_1.index == 0) | (ds_1.index == i)]).mark_trail() \
        .encode(
        longitude='y',
        latitude='x',
        size=alt.Size('2020:N', scale=alt.Scale(range=[1,10]), legend=None),
        color=alt.value(color_map[ds_1['Region'].loc[i]]),
    )
    points[i] = alt.Chart(ds_1.loc[(ds_1.index == 0) | (ds_1.index == i)]).mark_circle().encode(
        longitude='y',
        latitude='x',
        size=alt.Size(
            '2020:Q',
            scale=alt.Scale(range=[0, ds_1['2020'].loc[i] / 50]),
            legend=None
        ),
        color=alt.value(color_map[ds_1['Region'].loc[i]]),
        tooltip='Region',
    ).transform_filter(
        (datum.Region != 'US')
    )


ds_1.Latitude[ds_1.Region == 'US'] = 43.78373  # Change just to align the text in a proper position

text_us = alt.Chart(ds_1).mark_text(
    align='center',
    fontSize=12,
    fontWeight='bold',
    color='#234854',
    lineBreak=r'\n',
).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    text=alt.Text('Text:N')
).transform_filter(
    (datum.Region == 'US')
)

text_numbers = alt.Chart(ds_1).mark_text(
    align='center',
    baseline='middle',
    color='#234854',
    fontWeight='bold',
    fontSize=12,
).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    text=alt.Text('2020:Q', format=",.0f"),
).transform_filter(
    (datum.Region != 'US')
)
layer = alt.layer(background, continents_map,
                  lines[1], lines[2], lines[3], lines[4], lines[5], lines[6],
                  points[1], points[2], points[3], points[4], points[5], points[6],
                  text_us, text_numbers,
                  ).project('naturalEarth1') \
    .properties(
    width=1000,
    height=500,
    title='Flow Of Immigrants to U.S By Place Of Origin, 2020'
).configure_view(stroke=None)
layer.save('world_map.html')

print('Check html file')

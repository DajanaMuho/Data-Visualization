# DATASET Source - https://www.dhs.gov/immigration-statistics/yearbook/2020
import warnings

warnings.filterwarnings("ignore")
import os
import pandas as pd
from geopy.geocoders import Nominatim
import altair as alt
from vega_datasets import data


geolocator = Nominatim(user_agent='dmuho@gradcenter.cuny.edu')

path = os.getcwd()
#ds = pd.read_excel(path + '/datasets/fy2020_table4 _transposed.xlsx', sheet_name='Table 4')
ds = pd.read_excel(path + '/output.xlsx') #Generated from table 4
states = alt.topo_feature(data.us_10m.url, feature='states')

input_dropdown = alt.binding_select(options=list(ds.Year.unique()), name='Choose Year: ')
selector = alt.selection_single(fields=['Year'], bind=input_dropdown, init={'Year': 2011})

base = alt.Chart(states).mark_geoshape(fill='lightgray', stroke='black', strokeWidth=0.5)

chart = alt.Chart(ds).mark_geoshape(stroke='black').encode(
    color='Immigrants:Q',
    tooltip=['State:N', 'Immigrants:Q'],
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(states, key='id', fields=['geometry', 'type'])
).add_selection(
    selector
).transform_filter(
    selector
).properties(
    width=700,
    height=400,
    projection={'type': 'albersUsa'},
    title='Where Immigrants Live In The U.S ?'
)
layer = base + chart
layer = layer.configure_view(stroke=None).configure_title(fontSize=20)

layer.save('us_map.html')
print('done')


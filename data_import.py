import pandas as pd
import folium
from folium.plugins import MarkerCluster

df = pd.read_csv('climate_policy_database_policies_export.csv')

print(df.head())
print(len(df))
print(df.columns)
print(df['country'].unique())

us_policy = df[df['country']=='United States of America']

print(len(us_policy))

print(us_policy.columns)
print(us_policy['subnational_region'].unique())

# Assign lat and long based on state name
state_lat_long = {
    'Alabama': (32.806671, -86.791130),
    'Alaska': (61.370716, -152.404419),
    'Arizona': (33.729759, -111.431221),
    'Arkansas': (34.969704, -92.373123),
    'California': (36.116203, -119.681564),
    'Colorado': (39.059811, -105.311104),
    'Connecticut': (41.597782, -72.755371),
    'Delaware': (39.318523, -75.507141),
    'Florida': (27.766279, -81.686783),
    'Georgia': (33.040619, -83.643074),
    'Hawaii': (21.094318, -157.498337),
    'Idaho': (44.240459, -114.478828),
    'Illinois': (40.349457, -88.986137),
    'Indiana': (39.849426, -86.258278),
    'Iowa': (42.011539, -93.210526),
    'Kansas': (38.526600, -96.726486),
    'Kentucky': (37.668140, -84.670067),
    'Louisiana': (31.169546, -91.867805),
    'Maine': (44.693947, -69.381927),
    'Maryland': (39.063946, -76.802101),
    'Massachusetts': (42.230171, -71.530106),
    'Michigan': (43.326618, -84.536095),
    'Minnesota': (45.694454, -93.900192),
    'Mississippi': (32.741646, -89.678696),
    'Missouri': (38.456085, -92.288368),
    'Montana': (46.921925, -110.454353),
    'Nebraska': (41.125370, -98.268082),
    'Nevada': (38.313515, -117.055374),
    'New Hampshire': (43.452492, -71.563896),
    'New Jersey': (40.298904, -74.521011),
    'New Mexico': (34.840515, -106.248482),
    'New York': (42.165726, -74.948051),
    'North Carolina': (35.630066, -79.806419),
    'North Dakota': (47.528912, -99.784012),
    'Ohio': (40.388783, -82.764915),
    'Oklahoma': (35.565342, -96.928917),
    'Oregon': (44.572021, -122.070938),
    'Pennsylvania': (40.590752, -77.209755),
    'Rhode Island': (41.680893, -71.511780),
    'South Carolina': (33.856892, -80.945007),
    'South Dakota': (44.299782, -99.438828),
    'Tennessee': (35.747845, -86.692345),
    'Texas': (31.054487, -97.563461),
    'Utah': (40.150032, -111.862434),
    'Vermont': (44.045876, -72.710686),
    'Virginia': (37.769337, -78.169968),
    'Washington': (47.400902, -121.490494),
    'West Virginia': (38.491226, -80.954481),
    'Wisconsin': (44.268543, -89.616508),
    'Wyoming': (42.755966, -107.302490)
}

us_policy['lat'] = us_policy['subnational_region'].map(lambda x: state_lat_long[x][0] if x in state_lat_long else None)
us_policy['lon'] = us_policy['subnational_region'].map(lambda x: state_lat_long[x][1] if x in state_lat_long else None)

# Print the number of policies per subnational region
print(us_policy['subnational_region'].value_counts())

# Print the number of policies per sector
print(us_policy['sector'].value_counts())

us_policy = us_policy.dropna(subset=['lat', 'lon'])
# Create map with count of policies per subnational region

# Create a base map
us_map = folium.Map(location=[48, -102], zoom_start=3)

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(us_map)

# Loop through the dataset and add each point to the mark cluster
for i in range(0, len(us_policy)):
    lat = us_policy.iloc[i]['lat']
    long = us_policy.iloc[i]['lon']
    radius=5
    popup_text = """Policy name: {}<br>
                Subnational region: {}<br>
                Sector: {}<br>"""
    popup_text = popup_text.format(us_policy.iloc[i]['policy_name'],
                               us_policy.iloc[i]['subnational_region'],
                               us_policy.iloc[i]['sector'])
    folium.CircleMarker(location = [lat, long], radius=radius, popup=popup_text, fill=True).add_to(marker_cluster)

# Display the map
us_map.save('us_policy.html')

# Create map with count of policies per sector


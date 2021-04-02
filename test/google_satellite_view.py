API_key = "AIzaSyB3cnuHVDqgkccmk5teRruYz1LD_6Shkm0"

# https://pypi.org/project/google-streetview/
# Import google_streetview for the api module

import requests 
import pandas
from image_extraction import StreetViewer

df = pandas.read_csv('parcels.csv')
# print(df.columns)
df['input'] = df.latitude.astype(str) + ',' + df.longitude.astype(str)

test = StreetViewer(API_key, df["input"].iloc[0])
test.get_pic()

# print(df.input.head)

# for i in range(len(df)): 
#     center = df.input.iloc[i]

# print(len(df))

# for i in range(0,2):
#     center = df['input'].iloc[i]
#     print(center)
#     params = [{
#         # 'size': '600x300', # max 640x640 pixels
#         # 'zoom' : '20',
#         # 'maptype' : 'satellite',
#         'center': center,
#         'key' : API_key
#     }] 

#     # Create a results object
#     response = requests.get('https://maps.googleapis.com/maps/api/staticmap?size=600x300&zoom=20&maptype=satellite', params)

#     # Download images to directory 'downloads'
#     response.download_links('downloads')
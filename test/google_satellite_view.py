API_key = "AIzaSyB3cnuHVDqgkccmk5teRruYz1LD_6Shkm0"

# https://pypi.org/project/google-streetview/
# Import google_streetview for the api module

# http://maps.googleapis.com/maps/api/staticmap?sensor=false&size=640x400&maptype=satellite&visible=29.64,-13.09&visible=27.38,-18.53&markers=color:red%7Ccolor:red%7Clabel:A%7C27.38,-18.53&markers=color:red%7Ccolor:red%7Clabel:B%7C29.64,-13.09

import requests 
import pandas
from image_extraction import StreetViewer
# f = open('parcels.csv')

# def CalculateBoundsZoomLevel(self, bounds, view_size):
#     """Given lat/lng bounds, returns map zoom level.

#     This method is used to take in a bounding box (southwest and northeast 
#     bounds of the map view we want) and a map size and it will return us a zoom 
#     level for our map.  We use this because if we take the bottom left and 
#     upper right on the map we want to show, and calculate what pixels they 
#     would be on the map for a given zoom level, then we can see how many pixels 
#     it will take to display the map at this zoom level.  If our map size is 
#     within this many pixels, then we have the right zoom level.

#     Args:
#       bounds: A list of length 2, each holding a list of length 2. It holds
#         the southwest and northeast lat/lng bounds of a map.  It should look 
#         like this: [[southwestLat, southwestLng], [northeastLat, northeastLng]]
#       view_size: A list containing the width/height in pixels of the map.

#     Returns:
#       An int zoom level.
#     """
#     zmax = 18
#     zmin = 0
#     bottom_left = bounds[0]
#     top_right = bounds[1]
#     backwards_range = range(zmin, zmax)
#     backwards_range.reverse()
#     for z in backwards_range:
#       bottom_left_pixel = self.FromLatLngToPixel(bottom_left, z)
#       top_right_pixel = self.FromLatLngToPixel(top_right, z)
#       if bottom_left_pixel.x > top_right_pixel.x :
#         bottom_left_pixel.x -= self.CalcWrapWidth(z)
#       if abs(top_right_pixel.x - bottom_left_pixel.x) <= view_size[0] \
#           and abs(top_right_pixel.y - bottom_left_pixel.y) <= view_size[1] :
#         return z
#     return 0





df = pandas.read_csv('parcels.csv')
print(df.columns)
df['nw'] = df.max_latitude.astype(str) + ',' + df.max_longitude.astype(str)
df['se'] = df.min_latitude.astype(str) + ',' + df.min_longitude.astype(str)
df['center'] = (df.max_latitude - ((df.max_latitude - df.min_latitude)/2)).astype(str) + ',' + (df.max_longitude - ((df.max_longitude - df.min_longitude)/2)).astype(str)
# df['input_1'] = df.max_latitude.astype(str) + ',' + df.max_longitude.astype(str)+ ',' +df.min_latitude.astype(str) + ',' + df.min_longitude.astype(str)


# df['input_lat'] = [df.min_latitude] + [df.min_longitude]
# df['input_long'] = [df.max_latitude]+[df.max_longitude]

# test = StreetViewer(API_key, df["input"].iloc[0])
# test.get_pic()

# print(df.head)

# for i in range(len(df)): 
#     lat = df.input_lat.iloc[i]

print(df.shape)

for i in range(0,2):
    # center = df['input'].iloc[i]
    # print(center)
    # input1 = df['input_1'].iloc[i]
    # long = df['input_2'].iloc[i]
    nw = df['nw'].iloc[i]
    se = df['se'].iloc[i]
    vis = nw + se
    center = df['center'].iloc[i]

    params = {
        'size': '600x400', # max 640x640 pixels
        # 'zoom' : '20',
        'markers' : 'icon%3Ahttp%3A%2F%2Fwww.google.com%2Fmapfiles%2Farrow.png',
        'maptype' : 'satellite',
        'center' : center,
        'visible' : vis, 
        'key' : API_key
    }

    # Create a results object
    response = requests.get('https://maps.googleapis.com/maps/api/staticmap?size=600x300&zoom=20&maptype=satellite', params)

    # Download images to directory 'downloads'
    # response.download_links('downloads')
    print(response.url)
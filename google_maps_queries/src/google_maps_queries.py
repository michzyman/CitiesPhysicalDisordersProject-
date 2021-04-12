from secrets import API_KEY

from PIL import Image, ImageDraw

import requests 
import shutil
import math
import pandas

def coordinate_length_to_zoom(length):
  return -math.log(length/419.4304, 2)

def zoom_to_coordinate_length(zoom):
  return 2**(-zoom) * 419.4304

def get_zoom_and_masks(min_latitude, max_latitude, min_longitude, max_longitude):
  lat_length, lon_length = max_latitude - min_latitude, max_longitude - min_longitude

  # Find the appropriate Zoom for latitude/longitude
  lat_desired_zoom = coordinate_length_to_zoom(lat_length)
  lon_desired_zoom = coordinate_length_to_zoom(lon_length)

  # Choose the smaller of the two and round down (API takes only whole numbers for zoom)
  actual_zoom = math.floor(min(lat_desired_zoom, lon_desired_zoom))
  actual_zoom_length = zoom_to_coordinate_length(actual_zoom)

  lat_mask = ((actual_zoom_length - lat_length) / actual_zoom_length) / 2
  lon_mask = ((actual_zoom_length - lon_length) / actual_zoom_length) / 2

  return actual_zoom, lat_mask, lon_mask

def mask_image(filename, lat_mask, lon_mask):
  image = Image.open(filename).convert("RGB")

  draw = ImageDraw.Draw(image)
  draw.rectangle(((0,0), (300,300*lon_mask)), fill='black')
  draw.rectangle(((0,300), (300,300 - max(lon_mask,0.05)*300)), fill='black')
  draw.rectangle(((0,0), (300*lat_mask,300)), fill='black')
  draw.rectangle(((300,0), (300 - 300*lat_mask,300)), fill='black')
  
  image.save(filename, 'PNG')

def download_images_from_csv(filename):
  df = pandas.read_csv(filename)

  for _, row in df.iterrows():
      center = '{},{}'.format((row['max_latitude'] + row['min_latitude'])/2, (row['max_longitude'] + row['min_longitude'])/2)

      zoom, lat_mask, lon_mask = get_zoom_and_masks(row['min_latitude'], row['max_latitude'], row['min_longitude'], row['max_longitude'])

      params = {
          'size': '{}x{}'.format(300, 300),
          'zoom': zoom,
          'markers' : 'icon%3Ahttp%3A%2F%2Fwww.google.com%2Fmapfiles%2Farrow.png',
          'maptype' : 'satellite',
          'center' : center,
          'key' : API_KEY
      }

      response = requests.get('https://maps.googleapis.com/maps/api/staticmap', params, stream=True)

      category = row['category'].upper().replace(' ', '_')
      address = row['address'].replace(' ', '_')

      filename = 'output/{}/{}.png'.format(category, address)

      with open(filename, 'wb') as output_file:
        shutil.copyfileobj(response.raw, output_file)

      mask_image(filename, lat_mask, lon_mask)

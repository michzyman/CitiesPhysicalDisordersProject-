from secrets import API_KEY

from PIL import Image, ImageDraw

import requests 
import shutil
import math
import pandas

IMG_RES = 224

def zoom_to_coordinate_length(zoom):
  """
  Gives the "coordinate length" covered by a particular Google Maps API zoom
  level where "coordinate length" is defined as the difference between the
  maximum and minimum longitude/latitude

  e.g. zoom level 20 covers a .004 coordinate length

  Each zoom level covers half the distance of the previous zoom level.
  The constant, 1.3981, was approximated by measuring test images.
  """
  return 2**(-zoom) * 1.3981 * IMG_RES

def coordinate_length_to_zoom(length):
  """
  Inverses zoom_to_coordinate_length; gives zoom level for a particular
  coordinate length
  """
  return -math.log(length/(1.3981 * IMG_RES), 2)

def get_zoom_and_masks(min_lat, max_lat, min_lon, max_lon):
  """
  Calculates appropriate zoom level for Google Maps API given rectangular coordinate
  boundaries of an area
  """
  # Calculate the longitudinal and latitudinal distance that needs to be covered
  lat_length, lon_length = max_lat - min_lat, max_lon - min_lon

  # Approxiate the Zoom level for the larger coordinate length
  zoom = coordinate_length_to_zoom(min(lat_length, lon_length))

  # Zoom levels must be integers, so round down to avoid cutting anything off
  zoom = math.floor(zoom)

  # Calculate what fraction of the total distance covered at this zoom level is
  # outside of the target area; used for later masking
  length_covered = zoom_to_coordinate_length(zoom)
  lat_mask = ((length_covered - lat_length) / length_covered)
  lon_mask = ((length_covered - lon_length) / length_covered)

  return zoom, lat_mask, lon_mask

def mask_image(filename, lat_mask, lon_mask):
  image = Image.open(filename).convert("RGB")

  # Half of each mask will be applied on either side of the image
  lat_mask /= 2
  lon_mask /= 2

  draw = ImageDraw.Draw(image)

  # Top mask
  draw.rectangle(((0, 0), (IMG_RES, IMG_RES * lon_mask)), fill='black')

  # Bottom mask (at least 15px to cover Google watermark)
  draw.rectangle(((0, IMG_RES), (IMG_RES, IMG_RES - max(lon_mask, 15/IMG_RES) * IMG_RES)), fill='black')

  # Left mask
  draw.rectangle(((0, 0), (IMG_RES * lat_mask, IMG_RES)), fill='black')

  # Right mask
  draw.rectangle(((IMG_RES, 0), (IMG_RES - IMG_RES * lat_mask, IMG_RES)), fill='black')
  
  image.save(filename, 'PNG')

def download_images_from_csv(filename):
  df = pandas.read_csv(filename)

  for _, row in df.iterrows():
      max_lat, min_lat, max_lon, min_lon = (
        row['max_latitude'],
        row['min_latitude'],
        row['max_longitude'],
        row['min_longitude']
      )

      center = '{},{}'.format((max_lat + min_lat) / 2, (max_lon + min_lon) / 2)

      zoom, lat_mask, lon_mask = get_zoom_and_masks(min_lat, max_lat, min_lon, max_lon)

      params = {
          'size': '{}x{}'.format(IMG_RES, IMG_RES),
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
        print('downloaded {}...'.format(filename))

      mask_image(filename, lat_mask, lon_mask)
      print('masked {}...'.format(filename))

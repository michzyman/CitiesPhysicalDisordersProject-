import math
import requests
import pandas as pd

def rads_to_degrees(rads):
  return rads*57.29578

def wgs84_to_lat_lon(x,y):
  """
  The Hartford data uses WGS84 coordinates on a Mercator projection. These formulas come from page 44
  of the following book: https://pubs.usgs.gov/pp/1395/report.pdf. I calculated R by hand using the
  longitude/latitude of a known location and the provided WGS84 coordinates for that location.
  """

  R = 6378138.96443
  lat = (math.pi/2) - 2 * math.atan(math.e**(-y/R))
  lon = x/R

  return rads_to_degrees(lat), rads_to_degrees(lon)

def get_parcel_spatial_info(address):
  url_endpoint = 'https://gis1.hartford.gov/arcgis/rest/services/AddressPT_Locator_v105/GeocodeServer/findAddressCandidates'
  params = { 'f': 'pjson', 'Single Line Input':address, 'outSR':'{"wkid":102100,"latestWkid":3857}'}

  return requests.get(url_endpoint, params=params, timeout=5).json()

def get_parcel_category(location):
  url_endpoint = 'https://gis1.hartford.gov/arcgis/rest/services/AllCitySurvey2019Parcels/MapServer/0/query'
  params = {
    'f': 'pjson',
    'returnGeometry': 'true',
    'spatialRel': 'esriSpatialRelIntersects',
    'geometry':str(location),
    'geometryType': 'esriGeometryPoint',
    'inSR':102100,
    'outFields':'*',
    'outSR':102100,
    'featureEncoding':'esriDefault'
  }
  
  response = requests.get(url_endpoint, params=params, timeout=5)
  survey = response.json()

  return survey['features'][0]['attributes']['LovelandSurveyOriginal_category']

def get_parcel_data(address):
  spatial_info = get_parcel_spatial_info(address)

  if spatial_info['candidates'] == []:
    return None

  location = spatial_info['candidates'][0]['location']

  return wgs84_to_lat_lon(location['x'], location['y']), get_parcel_category(location)

def read_parcels_from_csv(filename):
  addresses = pd.read_csv(filename, usecols=['STREETNUM', 'STREETNAME', 'STREETTYPE'])
  addresses = addresses.dropna(axis=0, how='any')

  output = pd.DataFrame(columns=['latitude', 'longitude', 'category'])

  for _,row in addresses.iterrows():
    address = '{} {} {}'.format(row['STREETNUM'], row['STREETNAME'], row['STREETTYPE'])

    try:
      (lat,lon), category = get_parcel_data(address)

      new_row = {'latitude':lat, 'longitude':lon, 'category':category}
      output = output.append(new_row, ignore_index=True)

      print('added {}...'.format(address))

    except:
      print('failed {}...'.format(address))

  output.to_csv('parcels.csv', index = False)

read_parcels_from_csv('parcel-addresses.csv')

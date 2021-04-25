import math
import requests
import pandas as pd

TIMEOUT = 20

def rads_to_degrees(rads):
  return rads*57.29578

def wgs84_to_lat_lon(x,y):
  """
  Hartford GIS data uses WGS84 coordinates on a Mercator projection. These formulas come from page 44
  of the following textbook. I calculated R by hand using the longitude/latitude of a known location
  and the provided WGS84 coordinates for that location.
  https://pubs.usgs.gov/pp/1395/report.pdf
  """

  R = 6378138.96443
  lat = (math.pi/2) - 2 * math.atan(math.e**(-y/R))
  lon = x/R

  return rads_to_degrees(lat), rads_to_degrees(lon)

def query_address(address):
  """
  Gives possible parcels in Hartford based on input address
  """

  url_endpoint = 'https://gis1.hartford.gov/arcgis/rest/services/AddressPT_Locator_v105/GeocodeServer/findAddressCandidates'
  params = { 'f': 'pjson', 'Single Line Input':address, 'outSR':'{"wkid":102100,"latestWkid":3857}'}

  return requests.get(url_endpoint, params=params, timeout=TIMEOUT).json()

def query_parcel_survey(location):
  """
  Gives category and geometry for a parcel in the 2019 All-City Hartford Survey
  https://gis1.hartford.gov/Html5Viewer/index.html?viewer=AllCitySurvey2019
  """

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
  
  response = requests.get(url_endpoint, params=params, timeout=TIMEOUT)
  return response.json()

def get_parcel_data(address):
  parcel_candidates = query_address(address)

  if parcel_candidates['candidates'] == []:
    return None

  # Take first parcel; some addresses give multiple candidates that are actually the same parcel
  parcel_location = parcel_candidates['candidates'][0]['location']

  raw_parcel_data = query_parcel_survey(parcel_location)

  if raw_parcel_data['features'] == []:
    return None

  category = raw_parcel_data['features'][0]['attributes']['LovelandSurveyOriginal_category']

  rings = raw_parcel_data['features'][0]['geometry']['rings'][0]

  min_lat, min_lon, max_lat, max_lon = float('inf'), float('inf'), float('-inf'), float('-inf')

  for coordinates in rings:
    lat, lon = wgs84_to_lat_lon(coordinates[0], coordinates[1])

    min_lat = lat if lat < min_lat else min_lat
    max_lat = lat if lat > max_lat else max_lat
    min_lon = lon if lon < min_lon else min_lon
    max_lon = lon if lon > max_lon else max_lon

  return {
    'address': address,
    'min_latitude': min_lat,
    'max_latitude': max_lat,
    'min_longitude': min_lon,
    'max_longitude': max_lon,
    'category': category
  }

def read_parcels_from_csv(filename):
  addresses = pd.read_csv(filename, usecols=['FULL_ADDRESS'])
  addresses = addresses.dropna(axis=0, how='any')
  addresses = addresses.drop_duplicates(subset=['FULL_ADDRESS'])

  output = pd.DataFrame(columns=
    [
    'address',
    'min_latitude',
    'max_latitude',
    'min_longitude',
    'max_longitude',
    'category'
    ]
  )

  for _,row in addresses.iterrows():
    address = row['FULL_ADDRESS']

    parcel_data = get_parcel_data(address)

    if parcel_data:
      output = output.append(parcel_data, ignore_index=True)
      print('added {}...'.format(address))
    else:
      print('failed {}...'.format(address))

  output.to_csv('parcels.csv', index=False)

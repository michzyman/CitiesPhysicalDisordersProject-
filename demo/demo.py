import sys
sys.path.insert(0, '../parcel_info_collection/src')
sys.path.insert(0, '../google_maps_queries/src')

from parcel_info_collection import read_parcels_from_csv
from google_maps_queries import download_images_from_csv

print('----- Generating geometric info and survey categories from parcel addresses -----')
read_parcels_from_csv('demo_addresses.csv')
print()

print('------ Downloading and masking images via Google Maps API -----')
download_images_from_csv('parcels.csv')
print()

print('----- Starting Flask app -----')
#sys.path.insert(0, '../../frontend/src')
#import app

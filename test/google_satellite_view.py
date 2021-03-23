# https://pypi.org/project/google-streetview/
# Import google_streetview for the api module

import requests
import pandas

df = pandas.read_csv('params.csv')

print(df)

with open('params.txt',  mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        centers = (f'\t{row["latitude"]} , {row["longitude"]} ')
        print(centers)
        line_count += 1
    print(f'Processed {line_count} lines.') 



params = [{
	'size': '600x300', # max 640x640 pixels
    'zoom' : '20',
    'maptype' : 'satellite',
    'center': center,
	'key' : 'AIzaSyB3cnuHVDqgkccmk5teRruYz1LD_6Shkm0'
}] 

# Create a results object
response = request.get('https://maps.googleapis.com/maps/api/staticmap?', params)

# Download images to directory 'downloads'
response.download_links('downloads')
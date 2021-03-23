# https://pypi.org/project/google-streetview/
# Import google_streetview for the api module
import google_streetview.api
import csv 

# Define parameters for street view api
params = [{
	'size': '600x300', # max 640x640 pixels
	'location': '41.76652104910358, -72.6739940448788',
	#'location': '46.414382,10.013988',
	#'latitude':'41.767315735676085',
	#'longituded':'-72.67273680385246' ,
	'heading': '151.78',
	'pitch': '-0.76',
	'key': 'AIzaSyB3cnuHVDqgkccmk5teRruYz1LD_6Shkm0'

}]




# Create a results object
results = google_streetview.api.results(params)

# Download images to directory 'downloads'
results.download_links('downloads')
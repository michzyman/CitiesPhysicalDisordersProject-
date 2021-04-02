# code from: https://elvinouyang.github.io/project/how-to-query-google-street-view-api-with-python/
# Dependencies: requests, json
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class StreetViewer(object):
    def __init__(self, api_key, center, size="640x640", zoom = '20', maptype = 'satellite',
                 folder_directory='./satelliteviews/', verbose=True):
        """
        This class handles a single API request to the Google Static Street View API
        api_key: obtain it from your Google Cloud Platform console
        location: the address string or a (lat, lng) tuple
        size: returned picture size. maximum is 640*640
        folder_directory: directory to save the returned objects from request
        verbose: whether to print the processing status of the request
        """
        # input params are saved as attributes for later reference
        self._key = api_key
        self.center = center
        self.size = size
        self.zoom = zoom
        self.maptype = maptype
        self.folder_directory = folder_directory
        # # call parames are saved as internal params
        # self._meta_params = dict(key=self._key,
        #                         location=self.location)
        self._pic_params = dict(key=self._key,
                               location=self.center,
                               size=self.size,
                               zoom = self.zoom,
                               maptype = self.maptype)
        self.verbose = verbose
    

    def get_pic(self):
        """
        Method to query the StreetView picture and save to local directory
        """
        # define path to save picture and headers
        self.pic_path = "{}pic_{}.jpg".format(
            self.folder_directory, self.center.replace("/", ""))
        self.header_path = "{}header_{}.json".format(
            self.folder_directory, self.center.replace("/", ""))
        # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.verbose:
            print(">>> Picture available, requesting now...")
        self._pic_response = requests.get(
            'https://maps.googleapis.com/maps/api/staticmap?',
            params=self._pic_params)
        self.pic_header = dict(self._pic_response.headers)
        if self._pic_response.ok:
            if self.verbose:
                print(f">>> Saving objects to {self.folder_directory}")
            with open(self.pic_path, 'wb') as file:
                file.write(self._pic_response.content)
            with open(self.header_path, 'w') as file:
                json.dump(self.pic_header, file)
            self._pic_response.close()
            if self.verbose:
                print(">>> COMPLETE!")
        else:
            print(">>> Picture not available in StreetView, ABORTING!")
            
    def display_pic(self):
        """
        Method to display the downloaded street view picture if available
        """
        if self.meta_status == 'OK':
            plt.figure(figsize=(10, 10))
            img=mpimg.imread(self.pic_path)
            imgplot = plt.imshow(img)
            plt.show()
        else:
            print(">>> Picture not available in StreetView, ABORTING!")



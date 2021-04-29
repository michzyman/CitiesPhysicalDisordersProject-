We'd like to give a special thank you to the contributors of [https://github.com/weirdindiankid/CS501-Liberator-Project](https://github.com/weirdindiankid/CS501-Liberator-Project), as this README was in large part modeled after theirs.

# 1. Table Of Contents
1. [Table of Contents](#1-table-of-contents)
2. [Evaluating Physical Disorder in Cities](#2-evaluating-physical-disorder-in-cities)
3. [Why is This Tool Needed](#3-why-is-this-tool-needed)
4. [Future Direction](#4-future-direction)
5. [Overview of Functionality](#5-overview-of-functionality)
6. [Getting Started](#6-getting-started)
7. [Using the Flask App](#7-using-the-flask-app)
8. [Explanation of Code](#8-explanation-of-code)
9. [Resources](#9-resources)

# 2. Evaluating Physical Disorder in Cities
This repository contains a Flask application for determining the vacancy of a lot given its minimum and maximum latitude/longitude as input. The app processes the user input, generates images of the lots utilizing Google Maps Static API, and then predicts the vacancy of those lots via a Convolutional Neural Network. 

Even though lots can be polygons of any shape, our model currently is working with square images that are generated and masked according to the coordinates provided.

In the future, this model could be improved by utilizing images that capture the exact shape of lots, rather than approximating the shapes with rectangles. This would likely involve parsing a GIS Shapefile. In addition, our model does not distinguish vacant structures from occupied structures. In other words, our model defines a vacant lot as a lot containing no structures whatsoever. A model that could distinguish between a vacant lot, a vacant structure, and an occupied structure could be more useful but may require the use of Street View imagery.

![occupied structure](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/occupied.png) ![vacant lot](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/vacant_lot.png) ![vacant structure](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/vacant_structure.png)

_These are examples of the satellite images used as inputs to the convolutional neural network. The first image is an occupied structure, the second is a vacant lot, and the third is a vacant structure. All are images of real lots in in Hartford, Connecticut, and were extracted using the Google Maps Static API._

# 3. Why is This Tool Needed
Vacant and abandoned land is prevalent throughout the United States. Research from [studies](https://doi.org/10.1073/pnas.1718503115) conducted by Columbia University and University of Pennsylvania shows that restoring vacant land decreases firearm violence and crime. However, not all cities maintain comprehensive data of where vacant lots are present. As such, Dr. Jonathan Jay of the Boston University School of Public Health would like to automate the process of locating these lots. That way, city officials can be informed of the existence and location of empty lots, action can be taken to reorganize and rebuild these areas, and future violence can be prevented.

While our model does not yet fully automate the process of locating vacant lots, it is able to somewhat accurately determine the vacancy of a list of lots of interest. Therefore, this model can be seen as a proof-of-concept for the desired end goal.

# 4. Future Direction

## 4.1. Current State
As of right now, our model is able to do the following: 
* Take a CSV containing minimum and maximum latitude/longitude coordinates as input
* Generate images that approximate the boundaries of the lots with rectangular masks
* Classify a lot as being entirely vacant (no structures) or containing at least one structure (with an accuracy of ~94% )

## 4.2. Next Steps
Ideally, this model will eventually be expanded to include the following functionality:
* Take a GIS Shapefile as input
* Generate images of lots that are masked to their exact shape
* Accurately classify lots as being entirely vacant, containing a vacant structure, or containing an occupied structure 

# 5. Overview of Functionality
Our final model operates as a Flask server that provides the following functionality:
1. Provides the user with a CSV file containing an input template
2. Asks the user to upload a completed version of the input CSV that contains the coordinates for their lots of interest
3. Asks the user to provide a Google Maps Static API Key
4. Upon submission, generates images of the lots via the Google Maps Static API, masks those images to better approximate the shape of the lots, and classifies those images using a Tensorflow CNN (using VGG16 as the base)
5. Upon completion, provides the user a CSV download that contains the lot names provided in the input file and their corresponding classifications

Additionally, the code inside hartford_data_gen, while not utilized in the final model, was used to generate the training images (via data from the City of Hartford) which can be downloaded [here](https://drive.google.com/file/d/1_1_MolX4b3kORVZjum7Jp5Roj6IgdeHb/view).

# 6. Getting Started

## 6.1. System Requirements
This project is executed via a Docker container, and therefore should run fine on most systems with a Docker installation; however, the instructions given below have been tested on MacOS 11.2, so please use that OS if you encounter any issues.

Also, please ensure [nothing is running](https://help.extensis.com/hc/en-us/articles/360004935154-Identifying-ports-in-use-on-Mac-and-Windows-Operating-Systems) on port 5000, as it will be needed to run a Flask server.

## 6.2. Installing Git and Cloning the Repository
The first thing that you will need to do in order to run this project is to [install Git](https://github.com/git-guides/install-git). After installation, you are read to [clone the repository](https://github.com/git-guides/git-clone) in [Terminal](https://macpaw.com/how-to/use-terminal-on-mac) with the following console command.

`git clone https://github.com/michzyman/CitiesPhysicalDisordersProject-`

## 6.3. Downloading saved_model
Next, you will need to download [this](https://drive.google.com/file/d/1MeZVs2wut_zAWDisxKNaoUJDhI24aPbw/view?usp=sharing) ZIP file and unzip it in the following location: `application/src/classifier/saved_model`

## 6.3. Installing Docker
In order to be able to use Docker to build the project, [click here](https://docs.docker.com/docker-for-mac/install/) and follow the steps to install Docker. This documentation is for Mac only.

## 6.4. Building and Running the Docker Container
Navigate to the `application` directory in Terminal (`cd <path to project folder>/application`) and run the following Docker commands:

```
docker build -t city-disorders .
docker run -p 5000:5000 city-disorders
```

# 7. Using the Flask app

## 7.1 Download input_template.csv
You should be able to see a button that says download, if you click it, it will download a csv file named input_template.csv. This file contains a template for the CSV format the app takes as input. The second row contains an example of how your data should be formatted. This row can be deleted.

For each lot that should be predicted, add a row and complete all of the columns (name, minimum_latitude, maximum_latitude, minimum_longitude, maximum_longitude). The “name” value can be any arbitrary name used to identify that lot, but it must be unique for each lot. The other columns should be filled with the approximate minimum and maximum latitude/longitude coordinates of the lot.

Save the completed CSV to a known location on your computer.

## 7.2 Loading input_template.csv
Click the “Browse” button and load the CSV file that you just completed.

## 7.3 Google Maps Static API Key 
In the text field, provide an API key that has authorization to query the Google Maps Static API. Steps for acquiring a key can be found [here](https://developers.google.com/maps/premium/apikey/maps-static-apikey). If you are Tania or Dharmesh, you can use our personal key found [here](https://drive.google.com/file/d/19N8zhbAH3InMox-lb90q4_4MTJtyzY-t/view).

## 7.4 Submit
Clicking the submit button will begin the image generation and classification process. There will be no change in the webpage until it is complete, and this may take a considerable amount of time, especially if the input file contains many lots. Upon completion, a file containing the classifications will be downloaded. 

# 8. Explanation of Code

## 8.1. Hartford Data Scraping
`misc/hartford_data_gen/src/parcel_info_collection.py` contains the code we used to gather location and category information from Hartford for generating our training images. This information was sourced from a 2019 City Survey that can be viewed in a GIS interface [here](https://gis1.hartford.gov/Html5Viewer/index.html?viewer=AllCitySurvey2019). We noticed this interface has a search function that allows you to search for the address of a particular lot and see it outlined on the map. We inspected the network query this search function makes and figured out an HTTP request we can make to get location and category information for a lot, given its address.

Unfortunately, the location information give was not in longitudinal/latitudinal coordinates. Instead, it was in the WGS84 coordinate system on a Mercator projection, which varies depending on the scale of the map used. We were able to get formulas from page 44 of [this](https://pubs.usgs.gov/pp/1395/report.pdf) textbook, that can convert WG84 coordinates to longitude/latitude coordinates, given an R value that represents the radius of the spherical representation of the earth chosen for that particular map scale. However, we had no info on what R value was being used for this particular GIS system. We approximated it by getting the center coordinates of a particular lot from the GIS system, getting the longitude/latitude coordinates from the same point in Google Maps, and solving the textbook formulas for R.

Using this information and a [list of Hartford addresses](https://openhartford-hartfordgis.opendata.arcgis.com/datasets/address-points/data?geometry=-72.843%2C41.719%2C-72.523%2C41.809&page=2), we were able to generate a list of the category and location information for thousands of Hartford lots, available [here](https://docs.google.com/spreadsheets/d/1jNROdiK3b9OUrAaUAT3BtaPwoWtAbk71_V4hldIZOfk/edit#gid=1475189330).

## 8.2. Google Maps Satellite Image Generation
The code used to generate the images from the extracted csv file can be found in this repository at `application/src/google_maps_queries/queries.py`. Google Maps Static API was used to get satellite images of the lots. After reading the csv file, a center point is calculated for each of the locations based on the min and max latitude/longitude values. Since the API accepts a center point and "zoom level" for querying images, we had to do a bit of math to query and mask our dataset images to the precise lot locations.

Let the distance covered by a Google Maps API image in terms of longitude/latitude be the "coordinate length" of the image. For instance, a square image that shows the terrain from the longitude line 39.381 to line 39.481 has a latitude length of 0.1. Each zoom level in the Google Maps API shows half the coordinate length of the zoom level before it. For instance, if a 224x224 pixel image at a zoom level of 21 has a coordinate length of 0.1, then a 224x224 pixel image at a zoom level of 20 has a coordinate length of 0.2. Therefore, it must be the case that for some constant X the following formula can give the coordinate length covered:

`2**(-zoom_level) * X * image_resolution`

The inverse of this formula would instead give the appropriate zoom level for a particular coordinate distance:

`-math.log(coordinate_length/(X * image_resolution), 2)`

We were able to calculate X by simply generating an image, measuring the coordinate length it covered on Google Maps, and then plugging the image parameters into the formula above to solve for X. It turns out that `X = 1.3981`.

Because we knew what coordinate length needed to be covered for each image (the difference betwen either the min and max longitude or min and max latitude), we could use that second formula to get an appropriate zoom level, and then round down because zoom levels have to be integers. Initially, we used the larger of the latitudinal difference or longitudinal distance to ensure we did not cut off any of the lot, but because lots were not perfectly rectangular along the longitude/latitude axes, there was significant overlap from neighboring lots. We ended up instead using the smaller of the latitudinal difference and longitudnial difference to reduce this overlap while still getting most of the target lot.

We also masked the images with black rectangles. These masks are neccesary because having to round the zoom level down to the nearest integer (e.g. the desireable zoom level is 21.432, but the API will accept either 21 or 22) the zoom did not capture the desired distance exactly. These masks are used to cut out the irrevelant information this discrepancy adds at the border of the images.

## 8.3. Convolutional Neural Network

This program incorporates a supervised binary classification model to determine the probability of whether or not an input is a vacant lot or not. Code for the convolutional neural network is at `/application/src/classifier/model_code/vacant_occupied.py`.

Initially, the model takes in as input the images that were extracted in the previous step (224x224). We chose these image dimensions because it matches the dimensions of ImageNet, which VGG16 (the base of our model) has been pre-trained on. The data was manually split into two folders: train (80%) and test (20%). The subfolders in each of these are “STRUCTURE” and “VACANT_LOT.” Additionally, 20% of the training dataset was used for validation. The neural network uses VGG16 as a pretrained model, followed by several dense layers. Two dropout layers were added between the dense layers in order to prevent the model from overfitting to the training data. ReLU was used as the activation function; this activation function is typically used as a default for convolutional neural networks because it allows the model to overcome the vanishing gradient problem, and consequently learn faster and perform better. The final layer uses the sigmoid activation function to give a value between 0 and 1, which is ultimately used for the prediction of whether or not the parcel is a vacant lot. Since the image data contains a lot of information that is not necessarily used to make the prediction, it is considered quite noisy. As such, the Adam optimizer is used to handle this.

# 9. Resources

## 9.1. Example Input/Output
We provide a sample of an input CSV file which contains the min/max latitude and longitude coordinates of the lots of interest. This sample input file contains lots corresponding to the city of Hartford. In addition, we also provide a sample output CSV file with the description of the lot state (vacant, not vacant). Both of the sample files can be found in our google drive. 

[Input Sample CSV File](https://drive.google.com/file/d/1Ql-zzkaOViGRQaZ_xs-owNoEP8rWSbx6/view)

[Output Sample CSV File](https://drive.google.com/file/d/1wuopgssISEmlzSouLaOd1gaKnDOLVTT2/view)

## 9.2. EDA
When generating our dataset images, we used all vacant lots and vacant structures, but a subset of the occupied structures; however, we did not choose to balance the categories completely. As seen in the pie chart below, only 14.4% of the data (less than 1/6) represents vacant lots.

![category frequency](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/category_frequency.png)

We chose to do this because the frequency of occupied structures overwhelmingly dominates the frequency of vacant lots, so it make sense for the model to bias towards occupied structures if it is predicitng randomly sampled lots. Given the specifity and recall for our final binary model below, we felt this worked reasonably well for use cases in which the lots being predicted are randomly sampled; however, our dataset could be balanced and the model retrained if the use case required the model to not take category frequency into account and predict purely on their visual features. The categorical accuracy of our current model can be broken down as follows:

| Category | Precision | Recall | f1-score
--- | --- | --- | ---
| Not vacant | 0.96 | 0.96 | 0.96 |
| Vacant | 0.77 | 0.79 | 0.78 |

We considered doing a three-class model, separating vacant structures from occupied structures; however, we built a preliminary model with these classes and were getting significantly lower than desired accuracy (~78%). In order to understand these results better, we plotted the feature map of our test set at the second fully-connected layer using a t-distributed stochastic neighbor embedding to reduce dimensionality. This gave the following plot.

![t-SNE plot](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/misc/pics/tsne_reduction.png)

This plot shows that while occupied structures and vacant lots were largely seperable from one another, vacant structures were largely inseparable from occupied structures. This relationship makes sense when one considers that it is incredibly difficult to tell whether a structure is occupied from a satellite view. For this reason, we chose to combine vacant structures and occupied structures into one class.

## 9.3. Dataset Used for Training
The images used for training can be found [here](https://drive.google.com/file/d/1_1_MolX4b3kORVZjum7Jp5Roj6IgdeHb/view?usp=sharing). The dataset includes the "vacant structure" category, but this can be merged with the images in "occupied structure" to create the structure (referred to as "not vacant") vs. no structure (referred to as "vacant") classifications our final model uses.

# 1. Table Of Contents
TODO

# 2. Evaluating Physical Disorder in Cities
This repository contains a Flask application for determining the vacancy of a lot given its minimum and maximum latitude/longitude as input. The app processes the user input, generates images of the lots utilizing Google Maps Static API, and then predicts the vacancy of those lots via a Convolutional Neural Network. 

Even though lots can be polygons of any shape, our model currently is working with square images that are generated and masked according to the coordinates provided.

In the future, this model could be improved by utilizing images that capture the exact shape of lots, rather than approximating the shapes with rectangles. This would likely involve parsing a GIS Shapefile. In addition, our model does not distinguish vacant structures from occupied structures. In other words, our model defines a vacant lot as a lot containing no structures whatsoever. A model that could distinguish between a vacant lot, a vacant structure, and an occupied structure could be more useful but may require the use of Street View imagery.

![occupied structure](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/occupied.png) ![vacant lot](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/vacant_lot.png) ![vacant structure](https://raw.githubusercontent.com/michzyman/CitiesPhysicalDisordersProject-/main/vacant_structure.png)

_These are examples of the satellite images used as inputs to the convolutional neural network. The first image is an occupied structure, the second is a vacant lot, and the third is a vacant structure. All are images of real lots in in Hartford, Connecticut, and were extracted using the Google Maps Static API._

# 3. Why is this tool needed
Vacant and abandoned land is prevalent throughout the United States. Research from [studies](https://doi.org/10.1073/pnas.1718503115) conducted by Columbia University and University of Pennsylvania shows that restoring vacant land decreases firearm violence and crime. However, not all cities maintain comprehensive data of where vacant lots are present. As such, Dr. Jonathan Jay of the Boston University School of Public Health would like to automate the process of locating these lots. That way, city officials can be informed of the existence and location of empty lots, action can be taken to reorganize and rebuild these areas, and future violence can be prevented.

While our model does not yet fully automate the process of locating vacant lots, it is able to somewhat accurately determine the vacancy of a list of lots of interest. Therefore, this model can be seen as a proof-of-concept for the desired end goal.

# 4. Future direction

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

## 6.2. Setting up the Project
In order to run this project, you will need to [install Git](https://github.com/git-guides/install-git), [clone the repository](https://github.com/git-guides/git-clone), download and unzip [this ZIP file](https://drive.google.com/file/d/1MeZVs2wut_zAWDisxKNaoUJDhI24aPbw/view?usp=sharing), and place the saved_model folder at `application/src/classifier/saved_model`

## 6.3. Installing Docker
In order to be able to use Docker to build the project, [click here](https://docs.docker.com/docker-for-mac/install/) and follow the steps to install Docker. This documentation is for Mac only.

## 6.4. Building and Running the Docker Container
Navigate to the `application/` directory in [Terminal](https://macpaw.com/how-to/use-terminal-on-mac) and run the following Docker commands:

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
Inside the src folder which is inside the folder named “hartford_data_gen”, there is a python file named “parcel_info_collection.py”. This file contains the code we used to perform the Hartford data scraping. Thanks to the implementation of this code we were able to output a csv file with the min and max values for latitude and longitude coordinates for the parcels in Hartford. 

## 8.2. Google Maps Satellite Image Generation
TODO

## 8.3. Convolutional Neural Network
TODO

# 9. Resources

## 9.1. Example Input/Output
We provide a sample of an input CSV file which contains the min/max latitude and longitude coordinates of the parcels of interest. This sample input file contains parcels corresponding to the city of Hartford. In addition, we also provide a sample output CSV file with the description of the parcel state (vacant, not vacant). Both of the sample files can be found in our google drive. 

[Input Sample CSV File](https://drive.google.com/file/d/1Ql-zzkaOViGRQaZ_xs-owNoEP8rWSbx6/view)

[Output Sample CSV File](https://drive.google.com/file/d/1wuopgssISEmlzSouLaOd1gaKnDOLVTT2/view)

## 9.2. EDA
TODO

## 9.3. Dataset Used for Training
All of the data that we used to train and test our models can be found on Google Drive. Our models were trained using 80% of the data and tested on the remaining 20%. Each zip file contains two folders: test and train. 

TODO

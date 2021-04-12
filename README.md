Below are the instructions for running a demo of our code up to this point (which is primarily comprised of training data generation). This demo runs on a toy subset of our actual data due to API quotas (and because it would take a very long time otherwise) but it runs the same on the entire dataset.

### Prerequisites
* Docker
* Bash
* Nothing running on port 5000

### How to Run
1. Click [here](https://drive.google.com/file/d/19N8zhbAH3InMox-lb90q4_4MTJtyzY-t/view?usp=sharing) to download a secrets file

2. Place the secrets file at `google_maps_queries/src/secrets.py`

3. Make the project root the current working directory

4. Build the docker container with `docker build -t city-disorders .` (note: all Docker commands must be preceded by sudo on some machines)

5. Run the docker container with ``docker run -p 5000:5000 -v `pwd`:/code city-disorders``

### Expected Output
#### Generation of training images
1. The CSV containing addresses of parcels in Hartford, CT is converted into a CSV containing latitude/longitude coordinates and the vacancy category of those parcels

2. The generated CSV is used to query imgaes of the parcels and then masking is applied to each image to show only the parcel it represents

3. Generated images are saved according to parcel category at `demo/output`

#### Flask frontend
Additionally, a Flask frontend is running on port 5000 (viewable at localhost:5000 on a web browser). This frontend is not yet fully functional, but it currently allows the downloading and uploading of a template CSV file that will be used to make predictions with the final model

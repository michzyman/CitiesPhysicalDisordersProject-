from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pandas import DataFrame
import numpy as np
import os

from google_maps_queries.queries import download_images_from_csv

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
SAVED_MODEL_PATH = os.path.join(FILE_PATH, 'saved_model/')
IMAGE_PATH = os.path.join(FILE_PATH, 'images/')

IMAGE_SIZE = (224,224)
BATCH_SIZE = 1

def generate_predictions(input_filepath, output_filepath, api_key):
    download_images_from_csv(input_filepath, IMAGE_PATH, api_key, has_categories=False)
    
    classifier = load_model(SAVED_MODEL_PATH)

    datagen = ImageDataGenerator(rescale=1./255)

    pred_batches = datagen.flow_from_directory(
        IMAGE_PATH,
        shuffle=False,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    preds = classifier.predict(pred_batches)
    y_preds = (preds > 0.5)

    rows = []

    for i, prediction in enumerate(y_preds):
        name = pred_batches.filenames[i].replace('.png', '')
        filename_index = name.index('/') + 1
        name = name[filename_index:]

        label = 'Vacant' if prediction[0] else 'Not vacant'

        rows.append([name, label])

    df = DataFrame(rows, columns=['Name', 'Category'])

    df.to_csv(output_filepath, index=False)

import tensorflow as tf

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import torchvision
import torch
import os 

DATASET_PATH  = 'google_maps_queries/output'
# TEST_DIR = 'google_maps_queries/output'
IMAGE_SIZE    = (300,300)
NUM_CLASSES   = 3
BATCH_SIZE    = 10  
LEARNING_RATE = 0.001 

dataset = torchvision.datasets.ImageFolder(DATASET_PATH)
test_size = 0.2 * len(dataset)
print(test_size)
test_set = torch.utils.data.Subset(dataset, range(test_size))
train_set = torch.utils.data.Subset(dataset, range(test_size, len(dataset)))
# indexes = shuffle(range(len(dataset)))
# indexes_train = indexes[:int(len(dataset)*0.9)]
# indexes_test = indexes[int(len(dataset)*0.9):]


# train_dataset = image_dataset_from_directory(directory= DATASET_PATH, label_mode='categorical', class_names = ['OCCUPIED_STRUCTURE', 'VACANT_LOT','VACANT_STRUCTURE'])
# test_dataset = image_dataset_from_directory(directory= TEST_DIR, label_mode='categorical',class_names = ['OCCUPIED_STRUCTURE', 'VACANT_LOT','VACANT_STRUCTURE'])

train_datagen = ImageDataGenerator(rescale=1./255,rotation_range=50,featurewise_center = True,
                                   featurewise_std_normalization = True,width_shift_range=0.2,
                                   height_shift_range=0.2,shear_range=0.25,zoom_range=0.1,
                                   zca_whitening = True,channel_shift_range = 20,
                                   horizontal_flip = True,vertical_flip = True,
                                   validation_split = 0.2,fill_mode='constant')

train_batches = train_datagen.flow_from_directory(DATASET_PATH,target_size=IMAGE_SIZE,
                                                  shuffle=True,batch_size=BATCH_SIZE,
                                                  subset = "training",seed=42,
                                                  class_mode="categorical")

valid_batches = train_datagen.flow_from_directory(DATASET_PATH,target_size=IMAGE_SIZE,
                                                  shuffle=True,batch_size=BATCH_SIZE,
                                                  subset = "validation",
                                                  seed=42,class_mode="categorical")

model = Sequential()

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(300,300, 3))

for layer in base_model.layers:
  layer.trainable=False

model.add(base_model)
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_set, batch_size=32, epochs=10)

model.evaluate(test_set, batch_size=32)

model.save('model')

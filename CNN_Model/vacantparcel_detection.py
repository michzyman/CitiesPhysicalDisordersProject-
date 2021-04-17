import tensorflow as tf

from tensorflow.keras.applications import vgg16
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os 

DATASET_PATH  = 'parcels_data/train'
TEST_DIR = 'parcels_data/test'
BATCH_SIZE = 32
NUM_EPOCHS    = 10
IMAGE_SIZE    = (300,300)
NUM_CLASSES   = 3


train_dataset = image_dataset_from_directory(directory = DATASET_PATH, label_mode='categorical', class_names = ['OCCUPIED_STRUCTURE', 'VACANT_LOT','VACANT_STRUCTURE'])
test_dataset = image_dataset_from_directory(directory = TEST_DIR, label_mode='categorical', class_names = ['OCCUPIED_STRUCTURE', 'VACANT_LOT','VACANT_STRUCTURE'])

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

valid_batches = train_datagen.flow_from_directory(TEST_DIR,target_size=IMAGE_SIZE,
                                                  shuffle=True,batch_size=BATCH_SIZE,
                                                  subset = "validation",
                                                  seed=42,class_mode="categorical")
vgg = vgg16.VGG16(include_top=False,
                  weights='imagenet',
                  input_shape=(300,300,3))


for layer in vgg.layers[:]:
    layer.trainable = False

model = models.Sequential()
model.add(vgg)
model.add(layers.Flatten())
model.add(layers.Dense(300, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(3, activation='sigmoid'))

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt,loss='categorical_crossentropy', metrics=['accuracy'] )

model.fit(train_batches, validation_data=valid_batches, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)
model.evaluate(train_batches, batch_size=BATCH_SIZE)


model.save('model')

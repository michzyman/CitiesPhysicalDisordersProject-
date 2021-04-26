import tensorflow as tf
import numpy as np

from sklearn.metrics import classification_report
from tensorflow.keras.applications import vgg16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = 'data/train'
TEST_DIR = 'data/test'
BATCH_SIZE = 16
NUM_EPOCHS = 20
NUM_TUNING_EPOCHS = 10
IMAGE_SIZE = (224,224)

train_datagen = ImageDataGenerator(
    rescale=1./255, 
    validation_split = 0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_batches = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    shuffle=True,
    batch_size=BATCH_SIZE,
    subset = 'training',
    seed=42,
    class_mode='binary'
)

valid_batches = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    shuffle=True,
    batch_size=BATCH_SIZE,
    subset = 'validation',
    seed=42,
    class_mode='binary'
)

test_batches = test_datagen.flow_from_directory(
    TEST_DIR,
    shuffle=False,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

vgg = vgg16.VGG16(include_top=False,
                  weights='imagenet',
                  input_shape=(224,224,3))

for layer in vgg.layers[:]:
    layer.trainable = False

model = Sequential()
model.add(vgg)
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt,loss='binary_crossentropy', metrics=['accuracy'] )

model.fit(train_batches, validation_data=valid_batches, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)

for layer in vgg.layers[-4:]:
    layer.trainable = True

model.fit(train_batches, validation_data=valid_batches, epochs=NUM_TUNING_EPOCHS, batch_size=BATCH_SIZE)

preds = model.predict(test_batches)
y_preds = (preds > 0.5).astype(np.int)

print(classification_report(test_batches.classes, y_preds))

model.save('saved_model')

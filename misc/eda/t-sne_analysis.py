import tensorflow as tf
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from tensorflow.keras import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = 'data/train'
TEST_DIR = 'data/test'
BATCH_SIZE = 16
NUM_EPOCHS = 10
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
    class_mode='categorical'
)

valid_batches = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    shuffle=True,
    batch_size=BATCH_SIZE,
    subset = 'validation',
    seed=42,
    class_mode='categorical'
)

test_batches = test_datagen.flow_from_directory(
    TEST_DIR,
    shuffle=False,
    target_size=IMAGE_SIZE,
    batch_size=1,
    class_mode='categorical'
)

model = Sequential()

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224,224,3))

for layer in base_model.layers:
  layer.trainable=False

model.add(base_model)
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu', name='fc2'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'] )

model.fit(train_batches, validation_data=valid_batches, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)

# Construct model with early output at Flatten layer
early_output_model = Model(inputs=model.input, outputs=model.get_layer('fc2').output)

# Predict test data on early output model
tsne_pred = early_output_model.predict(test_batches)

# Generate 2-dimensional T-SNE reduction of feature map
reduction = TSNE(n_components=2).fit_transform(tsne_pred)

colors = []
for i in range(len(test_batches)):
    class_index = np.where(test_batches[i][1][0] == 1)[0]
    if class_index == 0:
        colors.append('red')
    elif class_index == 1:
        colors.append('blue')
    else:
        colors.append('green')

red = mpatches.Patch(color='red', label='Occupied Structure')
green = mpatches.Patch(color='green', label='Vacant Structure')
blue = mpatches.Patch(color='blue', label='Vacant Lot')

plt.scatter(reduction[:,0], reduction[:,1], c=colors)
plt.title('Feature Map at Second Fully-Connected Layer (t-SNE Reduction)')
plt.legend(handles=[red, green, blue])

plt.savefig('tsne_reduction.png')

import numpy as np
import os
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Configuration
IMG_SIZE = 150
LABELS = ['PNEUMONIA', 'NORMAL']
BASE_PATH = 'chest_xray'

def get_data(data_dir):
    data = []
    for label in LABELS:
        path = os.path.join(data_dir, label)
        class_num = LABELS.index(label)
        if not os.path.exists(path):
            print(f"Directory not found: {path}")
            continue
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                resized_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE))
                data.append([resized_arr, class_num])
            except Exception as e:
                print(f"Error loading image {img}: {e}")
    return np.array(data, dtype=object)

print("Loading data...")
# Load train, val, and test data
# Note: The folder structure might be chest_xray/chest_xray/train or chest_xray/train
# Based on ls -R output, the files are in chest_xray/train and chest_xray/chest_xray/train
# We'll use the most populated ones.
train_data = get_data(os.path.join(BASE_PATH, 'train'))
val_data = get_data(os.path.join(BASE_PATH, 'test')) # Using test as val if val is too small, similar to notebook
test_data = get_data(os.path.join(BASE_PATH, 'chest_xray/test'))

print(f"Total training samples: {len(train_data)}")

def preprocess(data):
    x = []
    y = []
    for feature, label in data:
        x.append(feature)
        y.append(label)
    x = np.array(x) / 255.0
    x = x.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = np.array(y)
    return x, y

x_train, y_train = preprocess(train_data)
x_val, y_val = preprocess(val_data)
x_test, y_test = preprocess(test_data)

# Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)
datagen.fit(x_train)

# Model Architecture
model = Sequential([
    Conv2D(32, (3, 3), strides=1, padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    MaxPool2D((2, 2), strides=2, padding='same'),

    Conv2D(64, (3, 3), strides=1, padding='same', activation='relu'),
    Dropout(0.1),
    BatchNormalization(),
    MaxPool2D((2, 2), strides=2, padding='same'),

    Conv2D(64, (3, 3), strides=1, padding='same', activation='relu'),
    BatchNormalization(),
    MaxPool2D((2, 2), strides=2, padding='same'),

    Conv2D(128, (3, 3), strides=1, padding='same', activation='relu'),
    Dropout(0.2),
    BatchNormalization(),
    MaxPool2D((2, 2), strides=2, padding='same'),

    Conv2D(256, (3, 3), strides=1, padding='same', activation='relu'),
    Dropout(0.2),
    BatchNormalization(),
    MaxPool2D((2, 2), strides=2, padding='same'),

    Flatten(),
    Dense(units=128, activation='relu'),
    Dropout(0.2),
    Dense(units=1, activation='sigmoid')
])

model.compile(optimizer="rmsprop", loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience=2, verbose=1, factor=0.3, min_lr=0.000001)

print("Starting training...")
# Check if GPU is available
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

history = model.fit(
    datagen.flow(x_train, y_train, batch_size=32),
    epochs=12,
    validation_data=datagen.flow(x_val, y_val),
    callbacks=[learning_rate_reduction]
)

print("Saving model...")
model.save('pneumonia_model.h5')
print("Model saved as pneumonia_model.h5")

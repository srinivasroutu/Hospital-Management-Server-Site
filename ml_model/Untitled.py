#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn import metrics
import matplotlib.pyplot as plt


# In[4]:


test_dir = r"C:\Users\srini\OneDrive\Documents\6TH SEM\DSAI\project\Alzheimer_s Dataset\test"
train_dir = r"C:\Users\srini\OneDrive\Documents\6TH SEM\DSAI\project\Alzheimer_s Dataset\train"


# In[6]:


for dirtrain in os.listdir(train_dir):
    print(dirtrain)
    for tr in os.listdir(os.path.join(train_dir, dirtrain)):
        img = cv2.imread(os.path.join(train_dir, dirtrain, tr))
        img = cv2.resize(img, (32, 32))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.reshape(32, 32, 1)
        data.append([img, dirtrain])


# In[9]:


for dirtest in os.listdir(test_dir):
    print(dirtest)
    for ts in os.listdir(os.path.join(test_dir, dirtest)):
        img = cv2.imread(os.path.join(test_dir, dirtest, ts))
        img = cv2.resize(img, (32, 32))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.reshape(32, 32, 1)
        data.append([img, dirtest])


# In[10]:


# Shuffle data
random.seed(20)
random.shuffle(data)

# Split data into features and labels
x, y = zip(*data)
x = np.array(x)
y = np.array(y)
y = y.reshape(y.shape[0], 1)

# One-hot encode labels
enc = OneHotEncoder(handle_unknown='ignore').fit(y)
y = enc.transform(y).toarray()

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)

# Model setup
model = Sequential([
    Conv2D(64, (4, 4), padding='same', activation='relu', input_shape=(32, 32, 1)),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Conv2D(128, (2, 2), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Conv2D(256, (2, 2), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(4, activation='softmax')
])

model.summary()


# In[11]:


import random


# In[12]:


# Shuffle data
random.seed(20)
random.shuffle(data)

# Split data into features and labels
x, y = zip(*data)
x = np.array(x)
y = np.array(y)
y = y.reshape(y.shape[0], 1)

# One-hot encode labels
enc = OneHotEncoder(handle_unknown='ignore').fit(y)
y = enc.transform(y).toarray()

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)

# Model setup
model = Sequential([
    Conv2D(64, (4, 4), padding='same', activation='relu', input_shape=(32, 32, 1)),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Conv2D(128, (2, 2), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Conv2D(256, (2, 2), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=(2, 2)),
    Dropout(0.3),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(4, activation='softmax')
])

model.summary()


# In[13]:


model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Model training
hist = model.fit(x_train, y_train, epochs=200, validation_split=0.2, batch_size=64, verbose=1, shuffle=True)


# In[14]:


fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
axes[0].plot(hist.history['loss'], color='teal', label='Training Loss')
axes[0].plot(hist.history['val_loss'], color='orange', label='Validation Loss')
axes[0].set_title('Loss')
axes[0].legend()

axes[1].plot(hist.history['accuracy'], color='teal', label='Training Accuracy')
axes[1].plot(hist.history['val_accuracy'], color='orange', label='Validation Accuracy')
axes[1].set_title('Accuracy')
axes[1].legend()

plt.show()


# In[15]:


loss_and_metrics = model.evaluate(x_test, y_test, verbose=2)
print(f'Test Loss: {loss_and_metrics[0]}')
print(f'Test Accuracy: {loss_and_metrics[1]}')


# In[16]:


y_pred = model.predict(x_test).argmax(axis=1)
confusion_matrix = metrics.confusion_matrix(np.argmax(y_test, axis=1), y_pred)
confusion_df = pd.DataFrame(confusion_matrix, columns=['0', '1', '2', '3'], index=['0', '1', '2', '3'])
print(confusion_df)


# In[17]:

model.save("alzheimer_model.h5")




# %%

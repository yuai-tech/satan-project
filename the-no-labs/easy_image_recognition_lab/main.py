
import matplotlib.pylab as plt
from tensorflow.keras import layers
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_hub.keras_layer import KerasLayer
import numpy as np
import PIL.Image as Image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import confusion_matrix
import seaborn as sns

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


# load images
data_set_directory = "./the-no-labs/easy_image_recognition_lab/data"

IMAGE_SHAPE = (64, 64)
image_generator = ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(
    data_set_directory,
    target_size=IMAGE_SHAPE,
    batch_size=32
)


# print image
n_image_to_show = 6
data_to_show = image_data[0][0][n_image_to_show]
label_to_show = image_data[0][1][n_image_to_show]
plt.imshow(data_to_show)
plt.title('LABEL: ' + str(label_to_show) + ' indices ' + str(image_data.class_indices))
plt.show()


# train model
# model
model = Sequential()
model.add(
    Input(shape=(64, 64, 3, ))
)
model.add(
    Flatten()
)
model.add(
    Dense(1000, activation='relu')
)
model.add(
    Dense(1000, activation='relu')
)
model.add(
    Dense(3, activation='sigmoid')
)
model.summary()


# train model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(image_data, epochs=20, verbose=1)

# predict
predictions_prob = model.predict(image_data[0][0])
predictions_current = np.argmax(predictions_prob, axis=1)
predictions_expected = np.argmax(image_data[0][1], axis=1)

# confusion matrix
cm = confusion_matrix(predictions_expected, predictions_current)
sns.heatmap(cm, annot=True, fmt="d", cmap="Spectral")
plt.show()



import tensorflow as tf
from keras import layers, models
from keras.src.legacy.preprocessing.image import ImageDataGenerator

model = models.Sequential()


# Aplanar la salida para pasarla a las capas densas
model.add(layers.Flatten())

# Capa densa completamente conectada con 512 neuronas
model.add(layers.Dense(512, activation='relu'))

# Capa de salida con una neurona, usando activación sigmoide para clasificación binaria (rostro o no rostro)
model.add(layers.Dense(1, activation='sigmoid'))


# Regularización usando Dropout para evitar sobreajuste
model.add(layers.Dropout(0.5))
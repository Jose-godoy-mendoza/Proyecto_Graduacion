import tensorflow as tf
from keras import layers, models
from keras.src.legacy.preprocessing.image import ImageDataGenerator

# Definir el modelo CNN
model = models.Sequential()

# Primera capa de convolución y pooling
model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))

# Segunda capa de convolución y pooling
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Tercera capa de convolución y pooling
model.add(layers.Conv2D(256, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Dropout(0.5))

# Cuarta capa de convolución y pooling
model.add(layers.Conv2D(512, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Aplanar la salida para pasarla a las capas densas
model.add(layers.Flatten())

# Capa densa completamente conectada con 512 neuronas
model.add(layers.Dense(512, activation='relu'))

# Regularización usando Dropout para evitar sobreajuste
model.add(layers.Dropout(0.5))

# Capa de salida con una neurona, usando activación sigmoide para clasificación binaria (rostro o no rostro)
model.add(layers.Dense(1, activation='sigmoid'))

# Compilar el modelo con un optimizador Adam y función de pérdida binaria
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Resumen del modelo
model.summary()


# Aumento de datos para prevenir sobreajuste y mejorar la capacidad generalizadora
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Escalar los valores de píxeles entre 0 y 1
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Directorios de imágenes de entrenamiento y validación
train_dir = 'path/to/train_images'  # Actualiza con la ruta de tus imágenes de entrenamiento
validation_dir = 'path/to/validation_images'  # Actualiza con la ruta de tus imágenes de validación

# Generadores de lotes de imágenes
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'  # Clasificación binaria
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

# Entrenar el modelo
history = model.fit(
    train_generator,
    steps_per_epoch=100,  # Número de lotes por época
    epochs=50,  # Número de épocas (puedes ajustar según el rendimiento)
    validation_data=validation_generator,
    validation_steps=50
)

# Evaluar el modelo en los datos de validación
loss, accuracy = model.evaluate(validation_generator)
print(f'Pérdida: {loss}, Precisión: {accuracy}')

# Matriz de confusión y clasificación
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Predecir las clases en los datos de validación
validation_generator.reset()
predictions = model.predict(validation_generator)
predicted_classes = np.round(predictions).astype(int)

# Obtener las clases reales
true_classes = validation_generator.classes

# Imprimir la matriz de confusión y el reporte de clasificación
print(confusion_matrix(true_classes, predicted_classes))
print(classification_report(true_classes, predicted_classes))

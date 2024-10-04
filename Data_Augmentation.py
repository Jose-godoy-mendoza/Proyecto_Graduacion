import os
from keras._tf_keras.keras.preprocessing.image import load_img, ImageDataGenerator, img_to_array, array_to_img

# Ruta donde se encuentran las fotos
ruta_fotos = "D:\\Codigos\\Fotos_Reconocimiento\\Juan_Perez_001"
# Ruta donde se guardarán las variaciones de las fotos
ruta_salida = "D:\\Codigos\\Fotos_Reconocimiento\\Variaciones_Juan_Perez"

# Crear el directorio de salida si no existe
os.makedirs(ruta_salida, exist_ok=True)

# Crear el generador de imágenes
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Cargar y procesar las imágenes
for nombre_archivo in os.listdir(ruta_fotos):
    if nombre_archivo.endswith(('.png', '.jpg', '.jpeg')):  # Verifica que sea una imagen
        # Cargar la imagen
        img_path = os.path.join(ruta_fotos, nombre_archivo)
        img = load_img(img_path)  # Cargar la imagen
        x = img_to_array(img)     # Convertir a un array numpy
        x = x.reshape((1,) + x.shape)  # Cambiar la forma a (1, alto, ancho, canales)

        # Generar variaciones y guardarlas
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=ruta_salida, 
                                   save_prefix='variacion', save_format='jpg'):
            i += 1
            if i > 20:  # Generar 20 imágenes por cada imagen original
                break

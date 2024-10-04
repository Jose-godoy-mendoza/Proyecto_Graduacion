import cv2
import os

def capturar_imagenes(nombre_empleado, id_empleado, num_imagenes=100, tamaño_imagen=(256, 256)):
    # Ruta personalizada donde se guardarán las imágenes
    carpeta = f"D:/Codigos/Fotos_Reconocimiento/{nombre_empleado}_{id_empleado}"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Inicializar la cámara
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return
    
    print("Cámara inicializada correctamente.")

    detector_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if detector_rostros.empty():
        print("Error: No se pudo cargar el archivo Haar Cascade.")
        return

    contador_imagenes = 0

    while contador_imagenes < num_imagenes:
        ret, frame = camara.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara.")
            break

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = detector_rostros.detectMultiScale(gris, 1.3, 5)

        for (x, y, w, h) in rostros:
            contador_imagenes += 1
            rostro = gris[y:y+h, x:x+w]

            # Redimensionar el rostro capturado al tamaño deseado (por ejemplo, 256x256)
            rostro_redimensionado = cv2.resize(rostro, tamaño_imagen)

            nombre_archivo = f"{carpeta}/{nombre_empleado}_{contador_imagenes}.jpg"
            cv2.imwrite(nombre_archivo, rostro_redimensionado, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # Guardar con compresión de 90%
            print(f"Imagen {contador_imagenes} capturada y guardada en {nombre_archivo} con tamaño {tamaño_imagen}")

        if contador_imagenes >= num_imagenes:
            print("Captura completa.")
            break

    camara.release()
    print("Proceso de captura completado.")

nombre_empleado = "Juan_Perez"
id_empleado = "001"
capturar_imagenes(nombre_empleado, id_empleado)

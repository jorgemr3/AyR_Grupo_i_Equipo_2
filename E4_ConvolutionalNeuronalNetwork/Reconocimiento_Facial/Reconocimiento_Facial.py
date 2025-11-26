import cv2
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array
import time

# Configuración del modelo
modelo_path = "../modelo/modelo.keras"
alto, largo = 150, 150

# Cargar modelo entrenado
try:
    cnn = load_model(modelo_path)
    print(f"Modelo cargado exitosamente desde: {modelo_path}")
except Exception as e:
    print(f"Error cargando modelo: {e}")
    exit()

# Configuración de la cámara
cam = cv2.VideoCapture(0)  # Cámara principal (0), cambiar a 1 si es necesario

# Clasificador de caras
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Diccionario de clases
clases = {
    0: 'C1- Jafeth',
    1: 'C2- Cenyi',
    2: 'C3- Luis',
    3: 'C4- Melo'
}

colores = {
    'C1- Jafeth': (0, 255, 255),
    'C2- Cenyi': (255, 0, 255),
    'C3- Luis': (255, 0, 255),
    'C4- Melo': (255, 255, 0)
}

predicciones_historicas = []


def predecir_cara(cara_img):
    """
    Predice la identidad de una cara usando el modelo entrenado en escala de grises
    """
    try:

        cara_resized = cv2.resize(cara_img, (alto, largo), interpolation=cv2.INTER_CUBIC)

        # Convertir a escala de grises (como se entrenó el modelo)
        cara_gray = cv2.cvtColor(cara_resized, cv2.COLOR_BGR2GRAY)

        # Convertir a array y normalizar (forma final: (1, 300, 300, 1))
        cara_array = img_to_array(cara_gray)
        cara_array = np.expand_dims(cara_array, axis=0)
        cara_array = cara_array / 255.0

        # Hacer predicción
        prediccion = cnn.predict(cara_array, verbose=0)
        clase_pred = np.argmax(prediccion[0])
        confianza = np.max(prediccion[0]) * 100

        return clases.get(clase_pred, 'Desconocido'), confianza

    except Exception as e:
        print(f"Error en predicción: {e}")
        return 'Error', 0


def detectar_y_reconocer(image):
    """
    Detecta caras y las reconoce usando el modelo
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40)
    )

    for (x, y, w, h) in faces:
        cara = image[y:y + h, x:x + w]

        nombre, confianza = predecir_cara(cara)

        predicciones_historicas.append((nombre, confianza))

        # Obtener color para esta persona
        color = colores.get(nombre, (255, 255, 255))  # Blanco por defecto

        # Dibujar rectángulo alrededor de la cara
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 3)

        # Texto con nombre y confianza
        texto = f"{nombre}: {confianza:.1f}%"

        # Fondo para el texto
        (text_width, text_height), baseline = cv2.getTextSize(
            texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(
            image,
            (x, y - text_height - 10),
            (x + text_width, y),
            color,
            -1
        )

        # Texto
        cv2.putText(
            image,
            texto,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),  # Texto negro
            2
        )

    return image


print("Iniciando reconocimiento facial en tiempo real...")
print("Presiona 'q' para salir")
print("Presiona 'r' para mostrar/ocultar FPS")
print("Input shape del modelo:", cnn.input_shape)

mostrar_fps = True
fps_counter = 0
start_time = time.time()

while True:
    ret, frame = cam.read()

    if not ret:
        print("Error: No se puede capturar frame de la cámara")
        break

    # Voltear imagen horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)

    # Detectar y reconocer caras
    frame_procesado = detectar_y_reconocer(frame)

    # Calcular FPS
    fps_counter += 1
    if mostrar_fps and fps_counter % 10 == 0:
        elapsed_time = time.time() - start_time
        fps = fps_counter / elapsed_time
        cv2.putText(
            frame_procesado,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    # Mostrar instrucciones
    cv2.putText(
        frame_procesado,
        "Presiona 'q' para salir, 'r' para FPS, 'c' para limpiar historial",
        (10, frame_procesado.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    # Mostrar frame
    cv2.imshow("Reconocimiento Facial - Tiempo Real", frame_procesado)

    # Controles de teclado
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        mostrar_fps = not mostrar_fps
        fps_counter = 0
        start_time = time.time()
    elif key == ord('c'):
        predicciones_historicas.clear()
        print("Historial de predicciones limpiado")

# Limpiar
cam.release()
cv2.destroyAllWindows()
print("Reconocimiento finalizado")

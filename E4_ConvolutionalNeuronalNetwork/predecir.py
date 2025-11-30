import os
import numpy as np
from keras.utils import load_img, img_to_array
from keras.models import load_model

alto, largo = 300, 300
modelo = "E4_ConvolutionalNeuronalNetwork\modelo3\modelo.keras"
pesos = 'E4_ConvolutionalNeuronalNetwork\modelo3\pesos.weights.h5'

cnn = load_model(modelo)
cnn.load_weights(pesos)

# Predicción de una imagen
def predict(file):
    imagen_a_predecir = load_img(file, target_size=(alto, largo), color_mode="grayscale")
    imagen_a_predecir = img_to_array(imagen_a_predecir) / 255.0  # Normalización
    imagen_a_predecir = np.expand_dims(imagen_a_predecir, axis=0)
    arreglo = cnn.predict(imagen_a_predecir, verbose=0)
    resultado = arreglo[0]
    respuesta = np.argmax(resultado)

    match respuesta:
        case 0:
            return 'C1- Jafeth'
        case 1:
            return 'C2- Cenyi'
        case 2:
            return 'C3- Luis'
        case 3:
            return 'C4- Melo'

# Obtener nombres de carpetas
def get_folders_name_from(from_location):
    list_dir = os.listdir(from_location)
    folders = [f for f in list_dir if os.path.isdir(os.path.join(from_location, f))]
    folders.sort()
    if '.DS_Store' in folders:
        folders.remove('.DS_Store')
    return folders

# Probar red neuronal
def probar_red_neuronal():
    cnn.summary()
    base_location = "E4_ConvolutionalNeuronalNetwork\\F3-Prueba"
    folders = get_folders_name_from(base_location)

    correct = 0
    count_predictions = 0

    for folder in folders:
        files = [f for f in os.listdir(os.path.join(base_location, folder))
                 if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        for file in files:
            composed_location = os.path.join(base_location, folder, file)
            prediction = predict(composed_location)
            print(folder, prediction, prediction in folder)
            count_predictions += 1
            if prediction in folder:
                correct += 1

    eficiencia = correct / count_predictions * 100
    print(f"\n🎯 Eficiencia total: {eficiencia:.2f}%")

probar_red_neuronal()

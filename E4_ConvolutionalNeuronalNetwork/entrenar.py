import os
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

K.clear_session()

# Rutas de datos (relativas a este script)
data_entrenamiento = "E4_ConvolutionalNeuronalNetwork\\F1-Entrenamiento"
data_validacion = "E4_ConvolutionalNeuronalNetwork\\F2-Validacion"

# Parámetros base
epocas = 80
alto, largo = 150, 150
batch_size = 8
pasos = 100
pasos_validacion = 20

# Parámetros de la red
kernel1 = (3, 3)
kernel2 = (2, 2)
kernel3 = (3, 3)

tot_kernels1 = 32
tot_kernels2 = 64
tot_kernels3 = 128

stride = (2, 2)
clases = 4
lr = 0.0001

# Aumento de datos (mejorado)
entrenamiento_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=25,
    shear_range=0.2,
    zoom_range=0.25,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

validacion_datagen = ImageDataGenerator(
    rescale=1.0/255
)

imagen_entrenamiento = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size=(alto, largo),
    batch_size=batch_size,
    class_mode='categorical',
    color_mode="grayscale"
)

imagen_validacion = validacion_datagen.flow_from_directory(
    data_validacion,
    target_size=(alto, largo),
    batch_size=batch_size,
    class_mode='categorical',
    color_mode="grayscale"
)

# Red convolucional
cnn = Sequential()

# Capas convolucionales y pooling
cnn.add(Convolution2D(tot_kernels1, kernel1, padding='same', input_shape=(alto, largo, 1), activation='relu'))
cnn.add(MaxPooling2D(pool_size=stride))

cnn.add(Convolution2D(tot_kernels2, kernel2, padding='same', activation='relu'))
cnn.add(MaxPooling2D(pool_size=stride))

cnn.add(Convolution2D(tot_kernels3, kernel3, padding='same', activation='relu'))
cnn.add(MaxPooling2D(pool_size=stride))

cnn.add(Flatten())

# Capas densas
cnn.add(Dense(256, activation='relu'))
cnn.add(Dropout(0.3))

cnn.add(Dense(512, activation='relu'))
cnn.add(Dropout(0.4))

# Capa de salida
cnn.add(Dense(clases, activation='softmax'))

# Compilación del modelo
cnn.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.Adam(learning_rate=lr),
    metrics=['accuracy']
)

# Callbacks inteligentes
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=5,
    min_lr=1e-6
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

# Entrenamiento
cnn.fit(
    imagen_entrenamiento,
    steps_per_epoch=pasos,
    epochs=epocas,
    validation_data=imagen_validacion,
    validation_steps=pasos_validacion,
    callbacks=[reduce_lr, early_stop]
)

# Guardar modelo y pesos
dir = "modelo/"
if not os.path.exists(dir):
    os.mkdir(dir)

cnn.save(dir + 'modelo.keras')          # modelo completo
cnn.save_weights(dir + 'pesos.weights.h5')  # solo pesos



print("✅ Entrenamiento completado y modelo guardado exitosamente.")


**Proyecto AyR — Resumen del repositorio**

Este repositorio contiene varios scripts y recursos organizados por carpetas para proyectos de simulación, reconocimiento facial, redes neuronales y utilidades varias. A continuación se ofrece una descripción a grandes rasgos de los archivos y carpetas principales.

**Estructura general**

- **Archivos raíz**: archivos sueltos en la raíz del repositorio.
  - `Letra.txt`: archivo de entrada para kareljs para formar la letra Y
  - `mundo recorrido.in`: archivo de datos de mundo/recorrido (nombre con espacio).
  - `mundo_letra.in`: otro archivo de datos de entrada relacionado con mundos/letras.
  - `Recorrido.txt`: archivo de recorrido para Kareljs, recoleccion y soltar objetos.

**`Coche/`**

- **Descripción**: scripts para simulación de coche/pista.
  - `Simulador_1.py`: El programa crea una simulación de un coche en Tkinter, donde el usuario puede controlar un auto que se mueve por una carretera. El coche puede avanzar, retroceder, girar a la izquierda/derecha y frenar, utilizando las flechas del teclado.
El entorno incluye pasto, carretera, líneas centrales, zona de inicio y meta, y el coche se redibuja con rotación realista en cada frame.
Además, el programa detecta colisiones con el pasto o cuando el coche toca la meta, y reinicia su posición.
También muestra la velocidad actual del coche en px/s y una conversión ficticia a km/h.

  - `pista.py`: El programa usa Pygame para mostrar una ventana de 900×700 píxeles donde se carga y despliega una imagen llamada pista.png.
La imagen se escala al tamaño de la ventana y se muestra continuamente en pantalla dentro de un ciclo principal que solo termina cuando el usuario cierra la ventana.

**`E4_ConvolutionalNeuronalNetwork/`**

- **Descripción**: proyecto relacionado con redes neuronales convolucionales para reconocimiento/ clasificación.
  - `entrenar.py`: script para entrenar modelos.
  - `predecir.py`: script para realizar predicciones con modelos entrenados.
  - `modelo/`, `modelo2/`, `modelo3/`: subcarpetas que contienen modelos entrenados y pesos (`.h5`, `.keras`, `.xml`, etc.).
  - `F1-Entrenamiento/`, `F2-Validacion/`, `F3-Prueba/`: conjuntos de datos ordenados por usuario/cliente dentro de cada fase (por ejemplo `C1- Jafeth/`, `C2- Cenyi/`, `C3- Luis/`, `C4- Melo/`).
  - `Reconocimiento_Facial/`: scripts auxiliares para entrenamiento y reconocimiento (por ejemplo `entrenar_EigenFace.py`, `Reconocimiento_Facial.py`).

**`E5/`**

- **Descripción**: utilidades relacionadas con control de coche / mediapipe.
  - `Instruc_coche.py`: instrucciones o controlador para el coche.
  - `Libreria_mediapipe.py`: wrapper o utilidades sobre MediaPipe para detección/seguimiento.

**`E6/`**

- **Descripción**: analizador/compilador/voz y utilidades de tokenización.
  - `Dicc.py`, `Scanner.py`, `Token.py`: módulos típicos de un analizador léxico / scanner.
  - `vosk_speech_recognition.py`: integración con Vosk para reconocimiento de habla.
  - `vosk-model-small-es-0.42/`: modelo de Vosk incluido (archivos binarios y configuración).

**`Lab/`**

- **Descripción**: implementaciones y experimentos con laberintos.
  - `laberinto_2.py`, `laberinto_3.py`, `Laberinto.py`: scripts que contienen implementaciones del laberinto y algoritmos de recorrido.

**`PuntoA-j/`**

- **Descripción**: ejercicio o script independiente.
  - `PuntoA-J.py`: script ejecutable para una tarea concreta (revisar contenido para más detalles).

**Notas generales y recomendaciones**

- **Ejecución**: la mayoría de los scripts son ejecutables con Python 3: por ejemplo `python Coche\SImulacion_1.py` desde PowerShell (usar la ruta correcta y un entorno virtual si hace falta).
- **Modelos y datos**: las carpetas `modelo*` y `vosk-model-small-es-0.42` contienen artefactos binarios (pesos, modelos) — no es necesario regenerarlos si ya están disponibles.
- **Nombres y consistencia**: hay algunos nombres con mayúsculas inusuales (`SImulacion_1.py`, espacios en nombres de archivo). Puede valer la pena estandarizar nombres para evitar errores al ejecutar scripts desde shell.
- **Siguientes pasos sugeridos**: añadir un `requirements.txt` si hay dependencias Python (tensorflow/keras, opencv, vosk, mediapipe), y añadir instrucciones de ejecución por carpeta si desea que documente comandos concretos.

**Documentación detallada de scripts Python**

- **Archivo**: `PuntoA-j/PuntoA-J.py` — Visualización y búsqueda de caminos en un grafo dirigido usando `networkx` y `matplotlib`. Genera un grafo con nodos A..J, asigna pesos aleatorios a aristas y usa una búsqueda con retroceso que bloquea aristas subóptimas; muestra la animación del proceso y el mejor camino encontrado.

- **Archivo**: `Lab/laberinto_3.py` — Generador procedural de laberintos y solución automática. Crea un laberinto por tallado recursivo, lo resuelve con BFS y anima la solución en una ventana `tkinter` moviendo un jugador paso a paso.

- **Archivo**: `Lab/laberinto_2.py` — Generador de laberintos con controlador interactivo. Genera el laberinto y permite controlar al jugador con las teclas `WASD`; muestra la ventana con `tkinter` y notifica al usuario al llegar a la salida.

- **Archivo**: `Lab/Laberinto.py` — Versión sencilla para generar y mostrar un laberinto en `tkinter`. No incluye auto-resolución ni controles (muestra el laberinto generado).

- **Archivo**: `E6/vosk_speech_recognition.py` — Cliente de reconocimiento de voz en tiempo real usando `vosk` y `pyaudio`. Carga el modelo local `vosk-model-small-es-0.42`, escucha el micrófono, convierte la hipótesis a tokens y clasifica palabras en tipos (`ACCION`, `OBJETO`, `LUGAR`, `PORCENTAJE`, `NUMERO`) usando un mapeo léxico y reglas (números como texto o dígitos, porcentajes).

- **Archivo**: `E6/Token.py` — Definición del `Token` como `dataclass` con utilidades (comparación, comprobaciones de tipo). Se integra con `Dicc.py` para representar tokens producidos por el analizador/voz.

- **Archivo**: `E6/Dicc.py` — Enumeración (`Enum`) `Dicc` que define los tipos de token usados por el analizador/voz: `ACCION`, `OBJETO`, `LUGAR`, `PORCENTAJE`, `NUMERO`.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/Reconocimiento_Facial.py` — Aplicación de reconocimiento facial en tiempo real con OpenCV y un modelo Keras. Captura video, detecta caras con Haar cascades, normaliza la región facial y pasa por la red CNN para predecir una clase; dibuja rectángulos y etiquetas de confianza en la cámara.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/entrenar_LBPHFace.py` — Entrenador para el algoritmo LBPH (OpenCV). Recibe listas de imágenes y etiquetas, entrena un `LBPHFaceRecognizer` y escribe el modelo en `../modelo2/modeloLBPHFace.xml`.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/entrenar_FisherFace.py` — Entrenador para `FisherFaceRecognizer` de OpenCV; entrena con `images, labels` y guarda el modelo en `../modelo2/modeloFisherFace.xml`.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/entrenar_EigenFace.py` — Entrenador para `EigenFaceRecognizer` (requiere `opencv-contrib-python`); entrena y guarda el modelo en `../modelo2/modeloEigenFace.xml`.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/entrenar.py` — Script que carga las imágenes desde la carpeta `F1-Entrenamiento`, prepara `images` y `labels` (redimensiona y pasa a escala de grises) y delega el entrenamiento al entrenador elegido (`entrenar_LBPHFace` por defecto). Sirve para preparar y lanzar el entrenamiento clásico de reconocimiento facial.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/Reconocimiento_Facial/entrenamiento2.0.py` — Versión basada en Keras de un flujo de entrenamiento: define una CNN simple, genera `ImageDataGenerator` para aumento de datos, entrena la red y guarda el modelo en `../modelo3/` (`modelo.keras` y `pesos.weights.h5`).

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/predecir.py` — Utilidad para cargar un modelo Keras (`modelo3`) y predecir la clase de imágenes individuales. También incluye una función para evaluar la red sobre el conjunto `F3-Prueba` y reportar eficiencia.

- **Archivo**: `E4_ConvolutionalNeuronalNetwork/entrenar.py` — Script principal de entrenamiento (versión mejorada): define la CNN, callbacks (`ReduceLROnPlateau`, `EarlyStopping`), prepara `ImageDataGenerator` y entrena el modelo guardando resultados en `modelo/`.

- **Archivo**: `E5/Libreria_mediapipe.py` — Biblioteca/auxiliar con utilidades de MediaPipe para detectar manos y dedos. Contiene funciones `fingers_up`, `detect_gesture` y una interfaz `HandDetectionApp` (Tkinter) para mostrar la cámara y acciones detectadas; se usa para controlar aplicaciones por gestos.

- **Archivo**: `E5/Instruc_coche.py` — Interfaz de detección de manos y mapeo a acciones para un coche (usa `mediapipe`, OpenCV, `tkinter` y `PIL`). Muestra la cámara y detecta gestos (avanzar, retroceder, girar, detener) y actúa (reproduce/pausa audio en la versión completa del proyecto).

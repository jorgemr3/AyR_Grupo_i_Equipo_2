**Proyecto AyR — Resumen del repositorio**

Este repositorio contiene varios scripts y recursos organizados por carpetas para proyectos de simulación, reconocimiento facial, redes neuronales y utilidades varias. A continuación se ofrece una descripción a grandes rasgos de los archivos y carpetas principales.

**Estructura general**

- **Archivos raíz**: archivos sueltos en la raíz del repositorio.
  - `Letra.txt`: archivo de entrada para kareljs para formar la letra Y
  - `mundo recorrido.in`: archivo de datos de mundo/recorrido (nombre con espacio).
  - `mundo_letra.in`: otro archivo de datos de entrada relacionado con mundos/letras.
  - `Recorrido.txt`: archivo de recorrido para Kareljs (posible salida o entrada de rutas).

**`Coche/`**

- **Descripción**: scripts para simulación de coche/pista.
  - `Pista.py`: lógica relacionada con la pista (generación, representación o utilidades).
  - `SImulacion_1.py`: script de simulación (nota: nombre con I mayúscula, revisar si corresponde `Simulacion`).

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

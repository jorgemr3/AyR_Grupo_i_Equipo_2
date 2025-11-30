import sys
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

# ---------------- ENUM Y TOKEN ----------------
class Dicc(Enum):
    ACCION = auto()
    OBJETO = auto()
    LUGAR = auto()
    PORCENTAJE = auto()
    NUMERO = auto()

@dataclass
class Token:
    type: Dicc
    value: Any
    linea: int
    columna: int = 1
    pos: int = 0

    def __str__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, linea={self.linea}, columna={self.columna})"


# ---------------- MODELO ----------------
if not os.path.exists("E6/vosk-model-small-es-0.42"):
    print("Descargar modelo de https://alphacephei.com/vosk/models")
    sys.exit(1)

model = Model("E6/vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

# Diccionario de palabras clave
lexico = {
    "abrir": Dicc.ACCION,
    "cerrar": Dicc.ACCION,
    "puerta": Dicc.OBJETO,
    "principal": Dicc.OBJETO,
    "laboratorio": Dicc.LUGAR,
    "salon": Dicc.LUGAR,
    "biblioteca": Dicc.LUGAR,
    "entrada": Dicc.LUGAR,
    "salida": Dicc.LUGAR,
}

# Diccionario de números en texto
numeros_texto = {
    "cero": 0,
    "uno": 1, "una": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "veinte": 20,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100
}

# ---------------- AUDIO ----------------
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("🎤 Escuchando comandos de puertas...")

linea = 1
while True:
    data = stream.read(4000, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result = result.replace("{","").replace("}", "").replace("\n", "").replace("\"", "")
        result = result.split(":")[1].strip()
        palabras = result.split(" ")

        tokens = []
        for i, palabra in enumerate(palabras):
            palabra = palabra.lower()

            # 1. Palabras del diccionario
            if palabra in lexico:
                token = Token(type=lexico[palabra], value=palabra, linea=linea, columna=i+1, pos=i)
                tokens.append(token)

            # 2. Porcentajes (ej: "50%")
            elif re.match(r'^\d+%$', palabra):
                token = Token(type=Dicc.PORCENTAJE, value=int(palabra.replace("%","")), linea=linea, columna=i+1, pos=i)
                tokens.append(token)

            # 3. Números en dígitos (ej: "50")
            elif palabra.isdigit():
                token = Token(type=Dicc.NUMERO, value=int(palabra), linea=linea, columna=i+1, pos=i)
                tokens.append(token)

            # 4. Números escritos en texto (ej: "cincuenta")
            elif palabra in numeros_texto:
                token = Token(type=Dicc.NUMERO, value=numeros_texto[palabra], linea=linea, columna=i+1, pos=i)
                tokens.append(token)

        if tokens:
            print("\n✅ Comando detectado:")
            for t in tokens:
                print(t)

        linea += 1

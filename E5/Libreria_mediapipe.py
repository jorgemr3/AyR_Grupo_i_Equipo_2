import cv2
import mediapipe as mp
import pygame
import tkinter as tk
from PIL import Image, ImageTk

# Inicializar pygame para reproducir música
pygame.mixer.init()

# Canciones (rutas locales)
song_peace = "E5\Peace.mp3"
song_metal = "E5\Metal.mp3"

# Estado actual
current_song = None
is_paused = False

# Configurar mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Función para reproducir canción
def play_song(song):
    global current_song, is_paused
    if current_song != song:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        current_song = song
        is_paused = False
    elif is_paused:
        pygame.mixer.music.unpause()
        is_paused = False

# Función para pausar canción
def pause_song():
    global is_paused
    if not is_paused and pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True

# Función para detectar qué dedos están levantados
def fingers_up(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Pulgar, índice, medio, anular, meñique
    fingers = []

    # Pulgar (comparar eje X porque es horizontal)
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Otros dedos (comparar eje Y porque son verticales)
    for tip in finger_tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# Detectar gestos
def detect_gesture(fingers):
    if fingers == [0, 1, 1, 0, 0]:  # ✌️
        return "PAZ"
    elif fingers == [0, 1, 0, 0, 1]:  # 🤘
        return "METAL"
    return None

# Interfaz gráfica
root = tk.Tk()
root.title("Detector de Gestos con Música (MediaPipe)")
root.geometry("900x700")
root.configure(bg="gray")

# Cargar imágenes
img_peace = Image.open("E5\Peace.jpg").resize((250, 250))
img_metal = Image.open("E5\Metal.jpg").resize((250, 250))
img_default = Image.open("E5\default.jpg").resize((250, 250))

photo_peace = ImageTk.PhotoImage(img_peace, master=root)
photo_metal = ImageTk.PhotoImage(img_metal, master=root)
photo_default = ImageTk.PhotoImage(img_default, master=root)

label_text = tk.StringVar()
label_text.set("Esperando gesto...")
label = tk.Label(root, textvariable=label_text, font=("Arial", 18), bg="gray", fg="white")
label.pack(pady=10)

canvas = tk.Label(root)
canvas.pack()

artist_label = tk.Label(root, image=photo_default, bg="gray")
artist_label.pack(pady=10)

# Configurar cámara
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

def update_frame():
    success, frame = cap.read()
    if not success:
        root.after(20, update_frame)
        return

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            fingers = fingers_up(hand_landmarks)
            gesture = detect_gesture(fingers)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Si una mano hace un gesto válido, lo usamos y rompemos el bucle
            if gesture is not None:
                break

    if gesture == "PAZ":
        root.configure(bg="#4da6ff")
        label.configure(bg="#4da6ff")
        label_text.set("✌️ Gesto detectado: Paz (Reproduciendo Paz)")
        artist_label.configure(image=photo_peace, bg="#4da6ff")
        play_song(song_peace)
    elif gesture == "METAL":
        root.configure(bg="#b30000")
        label.configure(bg="#b30000")
        label_text.set("🤘 Gesto detectado: Metal (Reproduciendo Metal)")
        artist_label.configure(image=photo_metal, bg="#b30000")
        play_song(song_metal)
    else:
        root.configure(bg="gray")
        label.configure(bg="gray")
        label_text.set("Esperando gesto...")
        artist_label.configure(image=photo_default, bg="gray")
        pause_song()

    # Mostrar cámara
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img, master=root)
    canvas.imgtk = imgtk
    canvas.configure(image=imgtk)

    root.after(20, update_frame)

update_frame()
root.mainloop()

cap.release()
cv2.destroyAllWindows()

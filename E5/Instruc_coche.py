import cv2
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp

# ---- Mediapipe inicialización ----
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def dedos_levantados(landmarks):
    """
    Devuelve un array [pulgar, índice, medio, anular, meñique]
    donde 1 = levantado, 0 = abajo
    """
    tips = [4, 8, 12, 16, 20]  # índices de las puntas de los dedos
    dedos = []

    # Pulgar → comparación en X
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        dedos.append(1)
    else:
        dedos.append(0)

    # Otros dedos → comparación en Y
    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)

    return dedos


def detectar_gesto(landmarks):
    dedos = dedos_levantados(landmarks)

    if dedos == [0, 1, 1, 0, 0]:
        return "Avanzar"      # Mano abierta
    elif dedos == [0, 0, 0, 0, 0]:
        return "Retroceder"      # Puño cerrado
    elif dedos == [0, 1, 0, 0, 0]:
        return "Girar izquierda"
    elif dedos == [0, 0, 0, 0, 1]:
        return "Girar derecha"
    elif dedos == [1 ,1, 1 ,1 ,1]:
        return "Detener"
    else:
        return f"Dedos levantados: {dedos}"


class HandDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control por gestos")
        self.root.geometry("1000x600")

        # ---- FRAME IZQUIERDO (CÁMARA) ----
        self.frame_cam = tk.Label(self.root)
        self.frame_cam.pack(side="left", padx=10, pady=10)

        # ---- FRAME DERECHO (ACCIONES) ----
        self.frame_info = tk.Frame(self.root, width=300, height=600, bg="lightgray")
        self.frame_info.pack(side="right", fill="both", expand=True)

        self.label_title = tk.Label(
            self.frame_info, text="Acciones detectadas",
            font=("Arial", 16, "bold"), bg="lightgray"
        )
        self.label_title.pack(pady=10)

        self.label_action = tk.Label(
            self.frame_info, text="Esperando gesto...",
            font=("Arial", 14), bg="white", width=25, height=3
        )
        self.label_action.pack(pady=20)

        # Inicializa la cámara
        self.cap = cv2.VideoCapture(0)
        self.hands = mp_hands.Hands(
            max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7
        )

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # efecto espejo

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            gesto = "Esperando gesto..."

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Dibujar esqueleto de la mano
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Detectar gesto
                    gesto = detectar_gesto(hand_landmarks.landmark)

            # Actualizar texto
            self.label_action.config(text=f"Gesto detectado: {gesto}")

            # Mostrar imagen en Tkinter
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            self.frame_cam.imgtk = imgtk
            self.frame_cam.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def run(self):
        self.root.mainloop()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = HandDetectionApp(root)
    app.run()

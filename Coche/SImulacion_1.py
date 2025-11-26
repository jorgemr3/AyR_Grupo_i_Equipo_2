import tkinter as tk
import math

class CarSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Coche")

        # Canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="green")  # fondo = pasto
        self.canvas.pack()

        # Carretera
        self.road_left = 200
        self.road_right = 600
        self.canvas.create_rectangle(self.road_left, 0, self.road_right, 600, fill="dimgray")

        # Línea central
        self.canvas.create_line(400, 0, 400, 600, fill="yellow", dash=(20, 20), width=3)

        # Meta e inicio
        self.meta_top, self.meta_bottom = 40, 80
        self.canvas.create_rectangle(self.road_left, self.meta_top, self.road_right, self.meta_bottom, fill="red")
        self.canvas.create_text(400, 30, text="META", font=("Arial", 14, "bold"), fill="black")

        self.inicio_top, self.inicio_bottom = 520, 560
        self.canvas.create_rectangle(self.road_left, self.inicio_top, self.road_right, self.inicio_bottom, fill="blue")
        self.canvas.create_text(400, 570, text="INICIO", font=("Arial", 14, "bold"), fill="black")

        # Posición inicial del coche
        self.start_x, self.start_y = 400, 540
        self.x, self.y = self.start_x, self.start_y
        self.angle = -90  # inicia mirando hacia arriba

        # Velocidades
        self.speed = 0
        self.acceleration = 0.05
        self.max_speed = 4
        self.reverse_speed = -3
        self.turn_speed = 2

        # Acción actual
        self.action = "stop"

        # Partes del coche
        self.car_parts = []
        self.draw_car()

        # Etiqueta de velocidad
        self.speed_label = self.canvas.create_text(650, 30, text="Velocidad: 0 px/s (0 km/h)", font=("Arial", 14), fill="white")

        # Controles
        self.root.bind("<Up>", lambda e: self.set_action("forward"))
        self.root.bind("<Down>", lambda e: self.set_action("backward"))
        self.root.bind("<Left>", lambda e: self.set_action("left"))
        self.root.bind("<Right>", lambda e: self.set_action("right"))
        self.root.bind("<space>", lambda e: self.set_action("stop"))

        self.update()

    def reset_position(self):
        """Reinicia el coche"""
        self.x, self.y = self.start_x, self.start_y
        self.angle = -90
        self.speed = 0
        self.action = "stop"

    def set_action(self, action):
        self.action = action

    def draw_car(self):
        """Dibuja el coche con orientación realista"""
        # Borrar coche anterior
        for part in self.car_parts:
            self.canvas.delete(part)
        self.car_parts.clear()

        car_length, car_width = 50, 25
        rad = math.radians(self.angle)

        def rotate_point(x, y):
            """Rotar coordenada local a global según ángulo"""
            return (self.x + x*math.cos(rad) - y*math.sin(rad),
                    self.y + x*math.sin(rad) + y*math.cos(rad))

        # Carrocería
        points = []
        for dx, dy in [(-car_length/2, -car_width/2), (car_length/2, -car_width/2),
                       (car_length/2, car_width/2), (-car_length/2, car_width/2)]:
            px, py = rotate_point(dx, dy)
            points.extend([px, py])
        body = self.canvas.create_polygon(points, fill="red", outline="black", width=2)
        self.car_parts.append(body)

        # Ventana
        win_pts = []
        for dx, dy in [(-10, -8), (10, -8), (10, 8), (-10, 8)]:
            px, py = rotate_point(dx, dy)
            win_pts.extend([px, py])
        window = self.canvas.create_polygon(win_pts, fill="skyblue", outline="black")
        self.car_parts.append(window)

        # Ruedas (rectángulos alargados que simulan óvalos)
        wheel_positions = [(-15, -15), (15, -15), (-15, 15), (15, 15)]
        for dx, dy in wheel_positions:
            wheel_pts = []
            for wx, wy in [(-6, -3), (6, -3), (6, 3), (-6, 3)]:
                px, py = rotate_point(dx + wx, dy + wy)
                wheel_pts.extend([px, py])
            wheel = self.canvas.create_polygon(wheel_pts, fill="black")
            self.car_parts.append(wheel)

        # Frente (luz gris)
        fx, fy = rotate_point(car_length/2 - 5, 0)
        front = self.canvas.create_oval(fx-4, fy-4, fx+4, fy+4, fill="gray", outline="black")
        self.car_parts.append(front)

    def update(self):
        # Movimiento continuo
        if self.action == "forward" and self.speed < self.max_speed:
            self.speed += self.acceleration
        elif self.action == "backward" and self.speed > self.reverse_speed:
            self.speed -= self.acceleration
        elif self.action in ["left", "right"]:
            if abs(self.speed) > 0.2:  # 🔹 Solo permite girar si se está moviendo
                if self.action == "left":
                    self.angle -= self.turn_speed
                elif self.action == "right":
                    self.angle += self.turn_speed
        elif self.action == "stop":
            if self.speed > 0:
                self.speed -= self.acceleration
            elif self.speed < 0:
                self.speed += self.acceleration
            if abs(self.speed) < 0.05:
                self.speed = 0

        # Mover coche
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

        # Verificar colisión con pasto
        if self.x < self.road_left or self.x > self.road_right:
            self.reset_position()

        # Meta
        if self.meta_top <= self.y <= self.meta_bottom and self.road_left <= self.x <= self.road_right:
            self.reset_position()

        # Redibujar coche
        self.draw_car()

        # Actualizar velocidad mostrada
        kmh = abs(self.speed * 10)  # escala ficticia para km/h
        self.canvas.itemconfig(self.speed_label, text=f"Velocidad: {self.speed:.2f} px/s ({kmh:.1f} km/h)")

        self.root.after(30, self.update)

# Ejecutar
root = tk.Tk()
app = CarSimulation(root)
root.mainloop()

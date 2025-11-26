import tkinter as tk
from tkinter import messagebox
import random

# ---------- Función para generar laberinto ----------
def generar_laberinto(n):
    lab = [['#' for _ in range(n)] for _ in range(n)]
    direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def en_rango(x, y):
        return 0 <= x < n and 0 <= y < n

    def tallar(x, y):
        lab[x][y] = ' '
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if en_rango(nx, ny) and lab[nx][ny] == '#':
                mx, my = x + dx // 2, y + dy // 2
                lab[mx][my] = ' '
                tallar(nx, ny)

    # Entrada y salida
    start_x, start_y = n - 1, 0
    exit_x, exit_y = 0, n - 1

    tallar(n - 2, 0)

    lab[start_x][start_y] = 'E'
    lab[exit_x][exit_y] = 'S'

    # Caminos falsos
    for _ in range(n // 2):
        x, y = random.randint(0, n - 1), random.randint(0, n - 1)
        if lab[x][y] == '#':
            lab[x][y] = ' '

    return lab


# ---------- Función para mostrar laberinto ----------
def mostrar_laberinto(laberinto):
    n = len(laberinto)
    cell_size = 25
    root = tk.Tk()
    root.title("Laberinto Procedural con Jugador")

    canvas = tk.Canvas(root, width=n * cell_size, height=n * cell_size)
    canvas.pack()

    colores = {
        '#': "black",   # pared
        ' ': "white",   # camino
        'E': "green",   # entrada
        'S': "red"      # salida
    }

    # Dibujar el laberinto
    for i in range(n):
        for j in range(n):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = colores.get(laberinto[i][j], "white")
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # Encontrar posición inicial del jugador (E)
    for i in range(n):
        for j in range(n):
            if laberinto[i][j] == 'E':
                jugador_pos = [i, j]
                break

    # Dibujar jugador
    jugador = canvas.create_rectangle(
        jugador_pos[1] * cell_size + 3,
        jugador_pos[0] * cell_size + 3,
        jugador_pos[1] * cell_size + cell_size - 3,
        jugador_pos[0] * cell_size + cell_size - 3,
        fill="blue"
    )

    # Función de movimiento
    def mover(dx, dy):
        new_x = jugador_pos[0] + dx
        new_y = jugador_pos[1] + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            if laberinto[new_x][new_y] in (' ', 'S'):  # espacio libre o salida
                jugador_pos[0], jugador_pos[1] = new_x, new_y
                canvas.coords(
                    jugador,
                    new_y * cell_size + 3,
                    new_x * cell_size + 3,
                    new_y * cell_size + cell_size - 3,
                    new_x * cell_size + cell_size - 3,
                )
                if laberinto[new_x][new_y] == 'S':
                    tk.messagebox.showinfo("¡Ganaste!", "Has llegado a la salida 🎉")

    # Asignar controles de movimiento
    root.bind("<w>", lambda e: mover(-1, 0))
    root.bind("<s>", lambda e: mover(1, 0))
    root.bind("<a>", lambda e: mover(0, -1))
    root.bind("<d>", lambda e: mover(0, 1))

    root.mainloop()


# ---------- Programa principal ----------
def main():
    try:
        n = int(input("Ingrese el tamaño del laberinto (n x n): "))
        if n < 5:
            print("Por favor ingrese un tamaño mayor o igual a 5.")
            return
        laberinto = generar_laberinto(n)
        mostrar_laberinto(laberinto)
    except ValueError:
        print("Ingrese un número válido.")

if __name__ == "__main__":
    main()

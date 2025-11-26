import tkinter as tk
from tkinter import messagebox
import random
import time

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


# ---------- Resolver laberinto (BFS) ----------
def resolver_laberinto(laberinto):
    n = len(laberinto)
    # Encontrar E y S
    for i in range(n):
        for j in range(n):
            if laberinto[i][j] == 'E':
                start = (i, j)
            elif laberinto[i][j] == 'S':
                end = (i, j)

    # BFS
    queue = [start]
    visitado = {start: None}

    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            break

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if laberinto[nx][ny] in (' ', 'S') and (nx, ny) not in visitado:
                    visitado[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    # reconstruir el camino
    camino = []
    actual = end
    while actual != start:
        camino.append(actual)
        actual = visitado.get(actual)
        if actual is None:
            return []  # No hay solución
    camino.append(start)
    camino.reverse()
    return camino


# ---------- Mostrar laberinto y resolver visualmente ----------
def mostrar_laberinto(laberinto):
    n = len(laberinto)
    cell_size = 25
    root = tk.Tk()
    root.title("Laberinto Procedural con Resolución Automática")

    canvas = tk.Canvas(root, width=n * cell_size, height=n * cell_size)
    canvas.pack()

    colores = {
        '#': "black",
        ' ': "white",
        'E': "green",
        'S': "red"
    }

    # Dibujar laberinto
    for i in range(n):
        for j in range(n):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = colores.get(laberinto[i][j], "white")
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # Resolver el laberinto
    camino = resolver_laberinto(laberinto)
    if not camino:
        messagebox.showerror("Error", "No se encontró salida en el laberinto.")
        root.mainloop()
        return

    # Crear jugador
    jugador = canvas.create_rectangle(0, 0, 0, 0, fill="blue")
    canvas.tag_raise(jugador)

    # Animar movimiento paso a paso
    def animar(pasos, i=0):
        if i >= len(pasos):
            messagebox.showinfo("¡Listo!", "¡El jugador ha llegado a la salida 🎉!")
            return
        x, y = pasos[i]
        canvas.coords(
            jugador,
            y * cell_size + 5,
            x * cell_size + 5,
            y * cell_size + cell_size - 5,
            x * cell_size + cell_size - 5
        )
        root.after(100, animar, pasos, i + 1)  # 100 ms entre pasos

    animar(camino)
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

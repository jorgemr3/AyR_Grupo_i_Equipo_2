import tkinter as tk
import random

# ---------- Función para generar laberinto ----------
def generar_laberinto(n):
    # Crear matriz de paredes
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

    # Generar caminos
    tallar(n - 2, 0)

    # Marcar entrada y salida
    lab[start_x][start_y] = 'E'
    lab[exit_x][exit_y] = 'S'

    # Crear caminos falsos
    for _ in range(n // 2):
        x, y = random.randint(0, n - 1), random.randint(0, n - 1)
        if lab[x][y] == '#':
            lab[x][y] = ' '

    return lab


# ---------- Función para mostrar laberinto ----------
def mostrar_laberinto(laberinto):
    n = len(laberinto)
    cell_size = 25  # tamaño de cada celda
    root = tk.Tk()
    root.title("Laberinto Procedural")

    canvas = tk.Canvas(root, width=n * cell_size, height=n * cell_size)
    canvas.pack()

    colores = {
        '#': "black",    # pared
        ' ': "white",    # camino
        'E': "green",    # entrada
        'S': "red"       # salida
    }

    for i in range(n):
        for j in range(n):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = colores.get(laberinto[i][j], "white")
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

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

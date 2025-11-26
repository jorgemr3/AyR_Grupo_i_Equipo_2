import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

# Nodos A hasta J (10 nodos)
nodos = [chr(i) for i in range(65, 75)]  # A..J
inicio, fin = 'A', 'J'

# Crear grafo dirigido
G = nx.DiGraph()

# Generar caminos aleatorios entre 3 y 5 por nodo
for nodo in nodos[:-1]:
    num_caminos = random.randint(3, 5)
    destinos = random.sample([x for x in nodos if x != nodo], num_caminos)
    for destino in destinos:
        peso = random.randint(1, 15)
        G.add_edge(nodo, destino, peso=peso)

# Posición de los nodos (ordenado en círculo)
pos = nx.shell_layout(G)

# Variables globales
mejor_distancia = float('inf')
camino_mejor = []
bloqueados = set()
contador_rutas = defaultdict(int)
terminar = False


# Función para mostrar la animación
def dibujar(camino_actual=None, persona=None, final=False):
    plt.clf()

    # Dibujar grafo base
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=900)
    etiquetas = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_color='black')

    # Aristas bloqueadas
    if bloqueados:
        nx.draw_networkx_edges(G, pos, edgelist=list(bloqueados), edge_color='red', width=2, style='dashed')

    # Camino actual (naranja)
    if camino_actual and len(camino_actual) > 1:
        aristas = [(camino_actual[i], camino_actual[i + 1]) for i in range(len(camino_actual) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas, edge_color='orange', width=3)

    # Mejor camino (verde)
    if camino_mejor and len(camino_mejor) > 1:
        aristas_mejor = [(camino_mejor[i], camino_mejor[i + 1]) for i in range(len(camino_mejor) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_mejor, edge_color='green', width=4)

    # Persona (círculo o marcador)
    if persona:
        x, y = pos[persona]
        plt.scatter(x, y, c='gold', s=500, edgecolors='black', zorder=5)

    # Mostrar título
    plt.title(
        f"Distancia mínima: {mejor_distancia if mejor_distancia != float('inf') else '---'}\n"
        f"Camino óptimo: {' → '.join(camino_mejor) if camino_mejor else '---'}",
        fontsize=12
    )
    plt.legend(
        handles=[
            plt.Line2D([0], [0], color='orange', lw=3, label='Camino actual'),
            plt.Line2D([0], [0], color='green', lw=3, label='Mejor camino'),
            plt.Line2D([0], [0], color='red', lw=2, linestyle='--', label='Bloqueado')
        ],
        loc='upper left', fontsize=8
    )

    # Si es la vista final, mostrar cuadro de resultados
    if final and camino_mejor:
        plt.text(
            0, -1.2,
            f"🏁 Camino final: {' → '.join(camino_mejor)}\n"
            f"Distancia total mínima: {mejor_distancia}",
            fontsize=13,
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black', boxstyle='round,pad=0.5'),
            ha='center'
        )

    plt.pause(0.4)


# Algoritmo de búsqueda con retroceso, bloqueos y control de repeticiones
def buscar(actual, camino, acumulado):
    global mejor_distancia, camino_mejor, terminar

    if terminar:
        return True

    # Mostrar posición actual
    dibujar(camino, persona=actual)

    # Si llega al final
    if actual == fin:
        if acumulado < mejor_distancia:
            mejor_distancia = acumulado
            camino_mejor = camino[:]
        return True

    # Si ya va peor que el mejor, bloquea y regresa
    if acumulado >= mejor_distancia:
        if len(camino) >= 2:
            bloqueados.add((camino[-2], camino[-1]))
        return False

    # Vecinos posibles no bloqueados
    vecinos = [v for v in G[actual] if (actual, v) not in bloqueados and v not in camino]
    random.shuffle(vecinos)

    for v in vecinos:
        peso = G[actual][v]['peso']
        ruta = tuple(camino + [v])
        contador_rutas[ruta] += 1

        # Si se repite más de 3 veces, terminar
        if contador_rutas[ruta] > 3:
            terminar = True
            return True

        resultado = buscar(v, camino + [v], acumulado + peso)
        if not resultado:
            bloqueados.add((actual, v))
        elif terminar:
            return True
        else:
            return True
    return False


# Ejecución visual
plt.ion()

for intento in range(20):
    if terminar:
        break
    dibujar([inicio], persona=inicio)
    exito = buscar(inicio, [inicio], 0)
    dibujar(camino_mejor, persona=fin)
    if not exito and len(bloqueados) >= len(G.edges()):
        break

plt.ioff()
dibujar(camino_mejor, persona=fin, final=True)
plt.show()

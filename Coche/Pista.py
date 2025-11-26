import pygame
pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Pista desde imagen")

# Carga de imagen
pista = pygame.image.load("pista.png")
pista = pygame.transform.scale(pista, (900, 700))

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.blit(pista, (0, 0))
    pygame.display.flip()
pygame.quit()

import pygame

class Brick:

    def __init__(self, position, dimensions):
        self.gameDisplay = pygame.display.get_surface()

        self.rect = pygame.Rect(
                position[0], position[1], dimensions[0], dimensions[1]
            )

        self.position = pygame.Vector2(position[0], position[1])
        self.speed = 12

        self.color = (0, 0, 0)

    def update(self):
        self.draw()

    def draw(self):
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)

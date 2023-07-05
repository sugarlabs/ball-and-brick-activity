import pygame

class Brick:

    def __init__(self, position, dimensions):
        self.gameDisplay = pygame.display.get_surface()

        self.rect = pygame.Rect(
                position[0], position[1], dimensions[0], dimensions[1]
            )
        
        self.color = (0, 0, 0)

    def update(self):
        self.draw()

    def draw(self, offset = (0, 0)):
        x, y = self.rect.x, self.rect.y
        self.rect.x += offset [0]
        self.rect.y += offset [1]
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)
        self.rect.x = x
        self.rect.y = y
import pygame
from random import random


class Ball:

    def __init__(self, position, radius):
        self.gameDisplay = pygame.display.get_surface()

        self.radius = radius
        self.position = pygame.Vector2(position[0], position[1])
        self.velocity = pygame.Vector2(7, -7)

        self.color = (0, 0, 0)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        bounce_padding = 10

        x_min = 0 + bounce_padding
        x_max = self.gameDisplay.get_width() - self.radius * 2 - bounce_padding
        y_min = 0 + bounce_padding
        y_max = self.gameDisplay.get_height() - self.radius * 2 - bounce_padding

        if self.position[0] <= x_min:
            self.position[0] = x_min
            self.velocity[0] *= -1

        if self.position[0] >= x_max:
            self.position[0] = x_max
            self.velocity[0] *= -1

        if self.position[1] <= y_min:
            self.position[1] = y_min
            self.velocity[1] *= -1
            
        if self.position[1] >= y_max:
            self.position[1] = y_max
            self.velocity[1] *= -1

        self.draw()

    def handle_collisions(self, paddle):
        ball_rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.radius * 2,
            self.radius * 2,
        )

        if ball_rect.colliderect(paddle):
            self.position[1] = paddle.y - self.radius * 2
            self.velocity[1] *= -1
            self.velocity.rotate_ip(random() * 10 - 5)

    def draw(self):
        pygame.draw.circle(
                    self.gameDisplay,
                    self.color,
                    (
                        int(self.position[0] + self.radius),
                        int(self.position[1] + self.radius),
                    ),
                    int(self.radius),
                )

    def check_collision(self, other_x, other_y, other_width, other_height):
        self_rect = pygame.Rect(self.x, self.y,
                                self.rect.width,
                                self.rect.height)
        other_rect = pygame.Rect(other_x, other_y,
                                 other_width,
                                 other_height)
        if self_rect.colliderect(other_rect):
            return True

# Copyright (C) 2023 Riya Jain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        self.velocity = pygame.Vector2(velocity[0], velocity[1])

    def set_position(self, position):
        self.position = pygame.Vector2(position[0], position[1])

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        bounce_padding = 10

        x_min = 0 + bounce_padding
        x_max = self.gameDisplay.get_width() - self.radius * 2 - bounce_padding
        y_min = 0 + bounce_padding
        y_max = self.gameDisplay.get_height() + self.radius * 4

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

    def is_lost(self):
        return self.position.y > self.gameDisplay.get_height()

    def bounce_against(self, rect):
        d = self.radius * 2
        overlap_x = max(0, min(rect.right, self.position.x + self.velocity.x) - max(rect.left, self.position.x))
        overlap_y = max(0, min(rect.bottom, self.position.y + self.velocity.y) - max(rect.top, self.position.y))

        if overlap_x < overlap_y:
            if self.velocity.x > 0:
                self.position.x = rect.left - d
            else:
                self.position.x = rect.right
            self.velocity.x *= -1
        else:
            if self.velocity.y > 0:
                self.position.y = rect.top - d
            else:
                self.position.y = rect.bottom
            self.velocity.y *= -1
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

    def check_collision(self, rect):
        ball_rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.radius * 2,
            self.radius * 2,
        )

        return ball_rect.colliderect(rect)

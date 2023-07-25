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

class Bat:

    def __init__(self, position, dimensions):
        self.gameDisplay = pygame.display.get_surface()

        self.rect = pygame.Rect(
                position[0], position[1], dimensions[0], dimensions[1]
            )

        self.position = pygame.Vector2(position[0], position[1])
        self.speed = 12

        self.color = (0, 0, 0)

    def move(self, direction):
        self.rect.x += self.speed * direction # 1-> Right; -1 -> Left

    def update(self):
        x_min = 0
        x_max = self.gameDisplay.get_width() - self.rect.width
        
        if self.rect.x < x_min:
            self.rect.x = x_min
        if self.rect.x > x_max:
            self.rect.x = x_max
            
        self.draw()

    def draw(self):
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)
